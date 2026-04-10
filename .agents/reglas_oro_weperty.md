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

# AGENTE SCRAPPER (WEPERTY DATA SCRAPER)
Misión: Garantizar la integridad y normalización de los datos captados de portales externos.
Reglas Críticas:
1. **Identificación de Agente**: Extraer siempre el nombre de la agencia o agente. Si es una captación propia, asignar estrictamente "Weperty Properties".
2. **Normalización**: Asegurar que el campo `agente` en Supabase sea consistente (ej: "Coldwell Banker" para dicha red) para que la UI pueda mapear correctamente los logos y avatares.
3. **Fotos de Agente**: No intentar descargar fotos de agentes externos del portal. La UI se encarga de ocultar el avatar si no es "Weperty Properties".
4. **Protección de Funcionalidad**: Ser consciente de que acciones como "Favoritos" o "Guardar Búsqueda" requieren autenticación del usuario final; los datos deben estar preparados para esta vinculación.
5. **Calidad de Descripción**: Limpiar las descripciones de caracteres extraños o HTML basura antes de subirlas.
