"""Lógica de negocio para la gestión de cuestionarios PHQ-9."""

import uuid
from datetime import datetime
from typing import List

from app.exceptions import CuestionarioNoEncontradoError
from app.interfaces.i_repositorio_cuestionario import (
    IRepositorioCuestionario,
)
from app.models.cuestionario_phq9 import CuestionarioPHQ9


class CuestionarioServicio:
    """Orquesta las operaciones de negocio sobre CuestionarioPHQ9.

    Recibe el repositorio por inyección de dependencias para desacoplarse
    del mecanismo de persistencia concreto.

    Args:
        repositorio: implementación que cumple IRepositorioCuestionario.
    """

    def __init__(self, repositorio: IRepositorioCuestionario) -> None:
        self._repo = repositorio

    def registrar_cuestionario(
        self,
        codigo_estudiante: str,
        fecha_aplicacion: datetime,
        respuestas: List[int],
    ) -> CuestionarioPHQ9:
        """Crea y persiste un nuevo cuestionario PHQ-9.

        Genera un UUID para el ID. La validación de dominio ocurre
        en el constructor de CuestionarioPHQ9.

        Args:
            codigo_estudiante: código institucional del estudiante.
            fecha_aplicacion: momento de aplicación del cuestionario.
            respuestas: lista de 9 enteros entre 0 y 3.

        Returns:
            El cuestionario creado y ya persistido.

        Raises:
            FechaInvalidaError: si la fecha es futura o inválida.
            PuntajeInvalidoError: si alguna respuesta está fuera de rango.
            EstudianteDuplicadoError: si ya existe registro el mismo día.
        """
        nuevo_id = str(uuid.uuid4())
        cuestionario = CuestionarioPHQ9(
            id=nuevo_id,
            codigo_estudiante=codigo_estudiante,
            fecha_aplicacion=fecha_aplicacion,
            respuestas=respuestas,
        )
        self._repo.guardar(cuestionario)
        return cuestionario

    def obtener_cuestionario(
        self, id_cuestionario: str
    ) -> CuestionarioPHQ9:
        """Recupera un cuestionario por ID.

        Args:
            id_cuestionario: UUID del cuestionario.

        Returns:
            CuestionarioPHQ9 encontrado.

        Raises:
            CuestionarioNoEncontradoError: si no existe.
        """
        return self._repo.obtener_por_id(id_cuestionario)

    def listar_cuestionarios(self) -> List[CuestionarioPHQ9]:
        """Retorna todos los cuestionarios ordenados por fecha descendente.

        Returns:
            Lista ordenada de cuestionarios (puede estar vacía).
        """
        return sorted(
            self._repo.obtener_todos(),
            key=lambda c: c.fecha_aplicacion,
            reverse=True,
        )

    def actualizar_respuestas(
        self,
        id_cuestionario: str,
        nuevas_respuestas: List[int],
    ) -> CuestionarioPHQ9:
        """Reemplaza las respuestas de un cuestionario y recalcula puntaje.

        Args:
            id_cuestionario: UUID del cuestionario a editar.
            nuevas_respuestas: lista de 9 enteros entre 0 y 3.

        Returns:
            El cuestionario actualizado con nuevo puntaje y severidad.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
            PuntajeInvalidoError: si alguna respuesta es inválida.
        """
        existente = self._repo.obtener_por_id(id_cuestionario)
        actualizado = CuestionarioPHQ9(
            id=existente.id,
            codigo_estudiante=existente.codigo_estudiante,
            fecha_aplicacion=existente.fecha_aplicacion,
            respuestas=nuevas_respuestas,
        )
        self._repo.actualizar(actualizado)
        return actualizado

    def eliminar_cuestionario(self, id_cuestionario: str) -> None:
        """Elimina un cuestionario del repositorio.

        Args:
            id_cuestionario: UUID del cuestionario a eliminar.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """
        self._repo.eliminar(id_cuestionario)

    def buscar_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]:
        """Lista todos los cuestionarios de un estudiante específico.

        Args:
            codigo_estudiante: código institucional.

        Returns:
            Lista de cuestionarios ordenada por fecha descendente.
        """
        return sorted(
            self._repo.obtener_por_estudiante(codigo_estudiante),
            key=lambda c: c.fecha_aplicacion,
            reverse=True,
        )

    def obtener_estadisticas(self) -> dict:
        """Calcula estadísticas generales sobre todos los cuestionarios.

        Returns:
            Diccionario con total, promedio_puntaje,
            distribucion_severidad y casos_severos.
        """
        todos = self._repo.obtener_todos()
        if not todos:
            return {
                "total": 0,
                "promedio_puntaje": 0.0,
                "distribucion_severidad": {},
                "casos_severos": 0,
            }

        puntajes = [c.puntaje_total for c in todos]
        distribucion: dict[str, int] = {}
        for cuestionario in todos:
            nivel = cuestionario.nivel_severidad
            distribucion[nivel] = distribucion.get(nivel, 0) + 1

        casos_severos = sum(
            1 for c in todos if c.es_riesgo_severo
        )

        return {
            "total": len(todos),
            "promedio_puntaje": sum(puntajes) / len(puntajes),
            "distribucion_severidad": distribucion,
            "casos_severos": casos_severos,
        }
