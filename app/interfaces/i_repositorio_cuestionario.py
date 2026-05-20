"""Contrato abstracto para el repositorio de CuestionarioPHQ9."""

from abc import ABC, abstractmethod
from typing import List

from app.models.cuestionario_phq9 import CuestionarioPHQ9


class IRepositorioCuestionario(ABC):
    """Define las operaciones CRUD para cualquier repositorio de PHQ-9.

    Las implementaciones concretas deciden el mecanismo de persistencia
    (JSON, base de datos, memoria, etc.) sin afectar las capas superiores.
    """

    @abstractmethod
    def guardar(self, cuestionario: CuestionarioPHQ9) -> None:
        """Persiste un nuevo cuestionario.

        Args:
            cuestionario: instancia validada a persistir.

        Raises:
            EstudianteDuplicadoError: si ya existe un registro para ese
                codigo_estudiante en la misma fecha calendario.
        """

    @abstractmethod
    def obtener_por_id(self, id_cuestionario: str) -> CuestionarioPHQ9:
        """Recupera un cuestionario por su ID único.

        Args:
            id_cuestionario: identificador del cuestionario.

        Returns:
            La instancia encontrada.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """

    @abstractmethod
    def obtener_todos(self) -> List[CuestionarioPHQ9]:
        """Retorna todos los cuestionarios almacenados.

        Returns:
            Lista (puede estar vacía) de todos los cuestionarios.
        """

    @abstractmethod
    def actualizar(self, cuestionario: CuestionarioPHQ9) -> None:
        """Reemplaza el cuestionario existente con el mismo ID.

        Args:
            cuestionario: instancia con datos actualizados.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """

    @abstractmethod
    def eliminar(self, id_cuestionario: str) -> None:
        """Elimina el cuestionario con el ID dado.

        Args:
            id_cuestionario: identificador del registro a eliminar.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """

    @abstractmethod
    def obtener_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]:
        """Filtra cuestionarios por código de estudiante.

        Args:
            codigo_estudiante: código institucional a buscar.

        Returns:
            Lista de cuestionarios del estudiante (puede estar vacía).
        """
