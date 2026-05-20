"""Constantes de dominio para el cuestionario PHQ-9."""

# Estructura del cuestionario
NUM_ITEMS_PHQ9: int = 9

# Rangos de respuesta por ítem
PUNTAJE_MINIMO_ITEM: int = 0
PUNTAJE_MAXIMO_ITEM: int = 3

# Puntaje máximo posible (9 ítems × 3 puntos)
PUNTAJE_MAXIMO_PHQ9: int = 27

# Umbrales de severidad (puntaje mínimo para cada nivel)
PUNTAJE_RIESGO_LEVE_PHQ9: int = 5
PUNTAJE_RIESGO_MODERADO_PHQ9: int = 10
PUNTAJE_RIESGO_MODSEVERO_PHQ9: int = 15
PUNTAJE_RIESGO_SEVERO_PHQ9: int = 20

# Persistencia
RUTA_DATOS_JSON: str = "data/cuestionarios.json"

# Formato de fecha para presentación en UI
FORMATO_FECHA_DISPLAY: str = "%d/%m/%Y %H:%M"
