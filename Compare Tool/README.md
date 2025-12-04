# JSON Key Compare for Translating

Compare voth JSON file to find new keys and changed values.

## Why You need to use this?

By updating, new key can be added and some values(strings) can be changed.

You can find these changes easily with this tool for helping updating.

## What it does

It needs 2 JSON(Original JSON and Target JSON) to work.

Original JSON is old version of lang file, and Target JSON is new version of lang file.

By select JSON and press button at GUI, It gonna make new .txt file contains which contains new keys at Target JSON and keys which value was changed.

Here is example:

Original JSON

```json
{
    "key": "value1"
}
```

Target JSON

```json
{
    "key": "value2",
    "new_key": "new_value"
}
```

compare_key.txt

```txt
new keys (Total: 1):
"new_key"

---

changed keys (Total: 1):
"key"
```

## How can I use it?

Open gui as bash, use cmd or VS code

```bash
python compare_tool.py
```