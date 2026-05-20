"""Jerarquía de excepciones de dominio del sistema PHQ-9."""


class AppError(Exception):
    """Base de todas las excepciones de dominio.

    Args:
        mensaje: descripción legible del error.
    """

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)

    def __str__(self) -> str:
        return self.mensaje


class FechaInvalidaError(AppError):
    """Fecha de aplicación fuera de rango o con formato incorrecto.

    Args:
        detalle: descripción específica del problema con la fecha.
    """

    def __init__(self, detalle: str) -> None:
        super().__init__(f"Fecha inválida: {detalle}")


class PuntajeInvalidoError(AppError):
    """Valor numérico fuera del rango válido para un ítem PHQ-9.

    Args:
        valor: el valor que se intentó asignar.
        rango_permitido: tupla (mínimo, máximo) permitido.
    """

    def __init__(
        self, valor: int, rango_permitido: tuple[int, int]
    ) -> None:
        minimo, maximo = rango_permitido
        super().__init__(
            f"Valor {valor} fuera del rango permitido "
            f"[{minimo}, {maximo}]."
        )


class CuestionarioNoEncontradoError(AppError):
    """El ID buscado no existe en el repositorio.

    Args:
        id_cuestionario: el ID que no se encontró.
    """

    def __init__(self, id_cuestionario: str) -> None:
        super().__init__(
            f"No se encontró el cuestionario con ID '{id_cuestionario}'."
        )


class EstudianteDuplicadoError(AppError):
    """Ya existe un cuestionario registrado para este estudiante en la misma fecha.

    Args:
        codigo_estudiante: código del estudiante duplicado.
        fecha: fecha en que ya existe un registro.
    """

    def __init__(self, codigo_estudiante: str, fecha: str) -> None:
        super().__init__(
            f"Ya existe un cuestionario para el estudiante "
            f"'{codigo_estudiante}' en la fecha {fecha}."
        )
