/**
 * Weperty Auth Utility (v5.0.0)
 * Centralized session and authentication modal management.
 */

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
        const modal = document.getElementById('auth-modal');
        if (modal) {
            // Ensure translations are applied before showing
            if (typeof updateContent === 'function') updateContent();
            
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        } else {
            console.warn("Auth modal not found in DOM");
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
    }
};

window.Auth = Auth;
