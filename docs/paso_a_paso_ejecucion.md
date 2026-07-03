# Paso a paso de ejecución local

## 1. Clonar el repositorio

```bash
git clone https://github.com/aarontimana04/BigData.git
cd BigData
```

## 2. Crear archivo de variables de entorno

```bash
cp .env.example .env
```

Para ejecución local fuera de Docker, puedes dejar los valores `localhost`.

## 3. Levantar servicios

```bash
docker compose up -d
```

Servicios disponibles:

| Servicio | URL / puerto |
|---|---|
| Airflow | http://localhost:8080 |
| MongoDB | localhost:27017 |
| Cassandra | localhost:9042 |
| Neo4j Browser | http://localhost:7474 |
| Streamlit | http://localhost:8501 |

Credenciales iniciales:

| Servicio | Usuario | Contraseña |
|---|---|---|
| Airflow | admin | admin |
| MongoDB | admin | admin |
| Neo4j | neo4j | password123 |

## 4. Instalar dependencias para ejecución local opcional

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Ejecutar una carga de prueba

```bash
python scripts/run_pipeline_once.py --date 2026-06-01 --hour 0
```

Esto realizará:

1. Descarga del archivo horario desde GH Archive.
2. Descompresión del `.json.gz`.
3. Validación y limpieza.
4. Carga en MongoDB.
5. Agregación y carga en Cassandra.
6. Carga parcial en Neo4j.
7. Generación de KPIs.

## 6. Ejecutar desde Airflow

1. Abrir Airflow:

```text
http://localhost:8080
```

2. Ingresar con:

```text
usuario: admin
contraseña: admin
```

3. Activar el DAG:

```text
github_events_pipeline
```

4. Ejecutar manualmente el DAG.

Puedes cambiar los parámetros:

```json
{
  "date": "2026-06-01",
  "hour": 0
}
```

## 7. Abrir dashboard

```text
http://localhost:8501
```

Selecciona la fecha cargada, por ejemplo:

```text
2026-06-01
```

## 8. Apagar servicios

```bash
docker compose down
```

Si deseas borrar volúmenes y reiniciar desde cero:

```bash
docker compose down -v
```
