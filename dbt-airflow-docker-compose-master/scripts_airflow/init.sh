#!/usr/bin/env bash

echo "🚀 Iniciando configuración de Airflow..."

# Setup DB Connection String para Airflow
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Configurar otras variables de entorno
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__CORE__LOAD_EXAMPLES=False

# Configurar conexión a la base de datos DBT
export DBT_POSTGRESQL_CONN="postgresql://${DBT_POSTGRES_USER}:${DBT_POSTGRES_PASSWORD}@${DBT_POSTGRES_HOST}:${DBT_POSTGRES_PORT}/${DBT_POSTGRES_DB}"

echo "📊 Configuración de base de datos:"
echo "   Airflow DB: $AIRFLOW__CORE__SQL_ALCHEMY_CONN"
echo "   DBT DB: $DBT_POSTGRESQL_CONN"

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
echo "   Esperando 10 segundos para que PostgreSQL se inicialice..."
sleep 10

# Verificar conectividad simple
echo "   Verificando conectividad a PostgreSQL..."
echo "   Esperando a que PostgreSQL esté listo..."
sleep 15

# Compilar DBT
echo "🔨 Compilando modelos DBT..."
cd /dbt && dbt compile

# Limpiar archivos temporales
rm -f /airflow/airflow-webserver.pid

echo "🗄️ Inicializando base de datos de Airflow..."
sleep 5

# Inicializar la base de datos de Airflow
echo "   Ejecutando: airflow db upgrade"
airflow db upgrade

echo "   Ejecutando: airflow db init"
airflow db init

sleep 5

echo "🔗 Creando conexión a la base de datos DBT..."

# Esperar a que Airflow esté completamente inicializado
echo "⏳ Esperando a que Airflow esté listo..."
sleep 10

# Eliminar conexión existente si existe
echo "   Eliminando conexión existente..."
airflow connections delete 'dbt_postgres_instance_raw_data' || echo "   Conexión no existía"

# Crear nueva conexión con valores hardcodeados para evitar problemas de variables
echo "   Creando nueva conexión..."
airflow connections add 'dbt_postgres_instance_raw_data' \
    --conn-type 'postgres' \
    --conn-host 'postgres-dbt' \
    --conn-login 'dbtuser' \
    --conn-password 'pssd' \
    --conn-schema 'dbtdb' \
    --conn-port '5432' \
    --conn-description 'Conexión a la base de datos DBT para datos raw'

# Verificar que la conexión se creó correctamente
echo "✅ Verificando conexión creada..."
if airflow connections get 'dbt_postgres_instance_raw_data'; then
    echo "✅ Conexión creada exitosamente"
else
    echo "❌ Error al crear conexión, reintentando..."
    sleep 5
    airflow connections add 'dbt_postgres_instance_raw_data' \
        --conn-type 'postgres' \
        --conn-host 'postgres-dbt' \
        --conn-login 'dbtuser' \
        --conn-password 'pssd' \
        --conn-schema 'dbtdb' \
        --conn-port '5432' \
        --conn-description 'Conexión a la base de datos DBT para datos raw'
fi

echo "✅ Verificando conexión creada..."
airflow connections list | grep dbt_postgres_instance_raw_data || echo "⚠️ Conexión no encontrada en la lista"

# Verificar que la conexión funciona
echo "🧪 Probando conexión..."
if airflow connections test 'dbt_postgres_instance_raw_data'; then
    echo "✅ Conexión funciona correctamente"
else
    echo "❌ Error en la conexión"
fi

echo "👤 Creando usuario administrador..."
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

echo "🚀 Iniciando servicios de Airflow..."
echo "   - Scheduler: airflow scheduler"
echo "   - Webserver: airflow webserver"

# Iniciar servicios en background
airflow scheduler &
airflow webserver

