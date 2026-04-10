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
        
        window.currentProperty = prop; // Guardar para re-renderizado
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
    
    // Traducción del Tipo de Inmueble
    const tipoNormalizado = (p.tipo || 'Inmueble').toLowerCase().trim();
    const tipoTraducido = translations[currentLang][`type.${tipoNormalizado}`] || p.tipo || 'Inmueble';
    document.getElementById('labelTipo').textContent = tipoTraducido;

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
        
        // Mapeo selectivo de valores comunes (extensible)
        if (lower === "sí" || lower === "si") return currentLang === "es" ? "Sí" : (currentLang === "en" ? "Yes" : (currentLang === "de" ? "Ja" : "Ja"));
        if (lower === "no") return currentLang === "es" ? "No" : (currentLang === "en" ? "No" : (currentLang === "de" ? "Nein" : "Nee"));

        if (lower.includes("piscina")) return translations[currentLang]["feat.pool"];
        if (lower.includes("aire acond")) return translations[currentLang]["feat.ac"];
        if (lower.includes("jardín") || lower.includes("jardin")) return translations[currentLang]["feat.garden"];
        if (lower.includes("terraza")) return translations[currentLang]["feat.terrace"];
        if (lower.includes("ascensor")) return translations[currentLang]["feat.lift"];
        if (lower.includes("garaje") || lower.includes("parking") || lower.includes("aparcamiento")) return translations[currentLang]["feat.parking"];
        if (lower.includes("amueblado")) return translations[currentLang]["feat.furnished"];
        if (lower.includes("exterior")) return translations[currentLang]["feat.exterior"];
        if (lower.includes("interior")) return translations[currentLang]["feat.interior"];
        if (lower.includes("vistas al mar")) return currentLang === "es" ? "Vistas al mar" : (currentLang === "en" ? "Sea views" : (currentLang === "de" ? "Meerblick" : "Zeezicht"));
        if (lower.includes("calefacción")) return currentLang === "es" ? "Calefacción" : (currentLang === "en" ? "Heating" : (currentLang === "de" ? "Heizung" : "Verwarming"));
        
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

    // Agent/Agency Display
    renderAgent(p);
}

function renderAgent(p) {
    const agentNameEl = document.getElementById('agent-name');
    const agencyTitleEl = document.getElementById('agency-title');
    const agencyLogoEl = document.getElementById('agency-logo');
    const agentAvatarEl = document.getElementById('agent-avatar');

    const agentVal = (p.agente || "").toLowerCase().trim();
    console.log("Detectando agente:", agentVal);

    if (agentVal === "weperty properties") {
        if (agentNameEl) agentNameEl.textContent = "Laura López";
        if (agencyTitleEl) agencyTitleEl.textContent = "Agente Weperty Properties";
        if (agencyLogoEl) agencyLogoEl.src = "logos_corporativos/weperty_logo_azul.png";
        if (agentAvatarEl) agentAvatarEl.src = "logos_corporativos/agent_laura_lopez.png";
    } else if (agentVal === "coldwellbanker") {
        if (agentNameEl) agentNameEl.textContent = "Exclusive Advisor";
        if (agencyTitleEl) agencyTitleEl.textContent = "Coldwell Banker España";
        if (agencyLogoEl) {
            agencyLogoEl.src = "logos_corporativos/coldwell_banker_logo.png";
            agencyLogoEl.style.display = 'block';
        }
        // Ocultar avatar o poner uno genérico para Coldwell Banker
        if (agentAvatarEl) agentAvatarEl.src = "logos_corporativos/coldwell_banker_logo.png";
    } else if (p.agente) {
        if (agentNameEl) agentNameEl.textContent = "Agente Inmobiliario";
        if (agencyTitleEl) agencyTitleEl.textContent = p.agente;
        if (agencyLogoEl) agencyLogoEl.style.display = 'none'; 
    }
}

let map;
let currentBaseLayer;
let mapStyles;

function initMap(p) {
    if (!p.latitud || !p.longitud) return;

    map = L.map('propertyMap', { zoomControl: false }).setView([p.latitud, p.longitud], 15);
    L.control.zoom({ position: 'bottomright' }).addTo(map);

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
    const title = currentLang === 'es' ? "Chat Próximamente" : "Chat Coming Soon";
    const msg = currentLang === 'es' ? "Estamos integrando nuestro sistema de chat directo. Estará disponible muy pronto." : "We are integrating our direct chat system. It will be available very soon.";
    showNotice(title, msg);
}

function openContact() {
    const title = currentLang === 'es' ? "Contacto Próximamente" : "Contact Coming Soon";
    const msg = currentLang === 'es' ? "El formulario de contacto directo está en mantenimiento. Por favor, intenta de nuevo en unos días." : "The direct contact form is under maintenance. Please try again in a few days.";
    showNotice(title, msg);
}

function toggleMenu(show) {
    const drawer = document.getElementById('mobileDrawer');
    if (drawer) drawer.classList.toggle('active', show);
}

function revealPhone() {
    const display = document.getElementById('phone-display');
    const tel = window.currentProperty?.caracteristicas?.telefono_agencia || "+34 663 706 497";
    const telLink = tel.replace(/\s+/g, '');
    
    if (display) {
        display.innerHTML = `
            <i class="fa-solid fa-phone" style="width: 14px; color: #888;"></i>
            <a href="tel:${telLink}" style="color: inherit; text-decoration: none; font-weight: 600;">${tel}</a>
        `;
    }
}

function showNotice(title, message) {
    const modal = document.getElementById('notice-modal');
    document.getElementById('notice-title').innerText = title;
    document.getElementById('notice-message').innerText = message;
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function hideNotice() {
    const modal = document.getElementById('notice-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// Cerrar modal al hacer click fuera
window.onclick = function(event) {
    const modal = document.getElementById('notice-modal');
    if (event.target == modal) {
        hideNotice();
    }
}

// Iniciar aplicación
initPropertyDetail();
