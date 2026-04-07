/**
 * Weperty Auth Utility (v5.0.0)
 * Centralized session and authentication modal management.
 */

const AUTH_MODAL_HTML = `
<div id="auth-modal">
    <div class="auth-card">
        <div class="auth-close" onclick="Auth.hideModal()">&times;</div>
        
        <img src="logos_corporativos/weperty_logo.png" alt="Weperty" class="auth-logo">
        
        <h1 class="auth-title" data-i18n="auth.title">Bienvenido a Weperty</h1>
        <p class="auth-subtitle" data-i18n="auth.subtitle">Tu portal inmobiliario de confianza.</p>
        
        <div id="auth-step-container">
            <!-- Dynamic content will be injected here -->
            <div class="auth-field-group">
                <i class="fa-solid fa-envelope"></i>
                <input type="email" id="auth-email-input" class="auth-input" placeholder="nombre@ejemplo.com" data-i18n-placeholder="auth.placeholder.email">
            </div>

            <button class="btn-auth-continue" onclick="Auth.handleContinue()">
                <span data-i18n="auth.btn.continue">Continuar</span>
                <i class="fa-solid fa-arrow-right"></i>
            </button>
            
            <div class="auth-divider">
                <span data-i18n="auth.divider">También puedes</span>
            </div>

            <div class="auth-google-btn" onclick="Auth.handleGoogleLogin()">
                <div class="google-avatar">D</div>
                <div class="google-content">
                    <div class="google-text">Continuar como David</div>
                    <div class="google-email">davidlpena74@gmail.com</div>
                </div>
                <img src="https://www.gstatic.com/images/branding/product/2x/googleg_48dp.png" alt="Google" class="google-logo">
            </div>
        </div>

        <p class="auth-footer">
            <span data-i18n="auth.footer.main">Al continuar, aceptas</span> 
            <a href="terms.html" data-i18n="auth.footer.terms">Términos</a> y 
            <a href="privacy.html" data-i18n="auth.footer.privacy">Privacidad</a>
        </p>
    </div>
</div>
`;

const Auth = {
    sessionKey: 'weperty_session',
    currentStep: 'email',
    userEmail: '',

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

    showAgentModal: function() {
        const session = this.getUser();
        if (session && session.role === 'admin') {
            window.location.href = 'crm.html';
            return;
        }

        const modal = document.getElementById('auth-modal');
        if (!modal) {
            const div = document.createElement('div');
            div.innerHTML = AUTH_MODAL_HTML;
            document.body.appendChild(div);
            if (typeof updateContent === 'function') updateContent();
        }
        this.renderStep('agent_login');
        document.getElementById('auth-modal').style.display = 'flex';
        document.body.style.overflow = 'hidden';
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
            this.currentStep = 'email';
            this.userEmail = '';
            this.renderStep('email');
            
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; 
        }
    },

    renderStep: function(step) {
        const container = document.getElementById('auth-step-container');
        if (!container) return;

        this.currentStep = step;
        let html = '';

        if (step === 'email') {
            html = `
                <div class="auth-field-group">
                    <i class="fa-solid fa-envelope"></i>
                    <input type="email" id="auth-email-input" class="auth-input" placeholder="nombre@ejemplo.com" value="${this.userEmail}" data-i18n-placeholder="auth.placeholder.email">
                </div>
                <button class="btn-auth-continue" onclick="Auth.handleContinue()">
                    <span data-i18n="auth.btn.continue">Continuar</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
                <div class="auth-divider"><span data-i18n="auth.divider">También puedes</span></div>
                <div class="auth-google-btn" onclick="Auth.handleGoogleLogin()">
                    <div class="google-avatar">D</div>
                    <div class="google-content">
                        <div class="google-text">Continuar como David</div>
                        <div class="google-email">davidlpena74@gmail.com</div>
                    </div>
                    <img src="https://www.gstatic.com/images/branding/product/2x/googleg_48dp.png" alt="Google" class="google-logo">
                </div>
            `;
        } else if (step === 'login') {
            html = `
                <div class="auth-back" onclick="Auth.renderStep('email')" style="position: absolute; left: 10px; top: -45px; cursor: pointer; color: #94a3b8;"><i class="fa-solid fa-arrow-left"></i></div>
                <div class="auth-field-group">
                    <i class="fa-solid fa-envelope"></i>
                    <input type="email" class="auth-input" value="${this.userEmail}" disabled style="opacity: 0.7; background: #f8fafc;">
                </div>
                <div class="auth-field-group">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" id="auth-password-input" class="auth-input" placeholder="••••••••" data-i18n-placeholder="auth.placeholder.password">
                </div>
                <button class="btn-auth-continue" onclick="Auth.handleLogin()">
                    <span data-i18n="auth.btn.login">Iniciar Sesión</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            `;
        } else if (step === 'register') {
            html = `
                <div class="auth-back" onclick="Auth.renderStep('email')" style="position: absolute; left: 10px; top: -45px; cursor: pointer; color: #94a3b8;"><i class="fa-solid fa-arrow-left"></i></div>
                <div class="auth-field-group">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" id="auth-new-password" class="auth-input" placeholder="Crea tu contraseña" data-i18n-placeholder="auth.placeholder.create_pass">
                </div>
                <div class="auth-field-group">
                    <i class="fa-solid fa-shield-check"></i>
                    <input type="password" id="auth-confirm-password" class="auth-input" placeholder="Confirma tu contraseña" data-i18n-placeholder="auth.placeholder.confirm_pass">
                </div>
                <button class="btn-auth-continue" onclick="Auth.handleRegister()">
                    <span data-i18n="auth.btn.register">Crear Cuenta</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            `;
        } else if (step === 'agent_login') {
            html = `
                <div class="auth-field-group">
                    <i class="fa-solid fa-user"></i>
                    <input type="text" id="agent-username" class="auth-input" placeholder="Nombre de usuario" required>
                </div>
                <div class="auth-field-group">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" id="agent-password" class="auth-input" placeholder="Contraseña" required>
                </div>
                <button class="btn-auth-continue" id="agentLoginBtn" onclick="Auth.handleAgentLogin()">
                    <span>Acceder al panel</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
                <div id="agentErrorMsg" class="auth-error" style="color: #ef4444; background: #fee2e2; padding: 10px; border-radius: 8px; font-size: 13px; margin-top: 15px; display: none;"></div>
            `;
        }

        container.innerHTML = html;
        if (typeof updateContent === 'function') updateContent();
    },

    hideModal: function() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
    },

    handleContinue: function() {
        const emailInput = document.getElementById('auth-email-input');
        const email = emailInput ? emailInput.value : '';
        
        if (!email || !email.includes('@')) {
            alert('Por favor introduce un email válido');
            return;
        }

        this.userEmail = email;
        const btn = document.querySelector('.btn-auth-continue');
        if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        // Mock check
        setTimeout(() => {
            const isRegistered = email.includes('admin') || email.includes('david') || email.includes('test');
            if (isRegistered) {
                this.renderStep('login');
            } else {
                this.renderStep('register');
            }
        }, 800);
    },

    handleAgentLogin: async function() {
        const user = document.getElementById('agent-username').value;
        const pass = document.getElementById('agent-password').value;
        const loginBtn = document.getElementById('agentLoginBtn');
        const errorMsg = document.getElementById('agentErrorMsg');
        
        if (loginBtn) {
            loginBtn.disabled = true;
            loginBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Verificando...';
        }
        
        if (errorMsg) errorMsg.style.display = 'none';

        if (user === 'admin' && pass === 'paulita2003P?') {
            localStorage.setItem('weperty_session', JSON.stringify({
                user: 'administrador',
                role: 'admin',
                loggedAt: new Date().getTime()
            }));
            
            setTimeout(() => {
                window.location.href = 'crm.html';
            }, 800);
        } else {
            if (errorMsg) {
                errorMsg.innerText = "Error: Usuario o contraseña incorrectos.";
                errorMsg.style.display = 'block';
            }
            if (loginBtn) {
                loginBtn.disabled = false;
                loginBtn.innerHTML = '<span>Acceder al panel</span> <i class="fa-solid fa-arrow-right"></i>';
            }
        }
    },

    handleLogin: function() {
        const pass = document.getElementById('auth-password-input').value;
        if (!pass) return;

        const btn = document.querySelector('.btn-auth-continue');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        setTimeout(() => {
            // Success Mock
            localStorage.setItem(this.sessionKey, JSON.stringify({
                user: this.userEmail.split('@')[0],
                role: 'user',
                loggedAt: new Date().getTime()
            }));
            window.location.reload();
        }, 1000);
    },

    handleRegister: function() {
        const p1 = document.getElementById('auth-new-password').value;
        const p2 = document.getElementById('auth-confirm-password').value;

        if (!p1 || p1.length < 6) {
            alert(currentLang === 'es' ? 'La contraseña debe tener al menos 6 caracteres.' : 'Password must be at least 6 characters.');
            return;
        }
        if (p1 !== p2) {
            alert(currentLang === 'es' ? 'Las contraseñas no coinciden.' : 'Passwords do not match.');
            return;
        }

        const btn = document.querySelector('.btn-auth-continue');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        setTimeout(() => {
            alert(currentLang === 'es' ? '¡Registro iniciado! Por favor, revisa tu email para confirmar.' : 'Registration started! Please check your email to confirm.');
            this.hideModal();
        }, 1500);
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
