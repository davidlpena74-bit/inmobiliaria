-- Inserción de las 25 localidades clave de la Costa Blanca (Alicante)
-- Este script puebla la tabla inm_municipios para dar soporte al buscador y analíticas

INSERT INTO inm_municipios (nombre, categoria, latitud, longitud, zona_madrid)
VALUES 
    ('Jávea / Xàbia', 'Costa Blanca Norte', 38.7892, 0.1662, 'Alicante'),
    ('Dénia', 'Costa Blanca Norte', 38.8408, 0.1061, 'Alicante'),
    ('Benitachell / El Poble Nou de Benitatxell', 'Costa Blanca Norte', 38.7328, 0.1448, 'Alicante'),
    ('Moraira', 'Costa Blanca Norte', 38.6894, 0.1347, 'Alicante'),
    ('Altea', 'Costa Blanca Norte', 38.5992, -0.0514, 'Alicante'),
    ('Pedreguer', 'Costa Blanca Norte', 38.7936, 0.0342, 'Alicante'),
    ('Calpe / Calp', 'Costa Blanca Norte', 38.6447, 0.0445, 'Alicante'),
    ('Benissa', 'Costa Blanca Norte', 38.7188, 0.0505, 'Alicante'),
    ('Teulada', 'Costa Blanca Norte', 38.7291, 0.1033, 'Alicante'),
    ('Finestrat', 'Marina Baixa', 38.5672, -0.2119, 'Alicante'),
    ('Polop', 'Marina Baixa', 38.6222, -0.1278, 'Alicante'),
    ('Alicante / Alacant', 'Capital', 38.3452, -0.4810, 'Alicante'),
    ('Gata de Gorgos', 'Costa Blanca Norte', 38.7731, 0.0863, 'Alicante'),
    ('La Nucia', 'Marina Baixa', 38.6111, -0.1258, 'Alicante'),
    ('Santa Pola', 'Costa Blanca Sur', 38.1917, -0.6022, 'Alicante'),
    ('Xaló', 'Costa Blanca Norte', 38.7408, -0.0117, 'Alicante'),
    ('Benidorm', 'Marina Baixa', 38.5343, -0.1291, 'Alicante'),
    ('El Verger', 'Costa Blanca Norte', 38.8436, -0.0108, 'Alicante'),
    ('L''Alfàs del Pi', 'Marina Baixa', 38.5802, -0.0303, 'Alicante'),
    ('Orba', 'Interior Norte', 38.8189, -0.0639, 'Alicante'),
    ('Torrevieja', 'Costa Blanca Sur', 37.9787, -0.6822, 'Alicante'),
    ('Monforte del Cid', 'Vinalopó Mitjà', 38.3808, -0.7289, 'Alicante'),
    ('Sella', 'Marina Baixa', 38.6089, -0.2722, 'Alicante'),
    ('Benidoleig', 'Costa Blanca Norte', 38.7903, -0.0319, 'Alicante'),
    ('Pego', 'Costa Blanca Norte', 38.8419, -0.1172, 'Alicante')
ON CONFLICT (nombre) DO UPDATE 
SET updated_at = CURRENT_TIMESTAMP;

-- Nota: Se ha usado 'zona_madrid' temporalmente como campo de Agrupación Provincia 
-- para mantener compatibilidad con el esquema actual.
