# Data notes
- One row represents one recorded workflow event.
- `request_id` identifies a synthetic service request.
- `event_name` is the workflow milestone.
- `event_time` is the timestamp recorded for that milestone.
- `service_region`, `priority`, and `asset_family` are request attributes repeated across events.
- The CSV includes 9 duplicate event rows and 11 missing region values for data-quality practice.
