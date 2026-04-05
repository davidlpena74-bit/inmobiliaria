/* ============================================
   WEPERTY CRM — Lógica de Interfaz (shell.js)
   Manejo de menús desplegables y navegación
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Manejo de menús desplegables en Sidebar
    const navItems = document.querySelectorAll('.s-nav .s-item');
    
    navItems.forEach(item => {
        // Solo añadir funcionalidad si tiene un submenú (s-sub) inmediatamente después
        const nextSub = item.nextElementSibling;
        if (nextSub && nextSub.classList.contains('s-sub')) {
            
            // Si el ítem ya está marcado como activo o tiene un sub-item activo, abrirlo por defecto
            if (item.classList.contains('active') || nextSub.querySelector('a.active')) {
                item.classList.add('open');
            }

            // Manejar el click
            item.addEventListener('click', (e) => {
                // Prevenir navegación si es un dropdown parent
                e.preventDefault();
                item.classList.toggle('open');
            });
        }
    });

    // 2. Hamburguesa (Colapsar Sidebar)
    const hamburger = document.querySelector('.hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            document.body.classList.toggle('collapsed-sidebar');
        });
    }

    // 3. Search Box Focus
    const searchInput = document.querySelector('.topbar .search-box input');
    if (searchInput) {
        searchInput.addEventListener('focus', () => {
            searchInput.parentElement.style.width = '240px';
            searchInput.parentElement.style.transition = '0.3s';
        });
        searchInput.addEventListener('blur', () => {
            searchInput.parentElement.style.width = '180px';
        });
    }
});
