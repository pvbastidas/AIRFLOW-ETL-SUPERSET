CREATE TABLE IF NOT EXISTS dbt_analytics.obt_orders (
    order_id INT PRIMARY KEY,
    order_date DATE,

    delivery_date DATE,
    delivery_day_of_week VARCHAR(16),
    delivery_month VARCHAR(16),
    delivery_quarter INT,
    
    customer_id INT,
    customer_name VARCHAR(128),
    email_address VARCHAR(255),
    business_type_id INT,
    business_type_name VARCHAR(64),
    is_key_account BOOLEAN,
    customer_archived BOOLEAN,

    site_code CHAR(3),
    city_name VARCHAR(128),
    country_name VARCHAR(128),
    continent CHAR(2),

    order_status VARCHAR(128),
    total DECIMAL(12,2),
    total_shipping DECIMAL(12,2),
    currency_ars DECIMAL(8,2),
    currency_mxn DECIMAL(8,2),
    currency_cop DECIMAL(8,2),
    currency_brl DECIMAL(8,2),

    tracking_code VARCHAR(64),
    gmv_enabled BOOLEAN,
    order_number VARCHAR(128),
    shipping_by_tracking DECIMAL(12,2),

    latitude FLOAT,
    longitude FLOAT
);

INSERT INTO dbt_analytics.obt_orders (
    order_id, order_date, delivery_date, delivery_day_of_week, delivery_month, delivery_quarter,
    customer_id, customer_name, email_address, business_type_id, business_type_name,
    is_key_account, customer_archived,
    site_code, city_name, country_name, continent,
    order_status, total, total_shipping, currency_ars, currency_mxn, currency_cop, currency_brl,
    tracking_code, gmv_enabled, order_number, shipping_by_tracking,
    latitude, longitude
)
SELECT
    o.order_id,
    o.submitted_date::date AS order_date,

    o.delivery_date,
    df_delivery.nombre_dia_semana,
    df_delivery.nombre_mes,
    df_delivery.trimestre,

    c.customer_id,
    c.name,
    c.email_address,
    c.business_type_id,
    bt.initcap AS business_type_name,
    c.is_key_account,
    c.archived,

    LEFT(o.site_code, 3),
    sc.city_name,
    sc.country_name,
    sc.continent,

    o.order_status,
    o.total,
    o.total_shipping,
    cc.ars,
    cc.mxn,
    cc.cop,
    cc.brl,

    o.tracking_code,
    o.gmv_enabled,
    o.order_number,
    o.shipping_by_tracking,
    o.latitude,
    o.longitude
FROM dbt_raw_data.orders o
LEFT JOIN dbt_raw_data.customers c ON o.customer_id = c.customer_id
LEFT JOIN dbt_raw_data.business_types bt ON c.business_type_id = bt.business_type_id
LEFT JOIN dbt_raw_data.site_codes sc ON LEFT(o.site_code, 3) = sc.site_code
LEFT JOIN dbt_raw_data.currency_codes cc ON DATE(o.created_date) = cc.date_currency
LEFT JOIN dbt_raw_data.dim_fecha df_delivery ON df_delivery.fecha = o.delivery_date
WHERE o.order_status = 'SUBMITTED'
and o.gmv_enabled is true
ON CONFLICT (order_id) DO NOTHING;
