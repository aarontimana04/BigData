use github_events;

db.github_events_raw.createIndex({ event_id: 1 }, { unique: true });
db.github_events_raw.createIndex({ type: 1 });
db.github_events_raw.createIndex({ created_at: 1 });
db.github_events_raw.createIndex({ event_date: 1 });
db.github_events_raw.createIndex({ "actor.login": 1 });
db.github_events_raw.createIndex({ "repo.name": 1 });
db.github_events_raw.createIndex({ source_file: 1 });
