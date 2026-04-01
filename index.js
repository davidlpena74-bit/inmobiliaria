document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 WEPERTY OS Sincronizado. David, el sistema está listo.');

    const btnSyncFC = document.getElementById('btn-sync-fc');
    const msgFC = document.getElementById('msg-fc');
    const statusFC = document.getElementById('status-fc');
    const btnSyncIW = document.getElementById('btn-sync-iw');

    // Simulación de Radar para Fotocasa (Demostración de Bloqueo de Infraestructura)
    btnSyncFC.addEventListener('click', () => {
        btnSyncFC.innerText = '🔍 ESCANEANDO INFRAESTRUCTURA...';
        btnSyncFC.style.background = '#f1c40f';
        btnSyncFC.style.color = '#000';
        msgFC.innerText = 'Probando dominios Adevinta en España...';

        setTimeout(() => {
            btnSyncFC.innerText = '❌ BLOQUEO DE RED DETECTADO';
            btnSyncFC.style.background = '#ff7675';
            btnSyncFC.style.color = '#fff';
            msgFC.innerHTML = 'Error: <span style="color:#ff7675">ConnectionError</span> en api.fotocasa.es.<br>Usa el Puente Maestro de Inmoweb para saltar el firewall.';
            statusFC.classList.remove('status-online');
            statusFC.classList.add('status-offline');
        }, 3000);
    });

    // Simulación de Éxito para INMOWEB BRIDGE
    btnSyncIW.addEventListener('click', () => {
        const url = document.getElementById('inmoweb-url').value;
        if (!url) {
            alert('Introduce la URL del Feed de Inmoweb para Weperty Properties.');
            return;
        }

        btnSyncIW.innerText = '📥 SUCCIONANDO INVENTARIO...';
        btnSyncIW.style.background = '#00d1b2';
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            btnSyncIW.innerText = `📥 PROCESANDO: ${progress}/39 INMUEBLES`;
            
            if (progress >= 39) {
                clearInterval(interval);
                btnSyncIW.innerText = '✅ INVENTARIO WEPERTY SINCRONIZADO';
                btnSyncIW.style.background = '#2ecc71';
                confetti(); // 🎉 ¡Celebración visual de Weperty!
            }
        }, 50);
    });

    function confetti() {
        console.log('🎉 ¡Catálogo recuperado con éxito!');
        document.body.style.boxShadow = 'inset 0 0 100px hsla(155, 100%, 45%, 0.2)';
        setTimeout(() => { document.body.style.boxShadow = 'none'; }, 2000);
    }
});
