-- 🏛️ ESQUEMA MAESTRO WEPERTY v2.2.0
-- Entidad Suprema: WEPERTY REAL ESTATE PLATFORM

-- 1. TABLA DE PROPIETARIOS (Módulo CRM Propietarios)
CREATE TABLE IF NOT EXISTS weperty_propietarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT,
    email TEXT UNIQUE,
    telefono TEXT,
    dni_cif TEXT UNIQUE,
    direccion_postal TEXT,
    tipo_propietario TEXT CHECK (tipo_propietario IN ('Particular', 'Inmobiliaria', 'Inversor', 'Banco')),
    notas_internas TEXT,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. ENRIQUECIMIENTO DE TABLA MUNICIPIOS (Inteligencia Geográfica)
ALTER TABLE inm_municipios ADD COLUMN IF NOT EXISTS codigo_postal TEXT;
ALTER TABLE inm_municipios ADD COLUMN IF NOT EXISTS zona_madrid TEXT; -- Norte, Sur, Este, Oeste, Centro, Sierra

-- 3. ACTUALIZACIÓN DE TABLA PROPIEDADES (Relaciones y Mapas)
-- Añadimos relación con propietario y coordenadas para Map Engine
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS propietario_id INTEGER REFERENCES weperty_propietarios(id);
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS latitud NUMERIC;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS longitud NUMERIC;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS estado_publicacion TEXT DEFAULT 'Borrador' CHECK (estado_publicacion IN ('Borrador', 'Activo', 'Vendido', 'Alquilado', 'Pausado'));
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS imagenes_url JSONB; -- Array de URLs de fotos
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS destacada BOOLEAN DEFAULT false;

-- 4. TABLA DE SOLICITUDES / LEADS (Gestión de Demanda)
CREATE TABLE IF NOT EXISTS weperty_solicitudes (
    id SERIAL PRIMARY KEY,
    cliente_nombre TEXT NOT NULL,
    cliente_email TEXT,
    cliente_telefono TEXT,
    propiedad_interes_id INTEGER REFERENCES inm_propiedades(id),
    tipo_operacion TEXT CHECK (tipo_operacion IN ('Compra', 'Alquiler', 'Venta', 'Valoracion')),
    presupuesto_max NUMERIC,
    zona_interes TEXT,
    mensaje_cliente TEXT,
    estado_solicitud TEXT DEFAULT 'Nuevo' CHECK (estado_solicitud IN ('Nuevo', 'Contactado', 'Cita Programada', 'Oferta Enviada', 'Cerrado', 'Descartado')),
    asignado_a TEXT, -- Para agentes de Weperty
    fecha_solicitud TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Habilitar RLS para las nuevas tablas
ALTER TABLE weperty_propietarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE weperty_solicitudes ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad para administración
-- (Ajustar según roles de usuario de Supabase Auth)
CREATE POLICY "Lectura interna propietarios" ON weperty_propietarios FOR ALL USING (true);
CREATE POLICY "Lectura interna solicitudes" ON weperty_solicitudes FOR ALL USING (true);
