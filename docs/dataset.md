# Dataset: GH Archive

## Fuente

GH Archive publica la actividad pública de GitHub en archivos horarios comprimidos en formato `.json.gz`.

Ejemplo:

```text
https://data.gharchive.org/2026-06-01-0.json.gz
```

## Naturaleza de los datos

Los datos son semiestructurados porque cada registro es un documento JSON. Todos los eventos comparten campos principales, pero el campo `payload` cambia según el tipo de evento.

## Campos principales

| Campo | Descripción |
|---|---|
| `id` | Identificador único del evento |
| `type` | Tipo de evento, por ejemplo `PushEvent` |
| `actor` | Usuario que ejecutó el evento |
| `repo` | Repositorio donde ocurrió el evento |
| `payload` | Detalle específico según el tipo de evento |
| `public` | Indica si el evento es público |
| `created_at` | Fecha y hora de creación del evento |
| `org` | Organización asociada, si existe |

## Volumen

El proyecto trabajará inicialmente con archivos horarios. Para la demostración se recomienda cargar entre 1 y 3 días:

```text
1 día = 24 archivos horarios
3 días = 72 archivos horarios
```

Esto supera el requisito mínimo de 50,000 registros.

## Actualización incremental

La actualización incremental se simula cargando una hora nueva por ejecución:

```text
Ejecución 1: 2026-06-01-0.json.gz
Ejecución 2: 2026-06-01-1.json.gz
Ejecución 3: 2026-06-01-2.json.gz
```

## Campos derivados

Durante la limpieza se agregan campos derivados para facilitar consultas:

| Campo derivado | Descripción |
|---|---|
| `event_id` | ID del evento como texto |
| `event_date` | Fecha del evento |
| `event_hour` | Hora del evento |
| `actor_login` | Login del usuario |
| `repo_name` | Nombre completo del repositorio |
| `org_login` | Login de la organización |
| `source_file` | Archivo de origen |
| `ingestion_timestamp` | Momento de ingesta |
