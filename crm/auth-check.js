/**
 * auth-check.js - Sistema de Seguridad Weperty CRM
 * Verifica que el usuario esté autenticado antes de mostrar el contenido.
 */

(function () {
    // 1. Evitar entrar en bucle si ya estamos en el login
    const isLoginPage = window.location.pathname.includes('login.html');
    const session = localStorage.getItem('weperty_session');

    if (!session && !isLoginPage) {
        // No hay sesión: Redirigir al inicio público
        window.location.href = '../index.html';
    }

    if (session && isLoginPage) {
        // Ya está logueado pero intenta entrar al login: Redirigir al CRM
        window.location.href = '../crm.html';
    }
})();

/**
 * Función global para cerrar sesión cómodamente desde cualquier parte
 */
function logout() {
    localStorage.removeItem('weperty_session');
    window.location.href = '../index.html';
}
