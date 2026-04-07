/**
 * Weperty Auth Utility (v5.0.0)
 * Centralized session and authentication modal management.
 */

const AUTH_MODAL_HTML = `
<div id="auth-modal">
    <div class="auth-card">
        <div class="auth-close" onclick="Auth.hideModal()">&times;</div>
        <h1 class="auth-title" data-i18n="auth.title">Register/Sign In</h1>
        
        <div class="auth-illustration">
            <svg width="200" height="150" viewBox="0 0 200 150" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 20L30 80H170L100 20Z" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
                <rect x="50" y="80" width="100" height="60" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
                <rect x="85" y="105" width="30" height="35" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
                <rect x="65" y="95" width="20" height="20" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
                <rect x="115" y="95" width="20" height="20" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
                <circle cx="20" cy="110" r="15" stroke="black" stroke-width="1.5"/>
                <line x1="20" y1="125" x2="20" y2="140" stroke="black" stroke-width="1.5"/>
                <circle cx="180" cy="110" r="15" stroke="black" stroke-width="1.5"/>
                <line x1="180" y1="125" x2="180" y2="140" stroke="black" stroke-width="1.5"/>
            </svg>
        </div>

        <div class="auth-actions">
            <button class="btn-auth-role" onclick="Auth.handleRole('agent')" data-i18n="auth.role.agent">Agent</button>
            <button class="btn-auth-role" onclick="Auth.handleRole('buyer_seller')" data-i18n="auth.role.buyer_seller">Buyer or Seller</button>
            <button class="btn-auth-role" onclick="Auth.handleRole('other')" data-i18n="auth.role.other">Other</button>
        </div>

        <p class="auth-footer">
            <span data-i18n="auth.footer.main">I accept Weperty</span> 
            <a href="terms.html" data-i18n="auth.footer.terms">Terms of Service</a> & 
            <a href="privacy.html" data-i18n="auth.footer.privacy">Privacy Policy</a>
        </p>
    </div>
</div>
`;

const Auth = {
    sessionKey: 'weperty_session',

    isLoggedIn: function() {
        const session = localStorage.getItem(this.sessionKey);
        if (!session) return false;
        try {
            const data = JSON.parse(session);
            // Optional: check session expiry if needed
            return !!data.user;
        } catch (e) {
            return false;
        }
    },

    getUser: function() {
        const session = localStorage.getItem(this.sessionKey);
        return session ? JSON.parse(session) : null;
    },

    showModal: function() {
        let modal = document.getElementById('auth-modal');
        if (!modal) {
            document.body.insertAdjacentHTML('beforeend', AUTH_MODAL_HTML);
            modal = document.getElementById('auth-modal');
        }

        if (modal) {
            // Ensure translations are applied before showing
            if (typeof updateContent === 'function') updateContent();
            
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        }
    },

    hideModal: function() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
    },

    handleRole: function(role) {
        console.log(`User selected role: ${role}`);
        // Redirect to specific login pages or show a more detailed form
        if (role === 'agent') {
            window.location.href = 'crm/login.html';
        } else {
            // For Buyer/Seller or Other, we might open a dedicated sign-up/sign-in page later
            const msg = (currentLang === 'es' ? 'Próximamente: Registro para ' : 'Coming Soon: Registration for ') + role;
            alert(msg);
        }
    },

    logout: function() {
        localStorage.removeItem(this.sessionKey);
        window.location.reload();
    },

    getInitials: function(name) {
        if (!name) return '??';
        const parts = name.trim().split(' ');
        if (parts.length >= 2) {
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    },

    updateHeader: function() {
        const desktopItem = document.getElementById('nav-auth-item');
        const mobileItem = document.getElementById('nav-auth-item-mob');
        const loggedIn = this.isLoggedIn();

        if (loggedIn) {
            const user = this.getUser();
            const displayName = user.user || 'Admin';
            const initials = this.getInitials(displayName);
            
            // Translations for Menu Items
            const t = {
                es: {
                    overview: 'Resumen',
                    transactions: 'Transacciones',
                    collections: 'Colecciones',
                    searches: 'Búsquedas guardadas',
                    favorites: 'Favoritos',
                    recent: 'Vistos recientemente',
                    buildings: 'Edificios guardados',
                    settings: 'Ajustes de cuenta',
                    notifications: 'Notificaciones',
                    logout: 'Salir'
                },
                en: {
                    overview: 'Overview',
                    transactions: 'Transactions',
                    collections: 'Collections',
                    searches: 'Saved Searches',
                    favorites: 'Favorites',
                    recent: 'Recently Viewed',
                    buildings: 'Saved Buildings',
                    settings: 'Account Settings',
                    notifications: 'Notifications',
                    logout: 'Logout'
                }
            };
            const lang = (typeof currentLang !== 'undefined' && t[currentLang]) ? currentLang : 'es';
            const mt = t[lang];

            // Render Desktop (Premium Dropdown)
            if (desktopItem) {
                desktopItem.style.marginLeft = '25px';
                desktopItem.innerHTML = `
                    <div class="user-menu-wrapper">
                        <div class="user-menu-trigger">
                            <span>${displayName}</span>
                            <div class="user-avatar">${initials}</div>
                        </div>
                        <div class="user-dropdown">
                            <div class="user-dropdown-section">
                                <a href="#">${mt.overview}</a>
                                <a href="#">${mt.transactions}</a>
                                <a href="#">${mt.collections}</a>
                                <a href="#">${mt.searches}</a>
                                <a href="#">${mt.favorites}</a>
                            </div>
                            <div class="user-dropdown-section">
                                <a href="#">${mt.recent}</a>
                                <a href="#">${mt.buildings}</a>
                            </div>
                            <div class="user-dropdown-section">
                                <a href="#">${mt.settings}</a>
                                <a href="#">${mt.notifications}</a>
                            </div>
                            <div class="user-dropdown-section">
                                <a href="javascript:Auth.logout()" class="logout-item">${mt.logout}</a>
                            </div>
                        </div>
                    </div>
                `;
                desktopItem.onclick = null;
            }

            // Render Mobile (Flat list in drawer)
            if (mobileItem) {
                mobileItem.innerHTML = `
                    <div style="border-top:1px solid #eee; margin-top:10px; padding-top:10px;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px; padding:0 5px;">
                            <div class="user-avatar" style="width:40px; height:40px;">${initials}</div>
                            <span style="font-weight:600; font-size:16px;">${displayName}</span>
                        </div>
                        <a href="#" style="font-size:14px; margin-bottom:12px;">${mt.overview}</a>
                        <a href="#" style="font-size:14px; margin-bottom:12px;">${mt.favorites}</a>
                        <a href="#" style="font-size:14px; margin-bottom:12px;">${mt.settings}</a>
                        <a href="javascript:Auth.logout()" style="color:#ef4444; font-size:14px;">${mt.logout}</a>
                    </div>
                `;
                mobileItem.onclick = null;
            }
        }
    }
};

window.Auth = Auth;
