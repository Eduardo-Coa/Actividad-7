"""Constantes de texto visibles al usuario en la interfaz de consola."""

# ── Encabezados ────────────────────────────────────────────────────────
APP_TITULO = "Sistema de Evaluación PHQ-9 — Salud Mental Estudiantil"
SEPARADOR = "─" * 60
SEPARADOR_DOBLE = "═" * 60

# ── Menú principal ─────────────────────────────────────────────────────
MENU_PRINCIPAL = (
    "\n{sep}\n"
    "  {titulo}\n"
    "{sep}\n"
    "  [1] Registrar nuevo cuestionario\n"
    "  [2] Ver todos los cuestionarios\n"
    "  [3] Buscar cuestionario por ID\n"
    "  [4] Editar respuestas de cuestionario\n"
    "  [5] Eliminar cuestionario\n"
    "  [6] Buscar cuestionarios por estudiante\n"
    "  [7] Ver estadísticas generales\n"
    "  [H] Ayuda\n"
    "  [0] Salir\n"
    "{sep}\n"
    "Seleccione una opción: "
)

# ── Prompts de entrada ─────────────────────────────────────────────────
PROMPT_CODIGO_ESTUDIANTE = (
    "Código del estudiante (ej. EST-2024-001, '0' para cancelar): "
)
PROMPT_FECHA_APLICACION = (
    "Fecha de aplicación (DD/MM/AAAA HH:MM, ej. 19/05/2026 14:30,\n"
    "  '0' para cancelar): "
)
PROMPT_RESPUESTA_ITEM = (
    "  Ítem {numero}/9 — {texto}\n"
    "    [0] Nunca  [1] Varios días  "
    "[2] Más de la mitad  [3] Casi siempre\n"
    "  Respuesta (0-3, '9' para cancelar): "
)
PROMPT_ID_CUESTIONARIO = (
    "ID del cuestionario ('0' para cancelar): "
)
PROMPT_CONFIRMAR_ELIMINACION = (
    "¿Confirma que desea eliminar el cuestionario '{id}'? (s/n): "
)
PROMPT_CODIGO_BUSQUEDA = (
    "Código del estudiante a buscar ('0' para cancelar): "
)

# ── Mensajes de éxito ──────────────────────────────────────────────────
MSG_CANCELADO = "Operación cancelada."
MSG_LISTA_VACIA = (
    "No hay cuestionarios registrados. "
    "Use la opción [1] para registrar el primero."
)
MSG_SIN_RESULTADOS = (
    "No se encontraron cuestionarios para ese estudiante."
)

# ── Mensajes de error ──────────────────────────────────────────────────
MSG_OPCION_INVALIDA = (
    "Opción no válida. Ingrese un número del menú o 'H' para ayuda."
)
MSG_ENTRADA_NUMERICA = (
    "Debe ingresar un número entero. Intente de nuevo."
)
MSG_RANGO_INVALIDO = (
    "Valor fuera de rango [{minimo}-{maximo}]. Intente de nuevo."
)

# ── Formatos de presentación ───────────────────────────────────────────
FORMATO_RESUMEN = (
    "  ID        : {id}\n"
    "  Estudiante: {codigo}\n"
    "  Fecha     : {fecha}\n"
    "  Puntaje   : {puntaje}/27\n"
    "  Severidad : {severidad}"
)
FORMATO_DETALLE_ITEM = (
    "  Ítem {numero}: {texto}\n"
    "    Respuesta: [{valor}] {etiqueta}"
)
FORMATO_ESTADISTICAS = (
    "  Total de cuestionarios : {total}\n"
    "  Promedio de puntaje    : {promedio:.1f}/27\n"
    "  Casos de riesgo alto   : {casos_severos}\n"
    "\n  Distribución por severidad:"
)
FORMATO_NIVEL = "    {nivel:<25}: {cantidad}"

# ── Ayuda ──────────────────────────────────────────────────────────────
TEXTO_AYUDA = (
    "\n{sep_doble}\n"
    "  AYUDA — Sistema de Evaluación PHQ-9\n"
    "{sep_doble}\n"
    "  El PHQ-9 evalúa síntomas depresivos en 9 ítems.\n"
    "  Cada ítem se puntúa de 0 (Nunca) a 3 (Casi siempre).\n"
    "\n"
    "  Escala de severidad:\n"
    "    0-4  : Mínimo               5-9  : Leve\n"
    "    10-14: Moderado             15-19: Moderadamente severo\n"
    "    20-27: Severo\n"
    "\n"
    "  NOTA: El Ítem 9 evalúa pensamientos de autolesión.\n"
    "  Puntajes >= 20 requieren atención profesional urgente.\n"
    "{sep_doble}\n"
    "Presione Enter para continuar..."
)
