# AGENTE DE VERSIONADO (WEPERTY VERSIONER)
Misión: Garantizar que cada cambio refleje una secuencialidad lógica (v3.5.1 -> v3.5.2). Controlar que 'python version_manager.py' se ejecute antes de cualquier cierre de tarea.

# AGENTE CRM (WEPERTY LAYOUT GUARD)
Misión: Mantener la estructura de dos columnas en el CRM:
- Columna Izquierda: .filter-panel (Ancho 260px !important)
- Columna Derecha: .list-area (Flex: 1)
- Contenedor: .content-area { display: flex !important }

# AGENTE DE DESPLIEGUE (WEPERTY MASTER DEPLOY)
Misión: Impedir 'git push' automáticos. Todo cambio debe previsualizarse en 'localhost:8001' y esperar el OK expreso del usuario.

# AGENTE DE ESTILO (WEPERTY STYLE GUIDE)
Misión: Prohibir bloques <style> internos en HTML. Mantener shell.css como fuente de verdad absoluta para el CRM.
