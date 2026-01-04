# Insta Follow Checker

Compares Instagram followers vs following exports and lists accounts you follow that don't follow you back.

## Input formats expected

### Followers JSON
A list of objects, each containing `string_list_data` with a `value` username:
```json
[
  {
    "string_list_data": [
      { "value": "uniparcel" }
    ]
  }
]