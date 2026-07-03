# KPIs del proyecto

## 1. Total de eventos procesados por día

**Definición:** cantidad total de eventos válidos procesados para una fecha.

**Fórmula:**

```text
Total eventos = COUNT(event_id) agrupado por event_date
```

**Interpretación:** mide el volumen diario de actividad pública en GitHub.

## 2. Usuarios únicos por día

**Definición:** cantidad de usuarios distintos que generaron eventos en una fecha.

**Fórmula:**

```text
Usuarios únicos = COUNT(DISTINCT actor_login)
```

**Interpretación:** mide cuántos actores participaron en la actividad pública.

## 3. Repositorios únicos por día

**Definición:** cantidad de repositorios distintos que recibieron actividad.

**Fórmula:**

```text
Repositorios únicos = COUNT(DISTINCT repo_name)
```

**Interpretación:** indica la diversidad de proyectos activos.

## 4. Tipo de evento dominante

**Definición:** tipo de evento con mayor frecuencia en una fecha.

**Fórmula:**

```text
Top evento = MAX(COUNT(event_type)) agrupado por event_type
```

**Interpretación:** permite identificar si predominan commits, issues, pull requests, stars u otros eventos.

## 5. Repositorios con mayor actividad

**Definición:** ranking de repositorios con más eventos procesados por fecha.

**Fórmula:**

```text
Total eventos por repo = COUNT(event_id) agrupado por event_date y repo_name
```

**Interpretación:** muestra los proyectos más activos dentro de la muestra analizada.

## 6. Relación usuario-repositorio

**Definición:** cantidad de relaciones generadas entre usuarios y repositorios en Neo4j.

**Fórmula:**

```cypher
MATCH (u:User)-[:INTERACTED_WITH]->(r:Repository)
RETURN count(*)
```

**Interpretación:** mide la conectividad del grafo y permite analizar interacción entre actores y proyectos.
