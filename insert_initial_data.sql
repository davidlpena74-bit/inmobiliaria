-- Insertar los 12 distritos iniciales de Madrid Capital
INSERT INTO public.inm_municipios (nombre, precio_venta, precio_alquiler, rentabilidad, ratio_recuperacion, variacion_1y, variacion_5y, variacion_10y, categoria, latitud, longitud) VALUES
('Salamanca', 9968, 27.4, 3.30, 30.3, 10.8, 67.8, 115.4, 'Premium', 40.429, -3.676),
('Chamberí', 8873, 26.5, 3.58, 27.9, 20.0, 65.2, 112.1, 'Premium', 40.434, -3.704),
('Retiro', 7691, 23.8, 3.71, 26.9, 14.6, 62.1, 108.5, 'Alto', 40.411, -3.674),
('Centro', 7322, 27.1, 4.44, 22.5, 8.6, 58.4, 105.2, 'Alto', 40.418, -3.703),
('Chamartín', 7000, 24.0, 4.11, 24.3, 20.0, 64.5, 110.8, 'Alto', 40.462, -3.676),
('Arganzuela', 5500, 20.5, 4.47, 22.4, 18.2, 60.5, 105.1, 'Medio', 40.398, -3.696),
('Ciudad Lineal', 4200, 18.5, 5.29, 18.9, 25.2, 63.8, 109.1, 'Medio', 40.444, -3.652),
('Vicálvaro', 3735, 16.2, 5.20, 19.2, 22.2, 52.1, 127.0, 'Asequible', 40.395, -3.585),
('Puente de Vallecas', 3287, 19.9, 7.26, 13.8, 26.9, 60.1, 132.2, 'Asequible', 40.393, -3.658),
('Usera', 3348, 17.0, 6.09, 16.4, 21.2, 53.5, 121.1, 'Asequible', 40.384, -3.707),
('Villa de Vallecas', 3100, 17.2, 6.66, 15.0, 20.2, 54.1, 120.5, 'Asequible', 40.375, -3.615),
('Villaverde', 2823, 16.1, 6.84, 14.6, 27.9, 62.5, 138.4, 'Económico', 40.350, -3.700)
ON CONFLICT (nombre) DO UPDATE SET
    precio_venta = EXCLUDED.precio_venta,
    precio_alquiler = EXCLUDED.precio_alquiler,
    rentabilidad = EXCLUDED.rentabilidad,
    ratio_recuperacion = EXCLUDED.ratio_recuperacion,
    variacion_1y = EXCLUDED.variacion_1y,
    variacion_5y = EXCLUDED.variacion_5y,
    variacion_10y = EXCLUDED.variacion_10y,
    categoria = EXCLUDED.categoria,
    latitud = EXCLUDED.latitud,
    longitud = EXCLUDED.longitud,
    updated_at = CURRENT_TIMESTAMP;
