"""Controlador MVC que media entre la UI y el servicio de cuestionarios."""

from datetime import datetime
from typing import List, Optional

from app.exceptions import AppError
from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.services.cuestionario_servicio import CuestionarioServicio
from app.utils.constantes_negocio import FORMATO_FECHA_DISPLAY


class CuestionarioControlador:
    """Mediador MVC entre la vista CLI y la capa de servicio.

    Traduce acciones del usuario en llamadas al servicio y convierte
    cualquier excepción de dominio en una tupla (éxito, mensaje).
    La vista nunca captura excepciones directamente.

    Args:
        servicio: instancia del servicio de cuestionarios.
    """

    def __init__(self, servicio: CuestionarioServicio) -> None:
        self._servicio = servicio

    def crear_cuestionario(
        self,
        codigo_estudiante: str,
        fecha_str: str,
        respuestas: List[int],
    ) -> tuple[bool, str, Optional[CuestionarioPHQ9]]:
        """Procesa la creación de un cuestionario desde la UI.

        Args:
            codigo_estudiante: código institucional del estudiante.
            fecha_str: fecha en formato FORMATO_FECHA_DISPLAY.
            respuestas: lista de 9 enteros entre 0 y 3.

        Returns:
            Tupla (exito, mensaje, cuestionario_o_none).
        """
        try:
            fecha = datetime.strptime(fecha_str, FORMATO_FECHA_DISPLAY)
            cuestionario = self._servicio.registrar_cuestionario(
                codigo_estudiante, fecha, respuestas
            )
            return True, "Cuestionario registrado correctamente.", cuestionario
        except ValueError:
            return (
                False,
                f"Formato de fecha inválido. Use: DD/MM/AAAA HH:MM",
                None,
            )
        except AppError as error:
            return False, str(error), None

    def listar_cuestionarios(
        self,
    ) -> tuple[bool, str, List[CuestionarioPHQ9]]:
        """Obtiene todos los cuestionarios ordenados por fecha.

        Returns:
            Tupla (exito, mensaje, lista_cuestionarios).
        """
        try:
            lista = self._servicio.listar_cuestionarios()
            return True, "", lista
        except AppError as error:
            return False, str(error), []

    def ver_cuestionario(
        self, id_cuestionario: str
    ) -> tuple[bool, str, Optional[CuestionarioPHQ9]]:
        """Busca un cuestionario por ID para mostrar su detalle.

        Args:
            id_cuestionario: UUID del cuestionario.

        Returns:
            Tupla (exito, mensaje, cuestionario_o_none).
        """
        try:
            cuestionario = self._servicio.obtener_cuestionario(
                id_cuestionario
            )
            return True, "", cuestionario
        except AppError as error:
            return False, str(error), None

    def editar_cuestionario(
        self,
        id_cuestionario: str,
        nuevas_respuestas: List[int],
    ) -> tuple[bool, str, Optional[CuestionarioPHQ9]]:
        """Actualiza las respuestas de un cuestionario.

        Args:
            id_cuestionario: UUID del cuestionario a editar.
            nuevas_respuestas: lista de 9 enteros entre 0 y 3.

        Returns:
            Tupla (exito, mensaje, cuestionario_actualizado_o_none).
        """
        try:
            actualizado = self._servicio.actualizar_respuestas(
                id_cuestionario, nuevas_respuestas
            )
            return (
                True,
                "Cuestionario actualizado correctamente.",
                actualizado,
            )
        except AppError as error:
            return False, str(error), None

    def eliminar_cuestionario(
        self, id_cuestionario: str
    ) -> tuple[bool, str]:
        """Elimina un cuestionario.

        Args:
            id_cuestionario: UUID del cuestionario a eliminar.

        Returns:
            Tupla (exito, mensaje).
        """
        try:
            self._servicio.eliminar_cuestionario(id_cuestionario)
            return True, "Cuestionario eliminado correctamente."
        except AppError as error:
            return False, str(error)

    def buscar_por_estudiante(
        self, codigo_estudiante: str
    ) -> tuple[bool, str, List[CuestionarioPHQ9]]:
        """Lista todos los cuestionarios de un estudiante.

        Args:
            codigo_estudiante: código institucional del estudiante.

        Returns:
            Tupla (exito, mensaje, lista_cuestionarios).
        """
        try:
            lista = self._servicio.buscar_por_estudiante(
                codigo_estudiante
            )
            return True, "", lista
        except AppError as error:
            return False, str(error), []

    def obtener_estadisticas(
        self,
    ) -> tuple[bool, str, Optional[dict]]:
        """Obtiene estadísticas generales para mostrar en la UI.

        Returns:
            Tupla (exito, mensaje, dict_estadisticas_o_none).
        """
        try:
            estadisticas = self._servicio.obtener_estadisticas()
            return True, "", estadisticas
        except AppError as error:
            return False, str(error), None
