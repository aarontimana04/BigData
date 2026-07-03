CREATE CONSTRAINT user_login_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.login IS UNIQUE;

CREATE CONSTRAINT repository_name_unique IF NOT EXISTS
FOR (r:Repository) REQUIRE r.name IS UNIQUE;

CREATE CONSTRAINT organization_login_unique IF NOT EXISTS
FOR (o:Organization) REQUIRE o.login IS UNIQUE;

CREATE CONSTRAINT event_id_unique IF NOT EXISTS
FOR (e:Event) REQUIRE e.event_id IS UNIQUE;

CREATE CONSTRAINT event_type_name_unique IF NOT EXISTS
FOR (t:EventType) REQUIRE t.name IS UNIQUE;
