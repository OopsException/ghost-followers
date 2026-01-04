# Insta Follow Checker

A simple Python CLI tool that compares your **Instagram followers and following lists**
and identifies accounts you follow that **do not follow you back**.

This tool works directly with the **default JSON files** provided by Instagram’s data
export. No API access, login, or manual editing required.


## Features

- Uses official Instagram data export (JSON)
- No API keys or authentication required
- Works with Instagram’s default export structure
- Supports file input or raw JSON strings
- Optional output to `.json` and `.txt` files
- No third-party dependencies


## How It Works

1. Extracts follower usernames from `followers.json`
2. Extracts following usernames from `following.json`
3. Normalizes usernames (trimmed + lowercase)
4. Compares the two lists
5. Outputs accounts you follow that **do not follow you back**

Duplicate usernames are removed while preserving order.


## Getting Your Instagram Data

1. Open Instagram
2. Go to **Settings → Accounts Center**
3. Select **Your information and permissions**
4. Choose **Download your information**
5. Select **Download or transfer information**
6. Choose your Instagram account
7. Select **Some of your information**
8. Check **Followers and following**
9. Choose **JSON** format
10. Request download
11. Download and extract the archive
12. Locate the following files:
    - `followers.json`
    - `following.json`


## Usage

Run the tool using Python’s module syntax:

```bash
python -m src.main --followers followers.json --following following.json
python -m src.main --followers followers.json --following following.json --write
```
