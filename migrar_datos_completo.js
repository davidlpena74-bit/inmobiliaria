// Script para migrar TODOS los datos a Supabase
const { createClient } = require('@supabase/supabase-js');

const SB_URL = "https://dwbvegnxmyvpolvofkfn.supabase.co";
const SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI";

const supabase = createClient(SB_URL, SB_KEY);

// Todos los datos de distritos y municipios
const todosLosDatos = [
    // MADRID CAPITAL - 21 Distritos
    { nombre: "Salamanca", precio_venta: 9968, precio_alquiler: 27.4, variacion_1y: 10.8, variacion_5y: 67.8, variacion_10y: 115.4, categoria: "Premium", latitud: 40.429, longitud: -3.676 },
    { nombre: "Chamberí", precio_venta: 8873, precio_alquiler: 26.5, variacion_1y: 20.0, variacion_5y: 65.2, variacion_10y: 112.1, categoria: "Premium", latitud: 40.434, longitud: -3.704 },
    { nombre: "Retiro", precio_venta: 7691, precio_alquiler: 23.8, variacion_1y: 14.6, variacion_5y: 62.1, variacion_10y: 108.5, categoria: "Alto", latitud: 40.411, longitud: -3.674 },
    { nombre: "Centro", precio_venta: 7322, precio_alquiler: 27.1, variacion_1y: 8.6, variacion_5y: 58.4, variacion_10y: 105.2, categoria: "Alto", latitud: 40.418, longitud: -3.703 },
    { nombre: "Chamartín", precio_venta: 7000, precio_alquiler: 24.0, variacion_1y: 20.0, variacion_5y: 64.5, variacion_10y: 110.8, categoria: "Alto", latitud: 40.462, longitud: -3.676 },
    { nombre: "Moncloa-Aravaca", precio_venta: 6500, precio_alquiler: 22.0, variacion_1y: 17.3, variacion_5y: 61.2, variacion_10y: 106.4, categoria: "Medio-Alto", latitud: 40.435, longitud: -3.731 },
    { nombre: "Tetuán", precio_venta: 5800, precio_alquiler: 21.0, variacion_1y: 20.0, variacion_5y: 59.8, variacion_10y: 104.2, categoria: "Medio", latitud: 40.459, longitud: -3.704 },
    { nombre: "Arganzuela", precio_venta: 5500, precio_alquiler: 20.5, variacion_1y: 18.2, variacion_5y: 60.5, variacion_10y: 105.1, categoria: "Medio", latitud: 40.398, longitud: -3.696 },
    { nombre: "Hortaleza", precio_venta: 4500, precio_alquiler: 19.0, variacion_1y: 13.6, variacion_5y: 57.2, variacion_10y: 102.4, categoria: "Medio", latitud: 40.470, longitud: -3.642 },
    { nombre: "Ciudad Lineal", precio_venta: 4200, precio_alquiler: 18.5, variacion_1y: 25.2, variacion_5y: 63.8, variacion_10y: 109.1, categoria: "Medio", latitud: 40.444, longitud: -3.652 },
    { nombre: "Fuencarral-El Pardo", precio_venta: 4100, precio_alquiler: 18.2, variacion_1y: 21.6, variacion_5y: 61.5, variacion_10y: 107.4, categoria: "Medio", latitud: 40.498, longitud: -3.731 },
    { nombre: "Moratalaz", precio_venta: 4000, precio_alquiler: 18.0, variacion_1y: 23.9, variacion_5y: 62.2, variacion_10y: 108.3, categoria: "Medio", latitud: 40.407, longitud: -3.645 },
    { nombre: "Latina", precio_venta: 3840, precio_alquiler: 18.0, variacion_1y: 23.3, variacion_5y: 55.4, variacion_10y: 124.2, categoria: "Asequible", latitud: 40.401, longitud: -3.754 },
    { nombre: "Vicálvaro", precio_venta: 3735, precio_alquiler: 16.2, variacion_1y: 22.2, variacion_5y: 52.1, variacion_10y: 127.0, categoria: "Asequible", latitud: 40.395, longitud: -3.585 },
    { nombre: "Carabanchel", precio_venta: 3573, precio_alquiler: 18.1, variacion_1y: 23.0, variacion_5y: 56.4, variacion_10y: 125.1, categoria: "Asequible", latitud: 40.383, longitud: -3.733 },
    { nombre: "San Blas-Canillejas", precio_venta: 3500, precio_alquiler: 17.5, variacion_1y: 20.2, variacion_5y: 54.2, variacion_10y: 122.3, categoria: "Asequible", latitud: 40.441, longitud: -3.606 },
    { nombre: "Usera", precio_venta: 3348, precio_alquiler: 17.0, variacion_1y: 21.2, variacion_5y: 53.5, variacion_10y: 121.1, categoria: "Asequible", latitud: 40.384, longitud: -3.707 },
    { nombre: "Puente de Vallecas", precio_venta: 3287, precio_alquiler: 19.9, variacion_1y: 26.9, variacion_5y: 60.1, variacion_10y: 132.2, categoria: "Asequible", latitud: 40.393, longitud: -3.658 },
    { nombre: "Villa de Vallecas", precio_venta: 3100, precio_alquiler: 17.2, variacion_1y: 20.2, variacion_5y: 54.1, variacion_10y: 120.5, categoria: "Asequible", latitud: 40.375, longitud: -3.615 },
    { nombre: "Barajas", precio_venta: 3000, precio_alquiler: 16.5, variacion_1y: 23.5, variacion_5y: 55.2, variacion_10y: 119.4, categoria: "Económico", latitud: 40.473, longitud: -3.578 },
    { nombre: "Villaverde", precio_venta: 2823, precio_alquiler: 16.1, variacion_1y: 27.9, variacion_5y: 62.5, variacion_10y: 138.4, categoria: "Económico", latitud: 40.350, longitud: -3.700 },

    // COMUNIDAD DE MADRID - Municipios
    { nombre: "Pozuelo de Alarcón", precio_venta: 7204, precio_alquiler: 22.7, variacion_1y: 18.2, variacion_5y: 48.4, variacion_10y: 92.2, categoria: "Premium", latitud: 40.435, longitud: -3.815 },
    { nombre: "Majadahonda", precio_venta: 5112, precio_alquiler: 18.0, variacion_1y: 18.0, variacion_5y: 48.2, variacion_10y: 90.4, categoria: "Premium", latitud: 40.473, longitud: -3.874 },
    { nombre: "Boadilla del Monte", precio_venta: 4368, precio_alquiler: 16.5, variacion_1y: 18.8, variacion_5y: 45.4, variacion_10y: 88.4, categoria: "Alto", latitud: 40.407, longitud: -3.882 },
    { nombre: "Las Rozas de Madrid", precio_venta: 4563, precio_alquiler: 17.2, variacion_1y: 18.5, variacion_5y: 48.5, variacion_10y: 92.1, categoria: "Alto", latitud: 40.492, longitud: -3.874 },
    { nombre: "Alcobendas", precio_venta: 4838, precio_alquiler: 17.8, variacion_1y: 20.1, variacion_5y: 50.2, variacion_10y: 95.2, categoria: "Alto", latitud: 40.533, longitud: -3.633 },
    { nombre: "San Sebastián de los Reyes", precio_venta: 4164, precio_alquiler: 17.4, variacion_1y: 22.0, variacion_5y: 55.1, variacion_10y: 110.4, categoria: "Alto", latitud: 40.547, longitud: -3.626 },
    { nombre: "Tres Cantos", precio_venta: 4210, precio_alquiler: 16.8, variacion_1y: 16.4, variacion_5y: 42.1, variacion_10y: 85.5, categoria: "Alto", latitud: 40.607, longitud: -3.712 },
    { nombre: "Villaviciosa de Odón", precio_venta: 3450, precio_alquiler: 14.5, variacion_1y: 14.2, variacion_5y: 40.1, variacion_10y: 80.2, categoria: "Medio", latitud: 40.358, longitud: -3.901 },
    { nombre: "Torrelodones", precio_venta: 3820, precio_alquiler: 15.2, variacion_1y: 15.1, variacion_5y: 41.5, variacion_10y: 82.4, categoria: "Alto", latitud: 40.576, longitud: -3.929 },
    { nombre: "Rivas-Vaciamadrid", precio_venta: 3120, precio_alquiler: 13.8, variacion_1y: 19.4, variacion_5y: 52.1, variacion_10y: 104.2, categoria: "Medio", latitud: 40.341, longitud: -3.518 },
    { nombre: "Alcorcón", precio_venta: 3158, precio_alquiler: 14.4, variacion_1y: 21.1, variacion_5y: 54.2, variacion_10y: 108.5, categoria: "Medio", latitud: 40.345, longitud: -3.824 },
    { nombre: "Getafe", precio_venta: 3078, precio_alquiler: 14.1, variacion_1y: 19.2, variacion_5y: 51.7, variacion_10y: 98.2, categoria: "Medio", latitud: 40.308, longitud: -3.730 },
    { nombre: "Leganés", precio_venta: 3035, precio_alquiler: 13.8, variacion_1y: 17.8, variacion_5y: 50.1, variacion_10y: 100.2, categoria: "Medio", latitud: 40.327, longitud: -3.763 },
    { nombre: "Móstoles", precio_venta: 2797, precio_alquiler: 13.2, variacion_1y: 23.7, variacion_5y: 55.4, variacion_10y: 110.2, categoria: "Medio", latitud: 40.323, longitud: -3.864 },
    { nombre: "Torrejón de Ardoz", precio_venta: 2768, precio_alquiler: 14.3, variacion_1y: 17.4, variacion_5y: 48.6, variacion_10y: 95.8, categoria: "Medio", latitud: 40.457, longitud: -3.488 },
    { nombre: "Alcalá de Henares", precio_venta: 2764, precio_alquiler: 13.5, variacion_1y: 23.2, variacion_5y: 52.4, variacion_10y: 105.1, categoria: "Medio", latitud: 40.481, longitud: -3.364 },
    { nombre: "Fuenlabrada", precio_venta: 2746, precio_alquiler: 12.8, variacion_1y: 22.7, variacion_5y: 53.6, variacion_10y: 102.1, categoria: "Medio", latitud: 40.284, longitud: -3.793 },
    { nombre: "Pinto", precio_venta: 2580, precio_alquiler: 12.5, variacion_1y: 16.8, variacion_5y: 48.1, variacion_10y: 94.2, categoria: "Asequible", latitud: 40.242, longitud: -3.702 },
    { nombre: "Valdemoro", precio_venta: 2470, precio_alquiler: 11.8, variacion_1y: 17.2, variacion_5y: 49.5, variacion_10y: 98.4, categoria: "Asequible", latitud: 40.191, longitud: -3.677 },
    { nombre: "Parla", precio_venta: 2193, precio_alquiler: 11.5, variacion_1y: 21.6, variacion_5y: 49.3, variacion_10y: 90.5, categoria: "Económico", latitud: 40.237, longitud: -3.774 },
    { nombre: "Arganda del Rey", precio_venta: 2280, precio_alquiler: 11.2, variacion_1y: 15.4, variacion_5y: 44.2, variacion_10y: 88.1, categoria: "Económico", latitud: 40.301, longitud: -3.438 },
    { nombre: "Aranjuez", precio_venta: 2050, precio_alquiler: 10.8, variacion_1y: 12.8, variacion_5y: 39.4, variacion_10y: 78.2, categoria: "Económico", latitud: 40.033, longitud: -3.604 },
    { nombre: "Colmenar Viejo", precio_venta: 2890, precio_alquiler: 12.4, variacion_1y: 16.2, variacion_5y: 44.5, variacion_10y: 89.1, categoria: "Medio", latitud: 40.658, longitud: -3.766 },
    { nombre: "San Fernando de Henares", precio_venta: 2650, precio_alquiler: 12.2, variacion_1y: 14.8, variacion_5y: 42.1, variacion_10y: 84.4, categoria: "Asequible", latitud: 40.424, longitud: -3.535 },
    { nombre: "Coslada", precio_venta: 3010, precio_alquiler: 13.5, variacion_1y: 18.2, variacion_5y: 48.6, variacion_10y: 92.1, categoria: "Medio", latitud: 40.426, longitud: -3.565 },
    { nombre: "Arroyomolinos", precio_venta: 2441, precio_alquiler: 11.5, variacion_1y: 12.4, variacion_5y: 40.1, variacion_10y: 82.3, categoria: "Asequible", latitud: 40.268, longitud: -3.918 },
    { nombre: "Brunete", precio_venta: 2491, precio_alquiler: 10.8, variacion_1y: 11.8, variacion_5y: 38.2, variacion_10y: 78.4, categoria: "Asequible", latitud: 40.403, longitud: -3.998 },
    { nombre: "Ciempozuelos", precio_venta: 1998, precio_alquiler: 9.2, variacion_1y: 10.2, variacion_5y: 34.1, variacion_10y: 72.1, categoria: "Económico", latitud: 40.124, longitud: -3.619 },
    { nombre: "Navalcarnero", precio_venta: 2680, precio_alquiler: 11.2, variacion_1y: 14.2, variacion_5y: 42.1, variacion_10y: 85.5, categoria: "Asequible", latitud: 40.288, longitud: -4.013 },
    { nombre: "Collado Villalba", precio_venta: 2816, precio_alquiler: 11.8, variacion_1y: 15.1, variacion_5y: 43.5, variacion_10y: 88.2, categoria: "Medio", latitud: 40.638, longitud: -4.011 },
    { nombre: "San Agustín del Guadalix", precio_venta: 3150, precio_alquiler: 13.2, variacion_1y: 16.4, variacion_5y: 46.2, variacion_10y: 92.1, categoria: "Medio", latitud: 40.678, longitud: -3.618 },
    { nombre: "Algete", precio_venta: 2550, precio_alquiler: 10.5, variacion_1y: 12.1, variacion_5y: 38.4, variacion_10y: 78.2, categoria: "Asequible", latitud: 40.598, longitud: -3.501 },
    { nombre: "Galapagar", precio_venta: 2650, precio_alquiler: 11.4, variacion_1y: 13.4, variacion_5y: 40.2, variacion_10y: 82.2, categoria: "Asequible", latitud: 40.578, longitud: -4.001 },
    { nombre: "Villanueva de la Cañada", precio_venta: 3650, precio_alquiler: 15.2, variacion_1y: 18.2, variacion_5y: 52.1, variacion_10y: 105.4, categoria: "Alto", latitud: 40.448, longitud: -4.001 },
    { nombre: "San Lorenzo de El Escorial", precio_venta: 3050, precio_alquiler: 12.8, variacion_1y: 15.4, variacion_5y: 45.1, variacion_10y: 90.2, categoria: "Medio", latitud: 40.598, longitud: -4.148 },
    { nombre: "Buitrago del Lozoya", precio_venta: 1850, precio_alquiler: 8.5, variacion_1y: 9.1, variacion_5y: 30.2, variacion_10y: 65.4, categoria: "Económico", latitud: 40.992, longitud: -3.638 },
    { nombre: "Paracuellos de Jarama", precio_venta: 2950, precio_alquiler: 12.5, variacion_1y: 14.8, variacion_5y: 44.5, variacion_10y: 89.4, categoria: "Medio", latitud: 40.505, longitud: -3.528 },
    { nombre: "Humanes de Madrid", precio_venta: 2150, precio_alquiler: 10.2, variacion_1y: 18.2, variacion_5y: 46.1, variacion_10y: 95.5, categoria: "Económico", latitud: 40.252, longitud: -3.828 },
    { nombre: "San Martín de la Vega", precio_venta: 1750, precio_alquiler: 8.8, variacion_1y: 16.4, variacion_5y: 42.1, variacion_10y: 85.5, categoria: "Económico", latitud: 40.208, longitud: -3.571 },
    { nombre: "Griñón", precio_venta: 2350, precio_alquiler: 10.5, variacion_1y: 14.2, variacion_5y: 41.5, variacion_10y: 82.4, categoria: "Económico", latitud: 40.213, longitud: -3.852 },
    { nombre: "Villa del Prado", precio_venta: 1450, precio_alquiler: 7.5, variacion_1y: 10.5, variacion_5y: 34.2, variacion_10y: 70.1, categoria: "Económico", latitud: 40.278, longitud: -4.301 },
    { nombre: "Manzanares el Real", precio_venta: 2750, precio_alquiler: 11.8, variacion_1y: 14.1, variacion_5y: 42.1, variacion_10y: 85.4, categoria: "Medio", latitud: 40.728, longitud: -3.861 },
    { nombre: "Daganzo de Arriba", precio_venta: 2350, precio_alquiler: 10.2, variacion_1y: 12.4, variacion_5y: 38.1, variacion_10y: 78.4, categoria: "Económico", latitud: 40.545, longitud: -3.458 },
    { nombre: "Meco", precio_venta: 2150, precio_alquiler: 9.5, variacion_1y: 11.1, variacion_5y: 35.2, variacion_10y: 72.1, categoria: "Económico", latitud: 40.552, longitud: -3.328 },
    { nombre: "Torrelaguna", precio_venta: 1850, precio_alquiler: 8.4, variacion_1y: 9.4, variacion_5y: 32.1, variacion_10y: 68.4, categoria: "Económico", latitud: 40.826, longitud: -3.538 },
    { nombre: "Campo Real", precio_venta: 1821, precio_alquiler: 8.2, variacion_1y: 8.8, variacion_5y: 30.4, variacion_10y: 64.2, categoria: "Económico", latitud: 40.338, longitud: -3.382 }
];

async function migrarDatos() {
    console.log('🚀 Iniciando migración de datos a Supabase...');
    console.log(`📊 Total de municipios a migrar: ${todosLosDatos.length}`);

    let exitosos = 0;
    let errores = 0;

    for (const dato of todosLosDatos) {
        // Calcular rentabilidad y ratio
        const rentabilidad = ((dato.precio_alquiler * 12) / dato.precio_venta * 100).toFixed(2);
        const ratio_recuperacion = (dato.precio_venta / (dato.precio_alquiler * 12)).toFixed(1);

        const registro = {
            nombre: dato.nombre,
            precio_venta: dato.precio_venta,
            precio_alquiler: dato.precio_alquiler,
            rentabilidad: parseFloat(rentabilidad),
            ratio_recuperacion: parseFloat(ratio_recuperacion),
            variacion_1y: dato.variacion_1y,
            variacion_5y: dato.variacion_5y,
            variacion_10y: dato.variacion_10y,
            categoria: dato.categoria,
            latitud: dato.latitud,
            longitud: dato.longitud
        };

        try {
            const { data, error } = await supabase
                .from('inm_municipios')
                .upsert(registro, { onConflict: 'nombre' });

            if (error) throw error;
            exitosos++;
            console.log(`✅ ${dato.nombre}`);
        } catch (error) {
            errores++;
            console.error(`❌ Error en ${dato.nombre}:`, error.message);
        }
    }

    console.log('\n📈 Resumen de la migración:');
    console.log(`✅ Exitosos: ${exitosos}`);
    console.log(`❌ Errores: ${errores}`);
    console.log(`📊 Total: ${todosLosDatos.length}`);
}

migrarDatos().then(() => {
    console.log('\n🎉 Migración completada!');
    process.exit(0);
}).catch(err => {
    console.error('\n💥 Error fatal:', err);
    process.exit(1);
});
