# BigData - GitHub Events Multimodel Analytics

Proyecto grupal de Big Data apoyado en Google Cloud Platform.

## Tema

Análisis multimodelo de eventos públicos de GitHub usando datos semiestructurados de **GH Archive**.

La fuente de datos publica eventos públicos de GitHub en archivos horarios `.json.gz`. Cada línea del archivo es un documento JSON que representa un evento, por ejemplo `PushEvent`, `PullRequestEvent`, `IssuesEvent`, `WatchEvent`, entre otros.

## Objetivo

Construir una arquitectura Big Data que permita extraer, procesar, almacenar y analizar eventos públicos de GitHub usando tres modelos de base de datos:

- **MongoDB**: almacenamiento de documentos JSON originales.
- **Cassandra**: almacenamiento de métricas temporales y consultas masivas.
- **Neo4j**: análisis de relaciones entre usuarios, eventos, repositorios y organizaciones.

## Arquitectura general

```text
GH Archive
   ↓
Apache Airflow
   ↓
Google Cloud Storage / almacenamiento raw local
   ↓
Procesamiento Python
   ↓
MongoDB       Cassandra       Neo4j
   ↓             ↓              ↓
Streamlit Dashboard
```

## Estructura del repositorio

```text
.
├── airflow/
│   └── dags/
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── databases/
│   ├── cassandra/
│   ├── mongodb/
│   └── neo4j/
├── docs/
└── scripts/
```

## Fuente de datos

Ejemplo de archivo horario:

```text
https://data.gharchive.org/2026-06-01-0.json.gz
```

Para simular actualizaciones incrementales, el DAG de Airflow descarga una hora distinta por ejecución.

## Flujo ETL

1. Extraer archivo `.json.gz` desde GH Archive.
2. Validar y limpiar eventos.
3. Cargar JSON original en MongoDB.
4. Generar agregados temporales y cargar en Cassandra.
5. Crear nodos y relaciones en Neo4j.
6. Generar KPIs para el dashboard.

## Ejecución local inicial

1. Copiar variables de entorno:

```bash
cp .env.example .env
```

2. Levantar servicios:

```bash
docker compose up -d
```

3. Instalar dependencias locales si se ejecutan scripts fuera de Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Ejecutar una carga de prueba:

```bash
python scripts/run_pipeline_once.py --date 2026-06-01 --hour 0
```

5. Abrir el dashboard:

```bash
streamlit run dashboard/app.py
```

## Entregables del proyecto

- Código fuente completo.
- Scripts de creación de bases de datos.
- DAG de Airflow.
- Dashboard funcional.
- Informe técnico en PDF.
- Video demostrativo de máximo 15 minutos.
