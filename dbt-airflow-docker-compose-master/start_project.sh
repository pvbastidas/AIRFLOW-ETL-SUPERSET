#!/bin/bash

echo "🚀 Iniciando proyecto DBT + Airflow + Superset"
echo "=============================================="
echo ""

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Inicia Docker Desktop primero."
    exit 1
fi

# Verificar que la red superset-network exista
if ! docker network ls | grep -q "superset-network"; then
    echo "🌐 Creando red superset-network..."
    docker network create superset-network
    echo "✅ Red creada"
else
    echo "✅ Red superset-network ya existe"
fi

# Detener y limpiar contenedores existentes
echo "🧹 Limpiando contenedores existentes..."
docker-compose down -v
docker-compose rm -f

# Limpiar volúmenes de Airflow si existen
echo "🗑️ Limpiando volúmenes de Airflow..."
docker volume prune -f

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "📊 Verificando estado de los servicios..."
docker-compose ps

# Verificar logs de Airflow
echo "📋 Verificando logs de Airflow..."
docker-compose logs airflow | tail -20

echo ""
echo "🎉 Proyecto iniciado!"
echo ""
echo "🌐 URLs de acceso:"
echo "   - Airflow: http://localhost:8000 (admin/admin)"
echo "   - Superset: http://localhost:8088 (admin/admin)"
echo "   - Adminer: http://localhost:8080"
echo ""
echo "📊 Para verificar que todo funciona:"
echo "   1. Ve a Airflow: http://localhost:8000"
echo "   2. Verifica que el DAG '1_load_initial_data' esté activo"
echo "   3. Ejecuta el DAG manualmente"
echo ""
echo "🔧 Si hay problemas, ejecuta:"
echo "   docker-compose logs airflow"
echo "   docker-compose logs postgres-dbt" 