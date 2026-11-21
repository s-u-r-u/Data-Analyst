-- MySQL 8+: import data/service_events.csv into service_events.
SELECT COUNT(*) AS event_rows, COUNT(DISTINCT request_id) AS requests,
       SUM(event_time IS NULL) AS missing_timestamps,
       SUM(service_region IS NULL) AS missing_regions
FROM service_events;

WITH request_span AS (
  SELECT request_id, MIN(event_time) AS opened_at, MAX(event_time) AS closed_at,
         MAX(priority) AS priority, MAX(service_region) AS service_region,
         MAX(asset_family) AS asset_family, COUNT(*) AS recorded_events
  FROM service_events WHERE event_time IS NOT NULL GROUP BY request_id
)
SELECT request_id, priority, service_region, asset_family, recorded_events,
       TIMESTAMPDIFF(MINUTE, opened_at, closed_at)/60.0 AS elapsed_hours
FROM request_span ORDER BY elapsed_hours DESC;

WITH request_span AS (
  SELECT request_id, MAX(service_region) AS service_region,
         TIMESTAMPDIFF(MINUTE,MIN(event_time),MAX(event_time))/60.0 AS elapsed_hours
  FROM service_events WHERE event_time IS NOT NULL GROUP BY request_id
)
SELECT COALESCE(service_region,'Unknown') AS service_region, COUNT(*) AS requests,
       ROUND(AVG(elapsed_hours),2) AS average_elapsed_hours
FROM request_span GROUP BY COALESCE(service_region,'Unknown')
ORDER BY average_elapsed_hours DESC;

SELECT DATE_FORMAT(event_time,'%Y-%m') AS event_month, event_name, COUNT(*) AS event_count
FROM service_events WHERE event_time IS NOT NULL
GROUP BY DATE_FORMAT(event_time,'%Y-%m'), event_name ORDER BY event_month,event_name;
