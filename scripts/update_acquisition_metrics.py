#!/usr/bin/env python3
"""Persist repository clones and release ZIP downloads as one total."""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "metrics" / "acquisitions.json"
BADGE_PATH = ROOT / "metrics" / "acquisitions-badge.json"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "bydtesla1609/intent-debugger")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
TRAFFIC_TOKEN = (
    os.environ.get("TRAFFIC_TOKEN")
    or os.environ.get("GH_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
)
CONTENTS_TOKEN = (
    os.environ.get("GH_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
    or TRAFFIC_TOKEN
)
RUNNING_IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"


def github_json(
    path: str,
    *,
    token: str | None,
    method: str = "GET",
    body: dict | None = None,
):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "intent-debugger-metrics",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers=headers,
        data=data,
        method=method,
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def load_json(path: Path) -> tuple[dict, str | None]:
    if not RUNNING_IN_ACTIONS:
        return json.loads(path.read_text(encoding="utf-8")), None
    relative_path = path.relative_to(ROOT).as_posix()
    response = github_json(
        f"/repos/{REPOSITORY}/contents/{relative_path}?ref="
        f"{urllib.parse.quote(BRANCH)}",
        token=CONTENTS_TOKEN,
    )
    content = base64.b64decode(response["content"]).decode()
    return json.loads(content), response["sha"]


def save_json(path: Path, value: dict, sha: str | None, *, compact: bool) -> None:
    separators = (",", ":") if compact else None
    content = json.dumps(
        value, ensure_ascii=False, indent=None if compact else 2, separators=separators
    ) + "\n"
    if not RUNNING_IN_ACTIONS:
        path.write_text(content, encoding="utf-8")
        return
    relative_path = path.relative_to(ROOT).as_posix()
    github_json(
        f"/repos/{REPOSITORY}/contents/{relative_path}",
        token=CONTENTS_TOKEN,
        method="PUT",
        body={
            "message": "Update download metrics",
            "content": base64.b64encode(content.encode()).decode(),
            "sha": sha,
            "branch": BRANCH,
        },
    )


def release_zip_downloads() -> int:
    total = 0
    page = 1
    while True:
        releases = github_json(
            f"/repos/{REPOSITORY}/releases?per_page=100&page={page}",
            token=CONTENTS_TOKEN,
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
    metrics, metrics_sha = load_json(METRICS_PATH)
    previous_badge, badge_sha = load_json(BADGE_PATH)
    clone_days = {
        key: int(value)
        for key, value in metrics["clone_days"].items()
        if int(value) > 0
    }

    try:
        clones = github_json(
            f"/repos/{REPOSITORY}/traffic/clones?per=day", token=TRAFFIC_TOKEN
        )
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
    total_downloads = clone_count + zip_download_count
    badge = {
        "schemaVersion": 1,
        "label": "total downloads",
        "message": str(total_downloads),
        "color": "0ea5e9",
    }
    changed = (
        clone_days != metrics["clone_days"]
        or clone_count != metrics["clone_count"]
        or zip_download_count != metrics.get("zip_download_count")
        or total_downloads != metrics.get("total_downloads")
        or previous_badge != badge
    )

    metrics["clone_days"] = dict(sorted(clone_days.items()))
    metrics["clone_count"] = clone_count
    metrics["zip_download_count"] = zip_download_count
    metrics["total_downloads"] = total_downloads
    if changed:
        metrics["updated_at"] = dt.datetime.now(dt.timezone.utc).replace(
            microsecond=0
        ).isoformat().replace("+00:00", "Z")

    assert metrics["clone_count"] == sum(metrics["clone_days"].values())
    assert metrics["total_downloads"] == (
        metrics["clone_count"] + metrics["zip_download_count"]
    )
    if changed or not RUNNING_IN_ACTIONS:
        save_json(METRICS_PATH, metrics, metrics_sha, compact=False)
        save_json(BADGE_PATH, badge, badge_sha, compact=True)
    print(
        f"clones={clone_count} zip_downloads={zip_download_count} "
        f"total_downloads={total_downloads}"
    )


if __name__ == "__main__":
    main()
