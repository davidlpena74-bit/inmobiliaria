-- 🛠️ ACTUALIZACIÓN OMNICANAL WEPERTY v2.3.0
-- Módulo de Control de Publicación en Redes y Portales

-- Añadir controles de destino a la tabla de inmuebles maestra
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS publicar_web BOOLEAN DEFAULT false;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS publicar_idealista BOOLEAN DEFAULT false;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS publicar_fotocasa BOOLEAN DEFAULT false;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS publicar_pisoscom BOOLEAN DEFAULT false;

-- Campos de sincronización externa (para tracking de IDs en portales)
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS id_externo_idealista TEXT;
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS id_externo_fotocasa TEXT;

-- Etiqueta de Origen Datos (para saber si es del CRM (Propios) o de Scraper (Competencia))
ALTER TABLE inm_propiedades ADD COLUMN IF NOT EXISTS origen_datos TEXT DEFAULT 'CRM_WEPERTY' CHECK (origen_datos IN ('CRM_WEPERTY', 'SCRAPER_EXTERNAL'));

-- Comentarios técnicos para el Agente Sincronizador
COMMENT ON COLUMN inm_propiedades.publicar_web IS 'Activa o desactiva la visibilidad en weperty.com';
COMMENT ON COLUMN inm_propiedades.publicar_idealista IS 'Activa la sincronización con el feed de Idealista';
