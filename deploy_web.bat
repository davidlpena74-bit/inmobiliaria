@echo off
echo ==========================================
echo 🚀 Desplegando Weperty (Web + CRM)
echo ==========================================

echo ➕ Añadiendo archivos de la web publica y CRM...
git add index.html CNAME crm/

echo 🔄 Guardando cambios en el servidor...
git commit -m "Arquitectura separada: Web publica en root y CRM privado en /crm"

echo ⬆️ Subiendo a GitHub...
git push

if %ERRORLEVEL% EQU 0 (
    echo ✅ Despliegue completado con exito.
    echo 🌐 Web Publica: https://weperty.com/
    echo 🔒 CRM Administrador: https://weperty.com/crm/login.html
) else (
    echo ⚠️ Hubo un error al subir a GitHub. Verifica tu conexion.
)

pause
