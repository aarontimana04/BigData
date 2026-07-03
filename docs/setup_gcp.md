# Setup inicial en Google Cloud Platform

## Objetivo

Montar una versión económica del proyecto usando créditos gratuitos de GCP.

## Arquitectura recomendada para iniciar

Para evitar costos innecesarios, el despliegue inicial puede hacerse en una sola VM de Compute Engine con Docker Compose.

```text
Compute Engine VM
├── Airflow
├── MongoDB
├── Cassandra
├── Neo4j
├── Streamlit
└── Scripts Python ETL
```

Cloud Storage puede usarse como zona raw para guardar archivos descargados desde GH Archive.

## Servicios de GCP sugeridos

| Servicio | Uso |
|---|---|
| Compute Engine | Ejecutar Docker Compose con las bases y Airflow |
| Cloud Storage | Guardar archivos raw y procesados |
| Cloud Logging | Revisar logs de la VM |
| IAM | Controlar permisos |

## VM sugerida para pruebas

```text
Sistema operativo: Ubuntu 22.04 LTS
Tipo de máquina inicial: e2-standard-4
Disco: 80 GB o 100 GB
```

Si el consumo sube demasiado, se puede reducir el volumen de datos o apagar la VM cuando no se use.

## Buenas prácticas para créditos gratuitos

1. Crear presupuesto y alerta de gasto.
2. Apagar la VM cuando no se esté usando.
3. No cargar demasiados días de GH Archive al inicio.
4. Empezar con 1 archivo horario y luego escalar.
5. No subir archivos `.json.gz` grandes al repositorio de GitHub.
6. Guardar datos pesados en Cloud Storage, no en GitHub.

## Estructura sugerida de bucket

```text
gs://bucket-bigdata-github-events/
├── raw/
│   └── gharchive/
├── processed/
└── logs/
```

## Comandos base en la VM

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER
```

Cerrar sesión y volver a entrar antes de usar Docker.

Luego:

```bash
git clone https://github.com/aarontimana04/BigData.git
cd BigData
cp .env.example .env
docker compose up -d
```

## Puertos importantes

| Servicio | Puerto |
|---|---|
| Airflow | 8080 |
| Neo4j Browser | 7474 |
| Streamlit | 8501 |
| MongoDB | 27017 |
| Cassandra | 9042 |

En GCP, solo deberían abrirse temporalmente los puertos necesarios para la exposición o pruebas.
