# Analytics Domain Specification

## 1. Domain Overview
The Analytics Domain ingests system-wide events to generate business intelligence, user listening reports (e.g., "SpotiGram Wrapped"), and mood trends.

## 2. Aggregates & Entities
- **Aggregate Root:** `AnalyticsReport`
- **Entities:** `MetricDataPoint`

## 3. Business Rules

### Metrics & KPIs
- **System KPIs:** DAU (Daily Active Users), Post Creation Rate, AI DJ Engagement Rate.
- **User Metrics:** Top Artists, Most Played Genres, Prevailing Moods.

### Rules
- **Music DNA & Mood Reports:** Generated monthly for users.
- **Retention Policy:** Raw interaction events are kept in cold storage (S3/GCS) for 1 year. Aggregated metrics are kept indefinitely.
- **Aggregation Frequency:** Rollups happen hourly, daily, and monthly via background cron jobs.

## 4. Domain Events
- `MonthlyReportGeneratedEvent(user_id, report_url)`
- `SystemKpiThresholdAlertEvent(kpi_name, value)`

## 5. Testability Requirements
- **Integration:** Test the map-reduce/aggregation logic against a mocked dataset of 100,000 raw events.
