"""Repositorio DAO que persiste CuestionarioPHQ9 en un archivo JSON."""

import json
import os
from typing import List

from app.exceptions import (
    CuestionarioNoEncontradoError,
    EstudianteDuplicadoError,
)
from app.interfaces.i_repositorio_cuestionario import (
    IRepositorioCuestionario,
)
from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.utils.constantes_negocio import RUTA_DATOS_JSON


class CuestionarioJsonRepositorio(IRepositorioCuestionario):
    """Repositorio JSON que implementa el contrato IRepositorioCuestionario.

    Persiste los cuestionarios en un archivo JSON local. El constructor
    recibe la ruta como parámetro para facilitar la inyección en tests.

    Args:
        ruta_archivo: ruta al archivo JSON de almacenamiento.
    """

    def __init__(self, ruta_archivo: str = RUTA_DATOS_JSON) -> None:
        self._ruta = ruta_archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self) -> None:
        directorio = os.path.dirname(self._ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
        if not os.path.exists(self._ruta):
            self._escribir_todos([])

    def _leer_todos(self) -> List[CuestionarioPHQ9]:
        with open(self._ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return [CuestionarioPHQ9.from_dict(d) for d in datos]

    def _escribir_todos(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> None:
        with open(self._ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                [c.to_dict() for c in cuestionarios],
                archivo,
                indent=2,
                ensure_ascii=False,
            )

    def guardar(self, cuestionario: CuestionarioPHQ9) -> None:
        """Persiste un nuevo cuestionario verificando duplicados por fecha.

        Args:
            cuestionario: instancia validada a persistir.

        Raises:
            EstudianteDuplicadoError: si ya existe registro del mismo
                estudiante en la misma fecha calendario.
        """
        todos = self._leer_todos()
        fecha_nueva = cuestionario.fecha_aplicacion.date()
        for existente in todos:
            if (
                existente.codigo_estudiante
                == cuestionario.codigo_estudiante
                and existente.fecha_aplicacion.date() == fecha_nueva
            ):
                raise EstudianteDuplicadoError(
                    cuestionario.codigo_estudiante,
                    str(fecha_nueva),
                )
        todos.append(cuestionario)
        self._escribir_todos(todos)

    def obtener_por_id(
        self, id_cuestionario: str
    ) -> CuestionarioPHQ9:
        """Recupera un cuestionario por ID.

        Args:
            id_cuestionario: identificador único.

        Returns:
            CuestionarioPHQ9 encontrado.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """
        encontrado = next(
            (c for c in self._leer_todos() if c.id == id_cuestionario),
            None,
        )
        if encontrado is None:
            raise CuestionarioNoEncontradoError(id_cuestionario)
        return encontrado

    def obtener_todos(self) -> List[CuestionarioPHQ9]:
        """Retorna todos los cuestionarios almacenados.

        Returns:
            Lista de cuestionarios (puede estar vacía).
        """
        return self._leer_todos()

    def actualizar(self, cuestionario: CuestionarioPHQ9) -> None:
        """Reemplaza el cuestionario con el mismo ID.

        Args:
            cuestionario: instancia con datos actualizados.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """
        todos = self._leer_todos()
        for indice, existente in enumerate(todos):
            if existente.id == cuestionario.id:
                todos[indice] = cuestionario
                self._escribir_todos(todos)
                return
        raise CuestionarioNoEncontradoError(cuestionario.id)

    def eliminar(self, id_cuestionario: str) -> None:
        """Elimina el cuestionario con el ID dado.

        Args:
            id_cuestionario: identificador del registro a eliminar.

        Raises:
            CuestionarioNoEncontradoError: si el ID no existe.
        """
        todos = self._leer_todos()
        filtrados = [c for c in todos if c.id != id_cuestionario]
        if len(filtrados) == len(todos):
            raise CuestionarioNoEncontradoError(id_cuestionario)
        self._escribir_todos(filtrados)

    def obtener_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]:
        """Filtra cuestionarios por código de estudiante.

        Args:
            codigo_estudiante: código institucional a buscar.

        Returns:
            Lista de cuestionarios del estudiante (puede estar vacía).
        """
        codigo = codigo_estudiante.upper()
        return [
            c
            for c in self._leer_todos()
            if c.codigo_estudiante.upper() == codigo
        ]
