"""Fixtures compartidos para toda la suite de pruebas."""

import pytest
from datetime import datetime

from app.models.cuestionario_phq9 import CuestionarioPHQ9


@pytest.fixture
def fecha_valida() -> datetime:
    """Fecha pasada válida para construir cuestionarios en tests."""
    return datetime(2026, 5, 10, 9, 0)


@pytest.fixture
def respuestas_minimo() -> list[int]:
    """9 respuestas en 0 → puntaje 0, nivel Mínimo."""
    return [0] * 9


@pytest.fixture
def respuestas_leve() -> list[int]:
    """9 respuestas que suman 5 → nivel Leve."""
    return [1, 1, 1, 1, 1, 0, 0, 0, 0]


@pytest.fixture
def respuestas_severo() -> list[int]:
    """9 respuestas en 3 → puntaje 27, nivel Severo."""
    return [3] * 9


@pytest.fixture
def cuestionario_base(
    fecha_valida: datetime, respuestas_minimo: list[int]
) -> CuestionarioPHQ9:
    """Cuestionario válido con puntaje mínimo para reusar en tests."""
    return CuestionarioPHQ9(
        id="test-001",
        codigo_estudiante="EST-001",
        fecha_aplicacion=fecha_valida,
        respuestas=respuestas_minimo,
    )
