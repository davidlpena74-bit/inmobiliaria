/** 🍪 Weperty Cookies Engine v3.0.0 (GDPR Compliant) */
function initCookieBanner() {
    const bannerHTML = `
        <div id="weperty-cookie-banner" class="cookie-banner active">
            <div class="cookie-content">
                <h3 class="cookie-title">Tu experiencia personalizada</h3>
                <p class="cookie-text">
                    En Weperty utilizamos cookies propias y de terceros para asegurar que disfrutas de la mejor experiencia de búsqueda en Alicante. Al continuar navegando, aceptas nuestra <a href="privacidad.html">Política de Cookies</a> y permites que personalicemos tus resultados de mercado.
                </p>
            </div>
            <div class="cookie-btns">
                <button id="weperty-cookie-settings" class="btn-cookie btn-settings">Configurar</button>
                <button id="weperty-cookie-accept" class="btn-cookie btn-accept">Aceptar todas</button>
            </div>
        </div>
    `;

    // Solo mostrar si no hay consentimiento previo
    if (!localStorage.getItem('weperty_cookies_consent')) {
        document.body.insertAdjacentHTML('beforeend', bannerHTML);
        document.getElementById('weperty-cookie-accept').addEventListener('click', acceptCookies);
        const banner = document.getElementById('weperty-cookie-banner');
        setTimeout(() => banner.style.display = 'flex', 100);
    }
}

function acceptCookies() {
    localStorage.setItem('weperty_cookies_consent', 'true');
    const banner = document.getElementById('weperty-cookie-banner');
    banner.classList.remove('active');
    setTimeout(() => banner.remove(), 800);
}

// Inyectar CSS si no existe
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'css/cookies.css';
document.head.appendChild(link);

window.addEventListener('load', initCookieBanner);
