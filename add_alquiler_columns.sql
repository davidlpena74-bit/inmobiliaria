-- Agregar columnas de variación de alquiler a la tabla inm_municipios
ALTER TABLE public.inm_municipios 
ADD COLUMN IF NOT EXISTS variacion_alquiler_1y NUMERIC,
ADD COLUMN IF NOT EXISTS variacion_alquiler_5y NUMERIC,
ADD COLUMN IF NOT EXISTS variacion_alquiler_10y NUMERIC;

-- Comentarios para documentar las nuevas columnas
COMMENT ON COLUMN public.inm_municipios.variacion_alquiler_1y IS 'Variación porcentual del precio de alquiler en 1 año';
COMMENT ON COLUMN public.inm_municipios.variacion_alquiler_5y IS 'Variación porcentual del precio de alquiler en 5 años';
COMMENT ON COLUMN public.inm_municipios.variacion_alquiler_10y IS 'Variación porcentual del precio de alquiler en 10 años';
