/**
 * Agente de Precios Inmobiliarios - Comunidad de Madrid
 * Versión Node.js
 */

const { createClient } = require('@supabase/supabase-js');
const axios = require('axios');
const cheerio = require('cheerio');

// Configuración de Supabase
const SB_URL = "https://dwbvegnxmyvpolvofkfn.supabase.co";
const SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI";

const supabase = createClient(SB_URL, SB_KEY);

// Lista de municipios prioritarios para completar
const MUNICIPIOS_PRIORITARIOS = [
    "Alcobendas", "San-Sebastian-de-los-Reyes", "Tres-Cantos",
    "Pozuelo-de-Alarcon", "Majadahonda", "Las-Rozas-de-Madrid",
    "Boadilla-del-Monte", "Villanueva-de-la-Cañada", "Torrelodones",
    "Alcorcon", "Getafe", "Leganes", "Mostoles", "Fuenlabrada",
    "Pinto", "Valdemoro", "Parla", "Rivas-Vaciamadrid",
    "Torrejon-de-Ardoz", "Alcala-de-Henares", "Coslada",
    "San-Fernando-de-Henares", "Arganda-del-Rey", "Colmenar-Viejo",
    "Galapagar", "Collado-Villalba", "Navalcarnero", "Arroyomolinos"
];

class AgentePrecios {
    constructor() {
        this.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9'
        };
        this.resultados = [];
    }

    async buscarPrecioIdealista(municipio) {
        try {
            const municipioUrl = municipio.toLowerCase().replace(/\s+/g, '-');
            const url = `https://www.idealista.com/venta-viviendas/${municipioUrl}-madrid/`;

            console.log(`🔍 Buscando: ${municipio}`);

            const response = await axios.get(url, {
                headers: this.headers,
                timeout: 10000
            });

            const $ = cheerio.load(response.data);

            // Intentar extraer precio medio
            let precioVenta = null;

            // Buscar en diferentes selectores
            const selectores = [
                '.avg-price',
                '.price-tag',
                '[data-test="price-average"]',
                '.item-price'
            ];

            for (const selector of selectores) {
                const elemento = $(selector).first();
                if (elemento.length) {
                    const texto = elemento.text();
                    const numeros = texto.match(/[\d.]+/g);
                    if (numeros && numeros.length > 0) {
                        precioVenta = parseFloat(numeros.join('').replace('.', ''));
                        break;
                    }
                }
            }

            // Si no encontramos precio medio, buscar en los anuncios
            if (!precioVenta) {
                const precios = [];
                $('.item-price').each((i, elem) => {
                    const texto = $(elem).text();
                    const numeros = texto.match(/[\d.]+/g);
                    if (numeros) {
                        const precio = parseFloat(numeros.join('').replace('.', ''));
                        if (precio > 500 && precio < 20000) { // Filtro de precios razonables por m²
                            precios.push(precio);
                        }
                    }
                });

                if (precios.length > 0) {
                    precioVenta = Math.round(precios.reduce((a, b) => a + b, 0) / precios.length);
                }
            }

            if (precioVenta) {
                console.log(`✅ ${municipio}: ${precioVenta} €/m²`);
                return { municipio, precio_venta: precioVenta, fuente: 'Idealista' };
            } else {
                console.log(`⚠️  ${municipio}: No se encontró precio`);
                return null;
            }

        } catch (error) {
            console.log(`❌ ${municipio}: Error - ${error.message}`);
            return null;
        }
    }

    async procesarMunicipio(municipio) {
        const resultado = await this.buscarPrecioIdealista(municipio);

        if (resultado) {
            // Estimar precio de alquiler (aproximadamente 0.35-0.45% del precio de venta mensual)
            const precioAlquiler = Math.round((resultado.precio_venta * 0.004) * 10) / 10;
            const rentabilidad = ((precioAlquiler * 12) / resultado.precio_venta * 100).toFixed(2);
            const ratioRecuperacion = (resultado.precio_venta / (precioAlquiler * 12)).toFixed(1);

            const datos = {
                nombre: municipio.replace(/-/g, ' '),
                precio_venta: resultado.precio_venta,
                precio_alquiler: precioAlquiler,
                rentabilidad: parseFloat(rentabilidad),
                ratio_recuperacion: parseFloat(ratioRecuperacion),
                updated_at: new Date().toISOString()
            };

            // Guardar en Supabase
            await this.guardarEnSupabase(datos);

            this.resultados.push(datos);
        }

        // Pausa para no saturar el servidor
        await this.sleep(3000 + Math.random() * 2000);
    }

    async guardarEnSupabase(datos) {
        try {
            const { data, error } = await supabase
                .from('inm_municipios')
                .upsert(datos, { onConflict: 'nombre' });

            if (error) throw error;
            console.log(`💾 Guardado en Supabase: ${datos.nombre}`);
        } catch (error) {
            console.error(`❌ Error guardando ${datos.nombre}:`, error.message);
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async ejecutar(limite = null) {
        console.log('🚀 Iniciando Agente de Precios Inmobiliarios');
        console.log('='.repeat(60));

        const municipiosAProcesar = limite
            ? MUNICIPIOS_PRIORITARIOS.slice(0, limite)
            : MUNICIPIOS_PRIORITARIOS;

        console.log(`📊 Municipios a procesar: ${municipiosAProcesar.length}`);
        console.log('');

        for (let i = 0; i < municipiosAProcesar.length; i++) {
            const municipio = municipiosAProcesar[i];
            console.log(`\n[${i + 1}/${municipiosAProcesar.length}] ${municipio}`);
            await this.procesarMunicipio(municipio);
        }

        console.log('\n' + '='.repeat(60));
        console.log('🎉 Búsqueda completada!');
        console.log(`✅ Municipios procesados: ${this.resultados.length}`);
        console.log(`⚠️  Sin datos: ${municipiosAProcesar.length - this.resultados.length}`);
        console.log('='.repeat(60));

        return this.resultados;
    }
}

// Ejecutar el agente
async function main() {
    const agente = new AgentePrecios();

    // Procesar solo 5 municipios como prueba
    // Cambia a null para procesar todos
    const resultados = await agente.ejecutar(5);

    // Guardar resultados en archivo
    const fs = require('fs');
    fs.writeFileSync(
        'resultados_agente.json',
        JSON.stringify(resultados, null, 2),
        'utf-8'
    );

    console.log('\n📄 Resultados guardados en: resultados_agente.json');
}

main().catch(console.error);
