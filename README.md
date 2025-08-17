
# 🚀 Pipeline de Datos con Apache Airflow & PostgreSQL

  

> **Proyecto de Ingeniería de Datos | ETL Pipeline | Data Pipeline | Data Engineering**

  

[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

[![Apache Superset](https://img.shields.io/badge/Apache%20Superset-FF6B6B?style=for-the-badge&logo=apache&logoColor=white)](https://superset.apache.org/)

[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)

  

## 🎯 Descripción del Proyecto

  

Este proyecto demuestra un **pipeline de datos completo** implementado con las mejores prácticas de **Data Engineering**. Incluye la automatización de procesos ETL (Extract, Transform, Load) utilizando Apache Airflow para orquestar la carga y transformación de datos en PostgreSQL, y Apache Superset para la visualización y análisis de datos.

  

### 🔥 Características Destacadas

  

-  **🔄 Orquestación Automatizada**: DAGs de Airflow para pipeline de datos

-  **📊 Modelado de Datos**: Creación de tablas dimensionales y hechos

-  **📈 Dashboard Interactivo**: Visualización con Apache Superset

-  **🐳 Containerización**: Implementación con Docker para fácil despliegue

-  **📈 Pipeline ETL**: Proceso completo de extracción, transformación y carga

-  **🔒 Gestión de Conexiones**: Configuración segura de bases de datos

-  **📋 Monitoreo**: Logs y seguimiento de ejecución de tareas

  

## 🏗️ Arquitectura del Sistema

  

```

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐

│ Sample Data │───▶│ Apache Airflow │───▶│ PostgreSQL │───▶│ Apache Superset │

│ (CSV Files) │ │ (ETL Engine) │ │ (Data Lake) │ │ (Dashboard) │

└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘

│ │ │

▼ ▼ ▼

┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ DAGs │ │ OBT │ │ Charts & │

│ ETL │ │ Tables │ │ Dashboards │

└─────────────┘ └─────────────┘ └─────────────┘

```

  

## 🛠️ Stack Tecnológico

  

| Componente | Tecnología | Versión | Propósito |

|------------|------------|---------|-----------|

| **Orquestador** | Apache Airflow | 2.3.0 | Programación y monitoreo de pipelines |

| **Base de Datos** | PostgreSQL | Latest | Almacenamiento de datos |

| **Dashboard** | Apache Superset | Latest | Visualización y análisis de datos |

| **Containerización** | Docker & Docker Compose | 3.8 | Despliegue y escalabilidad |

| **Lenguaje** | Python | 3.8 | Lógica de transformación |

| **Gestión de Datos** | SQL | - | Consultas y transformaciones |

  

## 📁 Estructura del Proyecto

  

```

├── airflow/

│ └── dags/

│ └── initialise_data.py # 🎯 DAG principal de ETL

├── dbt/

│ └── sql/

│ └── create_and_populate_obt_orders.sql # 🔄 Transformaciones SQL

├── sample_data/ # 📊 Datos de entrada (CSV)

├── docker-compose.yml # 🐳 Orquestación de servicios

├── dockerfile # 🐳 Imagen personalizada de Airflow

└── scripts_airflow/ # ⚙️ Scripts de inicialización

```

  

## 🚀 Cómo Ejecutar

  

### Prerrequisitos

- Docker Desktop

- Docker Compose

- 8GB RAM disponible

  

### Pasos de Ejecución

  

```bash

# 1. Clonar el repositorio

git  clone  <repository-url>

cd  dbt-airflow-docker-compose-master

  

## 🎯 **Inicio Automático (Recomendado)**

```bash

# Hacer ejecutable el script

chmod +x start_project.sh

  

# Ejecutar inicio automático

./start_project.sh

```

  

## 📋 **Inicio Manual**

```bash

# 1. Crear red Docker (si no existe)

docker  network  create  superset-network

  

# 2. Levantar los servicios

docker-compose  up  -d

  

# 3. Acceder a los servicios

# 🌐 Airflow: http://localhost:8000

# 👤 Usuario: admin | 🔑 Contraseña: admin

# 🌐 Superset: http://localhost:8088/

# 👤 Usuario: admin | 🔑 Contraseña: admin

  

# 4. Ejecutar el DAG

# El DAG '1_load_initial_data' se ejecutará automáticamente

```

  

## ✅ **Verificación del Sistema**

  

### **1. Verificar Servicios**

```bash

docker-compose  ps

```

  

### **2. Verificar Logs de Airflow**

```bash

docker-compose  logs  airflow

```

  

### **3. Verificar Conexiones**

- Ve a Airflow: http://localhost:8000

- Admin → Connections

- Deberías ver: `dbt_postgres_instance_raw_data`

  

### **4. Ejecutar DAG Manualmente**

- En Airflow, ve al DAG `1_load_initial_data`

- Haz clic en "Play" para ejecutarlo manualmente

- Verifica que todas las tareas se completen exitosamente

  

### **5. Verificar en Superset**
- Ejecutar docker compose -f docker-compose-image-tag.yml up

- Ve a Superset: http://localhost:8088

- Conecta la base de datos usando la cadena: `postgresql+psycopg2://dbtuser:pssd@postgres-dbt:5432/dbtdb`

- Verifica que puedas ver las tablas creadas y juega con los datos 😃

```
![Superset](dbt-airflow-docker-compose-master/bi.png)
  

## 🔗 Conexiones y URLs

  

### Airflow

- **URL**: http://localhost:8000

- **Usuario**: `admin`

- **Contraseña**: `admin`

  

### Apache Superset

- **URL**: http://localhost:8088/

- **Usuario**: `admin`

- **Contraseña**: `admin`

  

### Base de Datos PostgreSQL

- **Host**: `postgres-dbt`

- **Puerto**: `5432`

- **Base de Datos**: `dbtdb`

- **Usuario**: `dbtuser`

- **Contraseña**: `pssd`

- **Cadena de Conexión**: `postgresql+psycopg2://dbtuser:pssd@postgres-dbt:5432/dbtdb`

  

## 📊 Modelo de Datos

  

### Tablas de Origen (Raw Data)

- **`business_types`** - Tipos de negocio y categorías

- **`customers`** - Información de clientes y metadata

- **`orders`** - Transacciones y pedidos

- **`currency_codes`** - Tasas de cambio y monedas

- **`site_codes`** - Ubicaciones geográficas

  

### Tabla de Destino (Analytics) - OBT

- **`obt_orders`** - **One Big Table** consolidada para análisis

  

#### 🎯 **Características de la Tabla OBT (One Big Table)**

  

La tabla `obt_orders` es el corazón del modelo de datos, implementando el patrón **One Big Table** que ofrece:

  

- **📊 Consolidación Completa**: Todos los datos de negocio en una sola tabla

- **🔗 Joins Pre-calculados**: Relaciones entre entidades ya resueltas

- **📈 Métricas Agregadas**: KPIs calculados automáticamente

- **🌍 Enriquecimiento Geográfico**: Datos de ubicación integrados

- **💰 Información Monetaria**: Múltiples monedas con tasas de cambio

- **📅 Dimensiones Temporales**: Fechas con atributos calculados

  

#### **Estructura de la OBT:**

```sql

-- Campos principales de la tabla OBT

order_id, order_date, delivery_date, delivery_day_of_week, delivery_month, delivery_quarter,

customer_id, customer_name, email_address, business_type_id, business_type_name,

is_key_account, customer_archived,

site_code, city_name, country_name, continent,

order_status, total, total_shipping, currency_ars, currency_mxn, currency_cop, currency_brl,

tracking_code, gmv_enabled, order_number, shipping_by_tracking,

latitude, longitude

```

  

## 🔄 Pipeline ETL

  

1.  **📥 Extract**: Carga de archivos CSV desde `sample_data/`

2.  **🔄 Transform**: Creación de esquemas y tablas con lógica de negocio

3.  **📤 Load**: Inserción de datos transformados en tablas analíticas

4.  **✅ Validate**: Verificación de integridad y calidad de datos

5.  **📊 Visualize**: Creación de dashboards en Apache Superset

  

## 📈 Casos de Uso

  

-  **Análisis de Ventas**: Seguimiento de pedidos y rendimiento

-  **Inteligencia de Negocio**: Dashboards y reportes ejecutivos

-  **Análisis Geográfico**: Distribución de clientes por ubicación

-  **Métricas de Negocio**: KPIs e indicadores de rendimiento

-  **Análisis Temporal**: Tendencias por día, mes y trimestre

-  **Segmentación de Clientes**: Análisis por tipo de negocio y cuenta clave

  

### Conexiones de Base de Datos

-  **Airflow DB**: PostgreSQL para metadatos de Airflow

-  **Data DB**: PostgreSQL para datos de negocio

-  **Superset**: Conexión a PostgreSQL para visualizaciones

 
  

## 🌟 Próximos Pasos

  

- [ ] Implementar tests de calidad de datos

- [ ] Agregar alertas y notificaciones

- [ ] Crear dashboards de monitoreo

- [ ] Implementar CI/CD para el pipeline

- [ ] Agregar más transformaciones de datos

- [ ] Implementar cache de Superset para mejor rendimiento

- [ ] Agregar autenticación LDAP/SSO

  

## 🔧 Solución de Problemas

  

Si encuentras el error `The conn_id 'dbt_postgres_instance_raw_data' isn't defined`, reinicia los servicios con `docker-compose restart`.

  

### 🚀 Solución Rápida

```bash

# Ejecutar script de reparación automática

docker-compose  restart

```

  

### 📋 Verificación Rápida

```bash

# Verificar estado de contenedores

docker-compose  ps

  

# Verificar conexiones en Airflow

docker-compose  exec  airflow  airflow  connections  list

``
