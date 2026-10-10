# MCP tools

| Tool | Purpose |
| --- | --- |
| android_privileges | Report Core identity |
| android_start / android_stop | Create or release the owned display |
| android_status / android_windows | Display status or activity names |
| android_launch | Launch a full Android component |
| android_tap / android_swipe | Coordinates from fresh UI data |
| android_key | Allowed navigation keys |
| android_capture | PNG of the virtual screen |
| android_inspect_ui | Structured UI nodes |
| android_click_text | Exactly one matching clickable text |
| android_set_text | Exactly one focused non-password editable field |
| android_batch | 1–18 known steps, with partial results on failure |
| android_job_result | Retrieve a pending relay result |

The relay adds `request_id` to every Core call: 8–80 ASCII letters, digits, underscores or hyphens. A new action gets a fresh ID; reuse only on a network retry of that identical action. The agent strips it before Core.

Calls wait up to eight seconds for results. For a pending response use android_job_result with its job_id; never resubmit to poll. Results expire after 15 minutes; request tombstones prevent expired-ID replay.

Batch known steps and inspect at decision points. Click/set text already read fresh nodes. Focus the field before set_text and release the screen after verification. Sending messages requires the owner's explicit recipient and content instructions.
