-- TABLAS ESPECÍFICAS PARA EL PROYECTO INMOBILIARIA
-- Usamos el prefijo 'inm_' para organizar los datos

-- 1. Tabla de Municipios y Estadísticas
CREATE TABLE IF NOT EXISTS inm_municipios (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    precio_venta NUMERIC,
    precio_alquiler NUMERIC,
    rentabilidad NUMERIC,
    ratio_recuperacion NUMERIC,
    variacion_1y NUMERIC,
    variacion_5y NUMERIC,
    variacion_10y NUMERIC,
    categoria TEXT,
    latitud NUMERIC,
    longitud NUMERIC,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Propiedades Individuales
CREATE TABLE IF NOT EXISTS inm_propiedades (
    id SERIAL PRIMARY KEY,
    municipio_id INTEGER REFERENCES inm_municipios(id), -- Relación con la tabla principal
    titulo TEXT,
    precio NUMERIC,
    precio_anterior NUMERIC,
    habitaciones INTEGER,
    banos INTEGER,
    superficie NUMERIC,
    zona TEXT,
    url TEXT UNIQUE,
    agente TEXT,
    descripcion TEXT,
    caracteristicas JSONB,
    fecha_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Habilitar RLS para seguridad
ALTER TABLE inm_municipios ENABLE ROW LEVEL SECURITY;
ALTER TABLE inm_propiedades ENABLE ROW LEVEL SECURITY;

-- Políticas de lectura pública para que el Dashboard pueda leer los datos
CREATE POLICY "Lectura pública de municipios" ON inm_municipios FOR SELECT USING (true);
CREATE POLICY "Lectura pública de propiedades" ON inm_propiedades FOR SELECT USING (true);
