# Arquitectura propuesta

## Objetivo

Diseñar una arquitectura Big Data multimodelo para analizar eventos públicos de GitHub obtenidos desde GH Archive.

## Componentes

```text
GH Archive
   ↓
Airflow
   ↓
Zona raw: data/raw o Cloud Storage
   ↓
Scripts Python ETL
   ↓
MongoDB       Cassandra       Neo4j
   ↓             ↓              ↓
Dashboard Streamlit
```

## Justificación de tecnologías

### MongoDB

Se usa para almacenar los documentos originales. Los eventos de GitHub son JSON semiestructurados y el campo `payload` cambia según el tipo de evento. MongoDB permite preservar esa variabilidad sin forzar un esquema rígido.

### Cassandra

Se usa para consultas masivas y series temporales. Las tablas están diseñadas para responder preguntas por fecha, hora, tipo de evento, usuario y repositorio.

### Neo4j

Se usa para representar relaciones naturales del dominio:

- Usuario realiza evento.
- Evento ocurre en repositorio.
- Repositorio pertenece a organización.
- Usuario interactúa con repositorio.

## Despliegue en GCP

Para cuidar créditos gratuitos, se propone iniciar con una VM de Compute Engine usando Docker Compose. Cloud Storage puede usarse como zona raw si se desea persistencia en GCP.

Servicios en la VM:

- MongoDB
- Cassandra
- Neo4j
- Airflow
- Streamlit

## Flujo de Airflow

1. Extracción de datos.
2. Validación y limpieza.
3. Carga en MongoDB.
4. Transformación y carga en Cassandra.
5. Construcción de relaciones y carga en Neo4j.
6. Generación automática de indicadores.
