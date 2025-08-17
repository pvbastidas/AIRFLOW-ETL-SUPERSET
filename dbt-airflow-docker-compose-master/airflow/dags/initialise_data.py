from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.empty import EmptyOperator  # Nodo de sincronización
from datetime import datetime

# [START default_args]
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
# [END default_args]

# [START instantiate_dag]
load_initial_data_dag = DAG(
    '1_load_initial_data',
    default_args=default_args,
    schedule_interval=None,
)

# Creación de schema base
t1 = PostgresOperator(
    task_id='create_schema',
    sql="CREATE SCHEMA IF NOT EXISTS dbt_raw_data;",
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

# Business types
t2 = PostgresOperator(task_id='drop_table_business_types',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.business_types;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t3 = PostgresOperator(
    task_id='create_business_types',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.business_types (
        initcap VARCHAR(64),
        active BOOLEAN,
        business_type_id INT PRIMARY KEY
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t4 = PostgresOperator(task_id='load_business_types',
                      sql="COPY dbt_raw_data.business_types FROM '/sample_data/business_types_v1.csv' DELIMITER ';' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

# Customers
t5 = PostgresOperator(task_id='drop_table_create_customers',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.customers;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t6 = PostgresOperator(
    task_id='create_customers',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.customers (
        customer_id INT PRIMARY KEY,
        email_address VARCHAR(255),
        name VARCHAR(128),
        business_type_id INT,
        site_code VARCHAR(13),
        archived BOOLEAN,
        is_key_account BOOLEAN,
        date_updated TIMESTAMP,
        date_created TIMESTAMP
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t7 = PostgresOperator(task_id='load_customers',
                      sql="COPY dbt_raw_data.customers FROM '/sample_data/customers_v1.csv' DELIMITER ';' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

# Orders
t8 = PostgresOperator(task_id='drop_table_create_orders',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.orders;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t9 = PostgresOperator(
    task_id='create_orders',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.orders (
        batch_id INT,
        created_date TIMESTAMP,
        updated_date TIMESTAMP,
        submitted_date TIMESTAMP,
        delivery_date DATE,
        customer_id INT,
        order_id INT,
        site_code VARCHAR(18),
        total DECIMAL(12,2),
        total_shipping DECIMAL(12,2),
        tracking_code VARCHAR(64),
        order_status VARCHAR(128),
        gmv_enabled BOOLEAN,
        order_number VARCHAR(128),
        shipping_by_tracking DECIMAL(12,2),
        latitude FLOAT,
        longitude FLOAT
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t10 = PostgresOperator(task_id='load_orders',
                      sql="COPY dbt_raw_data.orders FROM '/sample_data/orders_v1.csv' DELIMITER ';' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

# Currency codes
t11 = PostgresOperator(task_id='drop_table_currency_codes',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.currency_codes;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t12 = PostgresOperator(
    task_id='create_currency_codes',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.currency_codes (
        date_currency TIMESTAMP PRIMARY KEY,
        ars DECIMAL(8,2),
        mxn DECIMAL(8,2),
        cop DECIMAL(8,2),
        brl DECIMAL(8,2),
        blue DECIMAL(8,2)
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t13 = PostgresOperator(task_id='load_currency_codes',
                      sql="COPY dbt_raw_data.currency_codes FROM '/sample_data/historico_monedas.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

# Site codes
t14 = PostgresOperator(task_id='drop_table_site_codes',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.site_codes;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t15 = PostgresOperator(
    task_id='create_site_codes',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.site_codes (
        site_code CHAR(3) PRIMARY KEY,
        city_name VARCHAR(128),
        country_name VARCHAR(128) NULL,
        continent CHAR(2),
        iso_country CHAR(2) NULL
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t16 = PostgresOperator(task_id='load_site_codes',
                      sql="COPY dbt_raw_data.site_codes FROM '/sample_data/iata_codes.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

# Dim Fecha
t17 = PostgresOperator(task_id='drop_table_dim_fecha',
                      sql="DROP TABLE IF EXISTS dbt_raw_data.dim_fecha;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t18 = PostgresOperator(
    task_id='create_dim_fecha',
    sql="""
    CREATE TABLE IF NOT EXISTS dbt_raw_data.dim_fecha (
        fecha_id SERIAL PRIMARY KEY,
        fecha DATE NOT NULL,
        anio SMALLINT NOT NULL,
        mes SMALLINT NOT NULL,
        dia SMALLINT NOT NULL,
        dia_semana SMALLINT NOT NULL,
        nombre_dia_semana VARCHAR(20) NOT NULL,
        nombre_mes VARCHAR(20) NOT NULL,
        trimestre SMALLINT NOT NULL,
        anio_semana SMALLINT NOT NULL,
        es_fin_semana BOOLEAN NOT NULL
    );
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

t19 = PostgresOperator(
    task_id='populate_dim_fecha',
    sql="""
    INSERT INTO dbt_raw_data.dim_fecha (fecha, anio, mes, dia, dia_semana, nombre_dia_semana, nombre_mes, trimestre, anio_semana, es_fin_semana)
    SELECT 
        fecha_series.fecha,
        EXTRACT(YEAR FROM fecha_series.fecha)::SMALLINT AS anio,
        EXTRACT(MONTH FROM fecha_series.fecha)::SMALLINT AS mes,
        EXTRACT(DAY FROM fecha_series.fecha)::SMALLINT AS dia,
        EXTRACT(DOW FROM fecha_series.fecha)::SMALLINT AS dia_semana,
        CASE EXTRACT(DOW FROM fecha_series.fecha)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Lunes'
            WHEN 2 THEN 'Martes'
            WHEN 3 THEN 'Miércoles'
            WHEN 4 THEN 'Jueves'
            WHEN 5 THEN 'Viernes'
            WHEN 6 THEN 'Sábado'
        END AS nombre_dia_semana,
        CASE EXTRACT(MONTH FROM fecha_series.fecha)
            WHEN 1 THEN 'Enero'
            WHEN 2 THEN 'Febrero'
            WHEN 3 THEN 'Marzo'
            WHEN 4 THEN 'Abril'
            WHEN 5 THEN 'Mayo'
            WHEN 6 THEN 'Junio'
            WHEN 7 THEN 'Julio'
            WHEN 8 THEN 'Agosto'
            WHEN 9 THEN 'Septiembre'
            WHEN 10 THEN 'Octubre'
            WHEN 11 THEN 'Noviembre'
            WHEN 12 THEN 'Diciembre'
        END AS nombre_mes,
        EXTRACT(QUARTER FROM fecha_series.fecha)::SMALLINT AS trimestre,
        EXTRACT(WEEK FROM fecha_series.fecha)::SMALLINT AS anio_semana,
        EXTRACT(DOW FROM fecha_series.fecha) IN (5, 6) AS mes_fin_semana
    FROM (
        SELECT generate_series(
            '2020-01-01'::date,
            '2030-12-31'::date,
            '1 day'::interval
        )::date AS fecha
    ) fecha_series;
    """,
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database="dbtdb",
    dag=load_initial_data_dag
)

# Nodo de sincronización para esperar todas las dimensiones
wait_for_dimensions = EmptyOperator(
    task_id='wait_for_all_dimensions',
    dag=load_initial_data_dag
)

# Schema analytics y OBT
t_create_dbt_analytics_schema = PostgresOperator(
    task_id='create_dbt_analytics_schema',
    sql="CREATE SCHEMA IF NOT EXISTS dbt_analytics;",
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database='dbtdb',
    dag=load_initial_data_dag
)

t_obt_create = PostgresOperator(
    task_id='create_and_populate_obt_orders',
    sql=open('/dbt/sql/create_and_populate_obt_orders.sql').read(),
    postgres_conn_id='dbt_postgres_instance_raw_data',
    autocommit=True,
    database='dbtdb',
    dag=load_initial_data_dag
)

# Dependencias
t1 >> t2 >> t3 >> t4
t1 >> t5 >> t6 >> t7
t1 >> t8 >> t9 >> t10
t1 >> t11 >> t12 >> t13
t1 >> t14 >> t15 >> t16
t1 >> t17 >> t18 >> t19

# Join point: todas las cargas deben completarse
[t4, t7, t10, t13, t16, t19] >> wait_for_dimensions

# Una vez listas todas, crear schema analytics y OBT
wait_for_dimensions >> t_create_dbt_analytics_schema >> t_obt_create
