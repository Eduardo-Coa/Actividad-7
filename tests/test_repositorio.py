"""Pruebas unitarias del repositorio JSON usando archivos temporales."""

import pytest
from datetime import datetime

from app.exceptions import (
    CuestionarioNoEncontradoError,
    EstudianteDuplicadoError,
)
from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.repositories.cuestionario_json_repositorio import (
    CuestionarioJsonRepositorio,
)


@pytest.fixture
def repo(tmp_path):
    """Repositorio apuntando a un archivo JSON temporal por cada test."""
    ruta = str(tmp_path / "test_cuestionarios.json")
    return CuestionarioJsonRepositorio(ruta_archivo=ruta)


@pytest.fixture
def cuestionario_a(fecha_valida: datetime) -> CuestionarioPHQ9:
    return CuestionarioPHQ9(
        id="repo-001",
        codigo_estudiante="EST-A",
        fecha_aplicacion=fecha_valida,
        respuestas=[0] * 9,
    )


class TestRepositorioGuardar:
    """Verifica persistencia y recuperación de cuestionarios."""

    def test_guardar_y_obtener_por_id(
        self,
        repo: CuestionarioJsonRepositorio,
        cuestionario_a: CuestionarioPHQ9,
    ) -> None:
        """Guardar y recuperar por ID debe devolver el mismo cuestionario."""
        repo.guardar(cuestionario_a)
        recuperado = repo.obtener_por_id(cuestionario_a.id)

        assert recuperado.id == cuestionario_a.id
        assert (
            recuperado.codigo_estudiante
            == cuestionario_a.codigo_estudiante
        )
        assert recuperado.respuestas == cuestionario_a.respuestas

    def test_guardar_duplicado_mismo_dia_lanza_excepcion(
        self,
        repo: CuestionarioJsonRepositorio,
        cuestionario_a: CuestionarioPHQ9,
        fecha_valida: datetime,
    ) -> None:
        """Dos cuestionarios del mismo estudiante en el mismo día deben fallar."""
        repo.guardar(cuestionario_a)
        duplicado = CuestionarioPHQ9(
            id="repo-002",
            codigo_estudiante="EST-A",
            fecha_aplicacion=fecha_valida,
            respuestas=[1] * 9,
        )
        with pytest.raises(EstudianteDuplicadoError):
            repo.guardar(duplicado)


class TestRepositorioEliminar:
    """Verifica la operación de eliminación."""

    def test_eliminar_lanza_error_si_no_existe(
        self, repo: CuestionarioJsonRepositorio
    ) -> None:
        """Eliminar un ID inexistente debe lanzar CuestionarioNoEncontradoError."""
        with pytest.raises(CuestionarioNoEncontradoError):
            repo.eliminar("id-inexistente")


class TestRepositorioActualizar:
    """Verifica la operación de actualización."""

    def test_actualizar_persiste_nuevas_respuestas(
        self,
        repo: CuestionarioJsonRepositorio,
        cuestionario_a: CuestionarioPHQ9,
    ) -> None:
        """Después de actualizar, las nuevas respuestas deben estar en el JSON."""
        repo.guardar(cuestionario_a)

        nuevas_respuestas = [3] * 9
        actualizado = CuestionarioPHQ9(
            id=cuestionario_a.id,
            codigo_estudiante=cuestionario_a.codigo_estudiante,
            fecha_aplicacion=cuestionario_a.fecha_aplicacion,
            respuestas=nuevas_respuestas,
        )
        repo.actualizar(actualizado)

        recuperado = repo.obtener_por_id(cuestionario_a.id)
        assert recuperado.respuestas == nuevas_respuestas
        assert recuperado.puntaje_total == 27
