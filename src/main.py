from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .instagram_compare import (
    CompareResult,
    compute_not_following_back,
    extract_followers_usernames,
    extract_following_usernames,
    load_json_from_file,
    load_json_from_string,
)


def _write_outputs(result: CompareResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "not_following_back.json"
    txt_path = out_dir / "not_following_back.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result.not_following_back, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        for u in result.not_following_back:
            f.write(u + "\n")


def _load_inputs(args: argparse.Namespace) -> tuple[Any, Any]:
    # Prefer raw JSON strings if provided
    if args.followers_json:
        followers_obj = load_json_from_string(args.followers_json)
    else:
        followers_obj = load_json_from_file(args.followers)

    if args.following_json:
        following_obj = load_json_from_string(args.following_json)
    else:
        following_obj = load_json_from_file(args.following)

    return followers_obj, following_obj


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare Instagram followers vs following and list accounts that don't follow back."
    )

    group_fol = parser.add_mutually_exclusive_group(required=True)
    group_fol.add_argument("--followers", help="Path to followers JSON file")
    group_fol.add_argument("--followers-json", help="Raw followers JSON string")

    group_ing = parser.add_mutually_exclusive_group(required=True)
    group_ing.add_argument("--following", help="Path to following JSON file")
    group_ing.add_argument("--following-json", help="Raw following JSON string")

    parser.add_argument(
        "--write",
        action="store_true",
        help="Write results to output/not_following_back.json and .txt",
    )
    parser.add_argument(
        "--out-dir",
        default="output",
        help="Output directory (default: output)",
    )

    args = parser.parse_args()

    followers_obj, following_obj = _load_inputs(args)

    followers_usernames = extract_followers_usernames(followers_obj)
    following_usernames = extract_following_usernames(following_obj)
    not_following_back = compute_not_following_back(followers_usernames, following_usernames)

    result = CompareResult(
        followers=followers_usernames,
        following=following_usernames,
        not_following_back=not_following_back,
    )

    print(f"Followers: {len(result.followers)}")
    print(f"Following: {len(result.following)}")
    print(f"Not following back: {len(result.not_following_back)}")

    # Print a preview (first 30)
    preview = result.not_following_back[:30]
    if preview:
        print("\nPreview (up to 30):")
        for u in preview:
            print(f"- {u}")

    if args.write:
        out_dir = Path(args.out_dir)
        _write_outputs(result, out_dir)
        print(f"\nWrote output to: {out_dir.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
