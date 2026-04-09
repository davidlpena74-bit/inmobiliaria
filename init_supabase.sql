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
    variacion_alquiler_1y NUMERIC,
    variacion_alquiler_5y NUMERIC,
    variacion_alquiler_10y NUMERIC,
    categoria TEXT,
    latitud NUMERIC,
    longitud NUMERIC,
    codigo_postal TEXT,
    zona_madrid TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Propiedades Individuales
CREATE TABLE IF NOT EXISTS inm_propiedades (
    id SERIAL PRIMARY KEY,
    municipio_id INTEGER REFERENCES inm_municipios(id),
    referencia TEXT UNIQUE,
    titulo TEXT,
    tipo TEXT, -- 'Apartamento', 'Villa', etc.
    precio NUMERIC,
    precio_anterior NUMERIC,
    habitaciones INTEGER,
    banos INTEGER,
    superficie NUMERIC,
    zona TEXT,
    url TEXT UNIQUE,
    agente TEXT,
    descripcion TEXT,
    caracteristicas JSONB, -- Objeto con detalles técnicos
    imagenes_url JSONB, -- Array de URLs de fotos
    latitud NUMERIC,
    longitud NUMERIC,
    destacada BOOLEAN DEFAULT false,
    estado_publicacion TEXT DEFAULT 'Activo' CHECK (estado_publicacion IN ('Borrador', 'Activo', 'Vendido', 'Alquilado', 'Pausado')),
    tipo_operacion TEXT DEFAULT 'Venta' CHECK (tipo_operacion IN ('Venta', 'Alquiler')),
    origen_datos TEXT DEFAULT 'CRM_WEPERTY' CHECK (origen_datos IN ('CRM_WEPERTY', 'SCRAPER_EXTERNAL')),
    
    -- Controles de publicación
    publicar_web BOOLEAN DEFAULT true,
    publicar_idealista BOOLEAN DEFAULT false,
    publicar_fotocasa BOOLEAN DEFAULT false,
    publicar_pisoscom BOOLEAN DEFAULT false,
    
    -- IDs en portales externos
    id_externo_idealista TEXT,
    id_externo_fotocasa TEXT,
    
    fecha_captura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Habilitar RLS para seguridad
ALTER TABLE inm_municipios ENABLE ROW LEVEL SECURITY;
ALTER TABLE inm_propiedades ENABLE ROW LEVEL SECURITY;

-- Políticas de lectura pública
CREATE POLICY "Lectura pública de municipios" ON inm_municipios FOR SELECT USING (true);
CREATE POLICY "Lectura pública de propiedades" ON inm_propiedades FOR SELECT USING (true);

-- Comentarios técnicos
COMMENT ON COLUMN inm_propiedades.publicar_web IS 'Activa o desactiva la visibilidad en weperty.com';
COMMENT ON COLUMN inm_propiedades.publicar_idealista IS 'Activa la sincronización con el feed de Idealista';
