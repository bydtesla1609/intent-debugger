#!/usr/bin/env python3
"""Persist clone events and release ZIP downloads as one acquisition total."""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "metrics" / "acquisitions.json"
BADGE_PATH = ROOT / "metrics" / "acquisitions-badge.json"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "bydtesla1609/intent-debugger")
TOKEN = (
    os.environ.get("TRAFFIC_TOKEN")
    or os.environ.get("GH_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
)


def github_json(path: str, *, token: str | None = TOKEN):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "intent-debugger-metrics",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def release_zip_downloads() -> int:
    total = 0
    page = 1
    while True:
        releases = github_json(
            f"/repos/{REPOSITORY}/releases?per_page=100&page={page}", token=TOKEN
        )
        for release in releases:
            total += sum(
                int(asset["download_count"])
                for asset in release.get("assets", [])
                if asset.get("name") == "intent-debugger-skill.zip"
            )
        if len(releases) < 100:
            return total
        page += 1


def main() -> None:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    clone_days = {
        key: int(value)
        for key, value in metrics["clone_days"].items()
        if int(value) > 0
    }

    try:
        clones = github_json(f"/repos/{REPOSITORY}/traffic/clones?per=day")
    except urllib.error.HTTPError as error:
        if error.code != 403:
            raise
        print("::warning::The token cannot read repository traffic; clone totals were preserved.")
    else:
        for day in clones["clones"]:
            date = day["timestamp"][:10]
            count = int(day["count"])
            if count > 0:
                clone_days[date] = max(clone_days.get(date, 0), count)

    clone_count = sum(clone_days.values())
    zip_download_count = release_zip_downloads()
    changed = (
        clone_days != metrics["clone_days"]
        or clone_count != metrics["clone_count"]
        or zip_download_count != metrics["zip_download_count"]
    )

    metrics.update(
        clone_days=dict(sorted(clone_days.items())),
        clone_count=clone_count,
        zip_download_count=zip_download_count,
        total_acquisitions=clone_count + zip_download_count,
    )
    if changed:
        metrics["updated_at"] = dt.datetime.now(dt.timezone.utc).replace(
            microsecond=0
        ).isoformat().replace("+00:00", "Z")

    badge = {
        "schemaVersion": 1,
        "label": "total acquisitions",
        "message": str(metrics["total_acquisitions"]),
        "color": "0ea5e9",
    }
    assert metrics["clone_count"] == sum(metrics["clone_days"].values())
    assert metrics["total_acquisitions"] == (
        metrics["clone_count"] + metrics["zip_download_count"]
    )
    METRICS_PATH.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    BADGE_PATH.write_text(
        json.dumps(badge, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(
        f"clones={clone_count} zip_downloads={zip_download_count} "
        f"total={metrics['total_acquisitions']}"
    )


if __name__ == "__main__":
    main()
