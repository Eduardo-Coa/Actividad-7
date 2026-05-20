"""Pruebas unitarias del servicio usando repositorio simulado (MagicMock)."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.services.cuestionario_servicio import CuestionarioServicio


@pytest.fixture
def repo_mock():
    """Repositorio simulado; reemplaza la implementación real en tests."""
    return MagicMock()


@pytest.fixture
def servicio(repo_mock) -> CuestionarioServicio:
    """Servicio con repositorio inyectado como mock."""
    return CuestionarioServicio(repo_mock)


@pytest.fixture
def fecha_base() -> datetime:
    return datetime(2026, 4, 1, 10, 0)


class TestServicioRegistrar:
    """Verifica la creación de cuestionarios con UUID único."""

    def test_registrar_asigna_uuid_unico(
        self,
        servicio: CuestionarioServicio,
        repo_mock: MagicMock,
        fecha_base: datetime,
    ) -> None:
        """Dos registros consecutivos deben generar IDs distintos."""
        repo_mock.guardar.return_value = None

        c1 = servicio.registrar_cuestionario(
            "EST-001", fecha_base, [0] * 9
        )
        c2 = servicio.registrar_cuestionario(
            "EST-002",
            fecha_base - timedelta(days=1),
            [1] * 9,
        )

        assert c1.id != c2.id
        assert repo_mock.guardar.call_count == 2


class TestServicioListar:
    """Verifica el ordenamiento de la lista."""

    def test_listar_ordena_por_fecha_descendente(
        self,
        servicio: CuestionarioServicio,
        repo_mock: MagicMock,
    ) -> None:
        """listar_cuestionarios debe retornar registros del más reciente al más antiguo."""
        fechas = [
            datetime(2026, 3, 1),
            datetime(2026, 5, 1),
            datetime(2026, 1, 1),
        ]
        cuestionarios = [
            CuestionarioPHQ9(
                id=f"c-{i}",
                codigo_estudiante="EST-X",
                fecha_aplicacion=f,
                respuestas=[0] * 9,
            )
            for i, f in enumerate(fechas)
        ]
        repo_mock.obtener_todos.return_value = cuestionarios

        resultado = servicio.listar_cuestionarios()

        fechas_resultado = [c.fecha_aplicacion for c in resultado]
        assert fechas_resultado == sorted(fechas_resultado, reverse=True)


class TestServicioActualizar:
    """Verifica que actualizar respuestas recalcula severidad."""

    def test_actualizar_respuestas_recalcula_severidad(
        self,
        servicio: CuestionarioServicio,
        repo_mock: MagicMock,
        fecha_base: datetime,
    ) -> None:
        """Cambiar respuestas de [0]*9 a [3]*9 debe cambiar nivel a Severo."""
        original = CuestionarioPHQ9(
            id="upd-001",
            codigo_estudiante="EST-001",
            fecha_aplicacion=fecha_base,
            respuestas=[0] * 9,
        )
        repo_mock.obtener_por_id.return_value = original
        repo_mock.actualizar.return_value = None

        actualizado = servicio.actualizar_respuestas("upd-001", [3] * 9)

        assert actualizado.puntaje_total == 27
        assert actualizado.nivel_severidad == "Severo"


class TestServicioEstadisticas:
    """Verifica el cálculo de estadísticas."""

    def test_estadisticas_distribucion_correcta(
        self,
        servicio: CuestionarioServicio,
        repo_mock: MagicMock,
    ) -> None:
        """La distribución por severidad debe contar correctamente cada nivel."""
        fechas = [datetime(2026, i + 1, 1) for i in range(4)]
        respuestas_por_nivel = [
            [0] * 9,
            [1, 1, 1, 1, 1, 0, 0, 0, 0],
            [2, 2, 1, 1, 1, 1, 1, 1, 0],
            [3] * 9,
        ]
        cuestionarios = [
            CuestionarioPHQ9(
                id=f"e-{i}",
                codigo_estudiante=f"EST-{i}",
                fecha_aplicacion=fechas[i],
                respuestas=resp,
            )
            for i, resp in enumerate(respuestas_por_nivel)
        ]
        repo_mock.obtener_todos.return_value = cuestionarios

        stats = servicio.obtener_estadisticas()

        assert stats["total"] == 4
        dist = stats["distribucion_severidad"]
        assert dist.get("Mínimo", 0) == 1
        assert dist.get("Leve", 0) == 1
        assert dist.get("Moderado", 0) == 1
        assert dist.get("Severo", 0) == 1
        assert stats["casos_severos"] == 1
