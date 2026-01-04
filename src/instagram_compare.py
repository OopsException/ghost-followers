from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable


def _normalize_username(u: str) -> str:
    return (u or "").strip().lower()


def load_json_from_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_from_string(raw: str) -> Any:
    return json.loads(raw)


def extract_followers_usernames(followers_json: Any) -> list[str]:
    """
    Followers export structure (as provided):
    [
      {
        "string_list_data": [
          {"value": "username", ...}
        ],
        ...
      },
      ...
    ]

    We will:
    - iterate items
    - look inside string_list_data for any dict containing "value"
    """
    usernames: list[str] = []

    if not isinstance(followers_json, list):
        raise ValueError("Followers JSON must be a list at the top level.")

    for item in followers_json:
        if not isinstance(item, dict):
            continue
        sld = item.get("string_list_data", [])
        if not isinstance(sld, list):
            continue

        # Instagram typically places the username in the first element's "value"
        # but we scan the list safely.
        for entry in sld:
            if isinstance(entry, dict) and "value" in entry:
                val = entry.get("value")
                if isinstance(val, str) and val.strip():
                    usernames.append(_normalize_username(val))
                break  # stop after first found username per item

    # Deduplicate while preserving order
    return list(dict.fromkeys(usernames))


def extract_following_usernames(following_json: Any) -> list[str]:
    """
    Following export structure (as provided):
    {
      "relationships_following": [
        {
          "title": "username",
          ...
        },
        ...
      ]
    }
    """
    if not isinstance(following_json, dict):
        raise ValueError("Following JSON must be an object/dict at the top level.")

    rel = following_json.get("relationships_following", [])
    if not isinstance(rel, list):
        raise ValueError("Following JSON missing 'relationships_following' list.")

    usernames: list[str] = []
    for item in rel:
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        if isinstance(title, str) and title.strip():
            usernames.append(_normalize_username(title))

    # Deduplicate while preserving order
    return list(dict.fromkeys(usernames))


def compute_not_following_back(
    followers_usernames: Iterable[str],
    following_usernames: Iterable[str],
) -> list[str]:
    followers_set = { _normalize_username(u) for u in followers_usernames if _normalize_username(u) }
    result: list[str] = []
    seen: set[str] = set()

    for u in following_usernames:
        nu = _normalize_username(u)
        if not nu or nu in seen:
            continue
        seen.add(nu)
        if nu not in followers_set:
            result.append(nu)

    return result


@dataclass
class CompareResult:
    followers: list[str]
    following: list[str]
    not_following_back: list[str]
