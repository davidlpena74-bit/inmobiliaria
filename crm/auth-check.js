/**
 * auth-check.js - Sistema de Seguridad Weperty CRM
 * Verifica que el usuario esté autenticado antes de mostrar el contenido.
 */

(function () {
    // 1. Evitar entrar en bucle si ya estamos en el login
    const isLoginPage = window.location.pathname.includes('login.html');
    const session = localStorage.getItem('weperty_session');

    if (!session && !isLoginPage) {
        // No hay sesión: Redirigir al login
        window.location.href = 'login.html';
    }

    if (session && isLoginPage) {
        // Ya está logueado pero intenta entrar al login: Redirigir al inicio
        window.location.href = 'index.html';
    }
})();

/**
 * Función global para cerrar sesión cómodamente desde cualquier parte
 */
function logout() {
    localStorage.removeItem('weperty_session');
    window.location.href = 'login.html';
}
