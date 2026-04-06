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
    const extras = p.caracteristicas?.Extras || [];
    
    // Añadimos extras técnicos primero
    if (p.caracteristicas?.['Interior/exterior']) addExtra(p.caracteristicas['Interior/exterior']);
    if (p.caracteristicas?.['Amueblado']) addExtra("Amueblado: " + p.caracteristicas['Amueblado']);

    extras.forEach(ex => addExtra(ex));

    function addExtra(text) {
        const item = document.createElement('div');
        item.className = 'extra-item';
        item.innerHTML = `<i class="fa-solid fa-check" style="color:var(--primary-color)"></i> ${text}`;
        extrasGrid.appendChild(item);
    }

    // Mapa
    if (p.latitud && p.longitud) {
        const map = L.map('propertyMap').setView([p.latitud, p.longitud], 15);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CARTO'
        }).addTo(map);
        L.marker([p.latitud, p.longitud]).addTo(map);
    }
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

// Iniciar aplicación
initPropertyDetail();
