# Modelos de datos

## MongoDB

Colección principal:

```text
github_events_raw
```

Uso:

- Conserva el JSON original.
- Permite trazabilidad del evento.
- Soporta estructuras variables en `payload`.

Ejemplo simplificado:

```json
{
  "_id": "49876637080",
  "event_id": "49876637080",
  "type": "PushEvent",
  "actor_login": "usuario",
  "repo_name": "owner/repository",
  "payload": {},
  "created_at": "2026-06-01T00:15:22Z",
  "event_date": "2026-06-01",
  "event_hour": 0
}
```

## Cassandra

Tablas principales:

```text
events_by_day_type
repo_activity_by_day
actor_activity_by_day
kpis_by_day
```

Uso:

- Consultas por fecha.
- Agregados temporales.
- Métricas por repositorio y usuario.

## Neo4j

Nodos:

```text
(:User)
(:Repository)
(:Organization)
(:Event)
(:EventType)
```

Relaciones:

```text
(:User)-[:TRIGGERED]->(:Event)
(:Event)-[:ON_REPOSITORY]->(:Repository)
(:Event)-[:HAS_TYPE]->(:EventType)
(:User)-[:INTERACTED_WITH]->(:Repository)
(:Repository)-[:BELONGS_TO]->(:Organization)
```

Uso:

- Analizar conectividad.
- Encontrar usuarios más activos.
- Encontrar repositorios más conectados.
- Analizar relaciones entre organizaciones, usuarios y repositorios.
