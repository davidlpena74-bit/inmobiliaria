-- MIGRACIÓN PARA AGREGAR EL CAMPO TIPO_OPERACION
-- Ejecutar este script en el editor SQL de Supabase

-- 1. Agregar la columna si no existe
ALTER TABLE public.inm_propiedades 
ADD COLUMN IF NOT EXISTS tipo_operacion TEXT CHECK (tipo_operacion IN ('Venta', 'Alquiler')) DEFAULT 'Venta';

-- 2. Poblar datos iniciales basados en el umbral de precio (Heurística)
-- Alquiler < 10.000€, Venta >= 10.000€
UPDATE public.inm_propiedades 
SET tipo_operacion = 'Alquiler' 
WHERE precio < 10000;

UPDATE public.inm_propiedades 
SET tipo_operacion = 'Venta' 
WHERE precio >= 10000;

-- 3. Documentar la columna
COMMENT ON COLUMN public.inm_propiedades.tipo_operacion IS 'Distingue si la propiedad es para Venta o Alquiler';
