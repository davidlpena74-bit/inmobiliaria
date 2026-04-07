/* 
   ========================================
   LÓGICA DETALLE INMUEBLE (Vanilla JS)
   ========================================
*/

const SUPABASE_URL = 'https://dwbvegnxmyvpolvofkfn.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3YnZlZ254bXl2cG9sdm9ma2ZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc1Mzg1NTUsImV4cCI6MjA4MzExNDU1NX0.eT5ZSce8H8Yk8pWKyLUYChU0HtmZljywP4eEQd5FkOI';
const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// 1. Obtener parámetros de la URL
const urlParams = new URLSearchParams(window.location.search);
const propertyRef = urlParams.get('ref');

if (!propertyRef) {
    alert("Referencia de inmueble no especificada.");
    window.location.href = 'inmuebles.html';
}

// 2. Función Principal
async function initPropertyDetail() {
    try {
        const { data: prop, error } = await _supabase
            .from('inm_propiedades')
            .select('*')
            .eq('referencia', propertyRef)
            .single();

        if (error || !prop) throw error || new Error("Inmueble no encontrado");

        renderProperty(prop);
    } catch (err) {
        console.error("Error cargando el inmueble:", err);
        document.body.innerHTML = `<div style="text-align:center; padding: 100px;"><h1>Inmueble no encontrado</h1><p>${err.message}</p><a href="inmuebles.html">Volver al listado</a></div>`;
    }
}

function renderProperty(p) {
    // Títulos y Precios
    const precioS = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(p.precio);
    const tit = t_prop(p, 'titulo');
    document.title = `${tit} | Weperty`;
    document.getElementById('propTitle').textContent = tit;
    document.getElementById('stickyPrice').textContent = precioS;
    document.getElementById('stickyRef').textContent = `Ref: ${p.referencia}`;
    document.getElementById('propLocation').innerHTML = `<i class="fa-solid fa-location-dot"></i> ${p.caracteristicas?.ciudad || 'Alicante'}, ${p.caracteristicas?.provincia || 'Alicante'}`;

    // Badges / Stats
    document.getElementById('labelBeds').textContent = `${p.habitaciones || 0} ${translations[currentLang]['prop.beds']}`;
    document.getElementById('labelBaths').textContent = `${p.banos || 0} ${translations[currentLang]['prop.baths']}`;
    document.getElementById('labelArea').textContent = `${p.superficie || 0} m²`;
    document.getElementById('labelTipo').textContent = p.tipo || 'Inmueble';

    // Descripción
    document.getElementById('propDesc').innerHTML = t_prop(p, 'descripcion') || "Sin descripción disponible.";

    // 🖼️ Galería (Carrusel de 1 imagen)
    const imgs = p.imagenes_url || [];
    if (imgs.length > 0) {
        let currentPhotoIndex = 0;
        const mainPhoto = document.getElementById('photoMain');
        const countDisplay = document.getElementById('photoCounter');
        const btnPrev = document.getElementById('btnPrevImg');
        const btnNext = document.getElementById('btnNextImg');

        const updateCarousel = () => {
            mainPhoto.style.opacity = '0';
            setTimeout(() => {
                mainPhoto.src = imgs[currentPhotoIndex];
                countDisplay.textContent = `${currentPhotoIndex + 1} / ${imgs.length}`;
                mainPhoto.style.opacity = '1';
            }, 300); // pequeña transición
        };

        if (imgs.length > 1) {
            btnPrev.style.display = 'block';
            btnNext.style.display = 'block';
            countDisplay.style.display = 'block';

            btnPrev.onclick = () => {
                currentPhotoIndex = (currentPhotoIndex > 0) ? currentPhotoIndex - 1 : imgs.length - 1;
                updateCarousel();
            };

            btnNext.onclick = () => {
                currentPhotoIndex = (currentPhotoIndex < imgs.length - 1) ? currentPhotoIndex + 1 : 0;
                updateCarousel();
            };
        }
        
        updateCarousel(); // Initialize first state
    }

    // Extras (Características)
    const extrasGrid = document.getElementById('extrasGrid');
    extrasGrid.innerHTML = '';
    
    function translateFeature(text) {
        if (!text) return "";
        const lower = text.toLowerCase().trim();
        
        // Mapeo selectivo de valores comunes
        if (lower === "sí" || lower === "si") return currentLang === "es" ? "Sí" : (currentLang === "en" ? "Yes" : (currentLang === "de" ? "Ja" : "Ja"));
        if (lower === "no") return currentLang === "es" ? "No" : (currentLang === "en" ? "No" : (currentLang === "de" ? "Nein" : "Nee"));

        if (lower.includes("piscina")) return translations[currentLang]["feat.pool"];
        if (lower.includes("aire acond")) return translations[currentLang]["feat.ac"];
        if (lower.includes("jardín") || lower.includes("jardin")) return translations[currentLang]["feat.garden"];
        if (lower.includes("terraza")) return translations[currentLang]["feat.terrace"];
        if (lower.includes("ascensor")) return translations[currentLang]["feat.lift"];
        if (lower.includes("garaje") || lower.includes("parking")) return translations[currentLang]["feat.parking"];
        if (lower.includes("amueblado")) return translations[currentLang]["feat.furnished"];
        if (lower.includes("exterior")) return translations[currentLang]["feat.exterior"];
        if (lower.includes("interior")) return translations[currentLang]["feat.interior"];
        return text; // Fallback
    }

    // Añadimos extras técnicos primero
    if (p.caracteristicas?.['Interior/exterior']) addExtra(translateFeature(p.caracteristicas['Interior/exterior']));
    if (p.caracteristicas?.['Amueblado']) {
        const val = p.caracteristicas['Amueblado'];
        const label = translations[currentLang]["feat.furnished"];
        addExtra(`${label}: ${val}`);
    }

    const extras = p.caracteristicas?.Extras || [];
    extras.forEach(ex => addExtra(translateFeature(ex)));

    function addExtra(text) {
        const item = document.createElement('div');
        item.className = 'extra-item';
        item.innerHTML = `<i class="fa-solid fa-check" style="color:var(--primary-color)"></i> ${text}`;
        extrasGrid.appendChild(item);
    }

    // Mapa
    initMap(p);

    // 🚩 IMPORTANTE: Forzar actualización de etiquetas i18n
    if (typeof updateContent === "function") {
        updateContent();
    }
}

let map;
let currentBaseLayer;
let mapStyles;

function initMap(p) {
    if (!p.latitud || !p.longitud) return;

    map = L.map('propertyMap').setView([p.latitud, p.longitud], 15);

    mapStyles = {
        light: L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CARTO'
        }),
        voyager: L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CARTO'
        }),
        satellite: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: '&copy; ESRI'
        }),
        osm: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        })
    };

    currentBaseLayer = mapStyles.osm;
    currentBaseLayer.addTo(map);

    // Update UI initial state
    document.querySelectorAll('.style-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('style-osm').classList.add('active');

    L.marker([p.latitud, p.longitud]).addTo(map);
}

function setMapStyle(style) {
    if (!map || !mapStyles[style]) return;

    if (map.hasLayer(currentBaseLayer)) {
        map.removeLayer(currentBaseLayer);
    }
    currentBaseLayer = mapStyles[style];
    currentBaseLayer.addTo(map);

    // Actualizar UI del selector
    document.querySelectorAll('.style-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`style-${style}`).classList.add('active');
}


// 🖼️ Lógica de Modal (por si en un futuro se hace click en la imagen para pantalla completa)
function openGallery(images, index) {
    console.log("Abrir galería modal en índice:", index);
}

// 📞 Acciones de Contacto
function openWhatsapp() {
    window.open(`https://wa.me/34654321098?text=Hola, estoy interesado en el inmueble ${propertyRef}`, '_blank');
}

function openContact() {
    alert("Formulario de contacto próximamente.");
}

function toggleMenu(show) {
    const drawer = document.getElementById('mobileDrawer');
    if (drawer) drawer.classList.toggle('active', show);
}

// Iniciar aplicación
initPropertyDetail();
