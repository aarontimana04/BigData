CREATE KEYSPACE IF NOT EXISTS github_events
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE github_events;

CREATE TABLE IF NOT EXISTS events_by_day_type (
    event_date date,
    event_type text,
    event_hour int,
    total_events int,
    PRIMARY KEY ((event_date), event_type, event_hour)
);

CREATE TABLE IF NOT EXISTS repo_activity_by_day (
    event_date date,
    repo_name text,
    event_type text,
    total_events int,
    unique_actors int,
    PRIMARY KEY ((event_date), repo_name, event_type)
);

CREATE TABLE IF NOT EXISTS actor_activity_by_day (
    event_date date,
    actor_login text,
    total_events int,
    push_events int,
    pull_request_events int,
    issue_events int,
    watch_events int,
    PRIMARY KEY ((event_date), actor_login)
);

CREATE TABLE IF NOT EXISTS kpis_by_day (
    event_date date,
    total_events int,
    unique_actors int,
    unique_repositories int,
    top_event_type text,
    generated_at timestamp,
    PRIMARY KEY ((event_date))
);
