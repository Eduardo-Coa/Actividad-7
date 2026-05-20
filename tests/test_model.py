"""Pruebas unitarias del modelo CuestionarioPHQ9 y Respuesta."""

import pytest
from datetime import datetime, timedelta

from app.exceptions import FechaInvalidaError, PuntajeInvalidoError
from app.models.cuestionario_phq9 import CuestionarioPHQ9, Respuesta


class TestCuestionarioPHQ9Puntaje:
    """Verifica el cálculo automático del puntaje total."""

    def test_puntaje_calculado_automaticamente(
        self, fecha_valida: datetime
    ) -> None:
        """El puntaje total debe ser la suma exacta de las 9 respuestas."""
        respuestas = [1, 2, 1, 0, 0, 0, 1, 0, 0]
        cuestionario = CuestionarioPHQ9(
            id="t-001",
            codigo_estudiante="EST-001",
            fecha_aplicacion=fecha_valida,
            respuestas=respuestas,
        )
        assert cuestionario.puntaje_total == sum(respuestas)

    @pytest.mark.parametrize(
        "respuestas,nivel_esperado",
        [
            ([0] * 9, "Mínimo"),
            ([1, 1, 1, 1, 1, 0, 0, 0, 0], "Leve"),
            ([2, 2, 1, 1, 1, 1, 1, 1, 0], "Moderado"),
            ([2, 2, 2, 2, 2, 2, 2, 1, 0], "Moderadamente severo"),
            ([3] * 9, "Severo"),
        ],
    )
    def test_clasificacion_severidad_todos_los_niveles(
        self,
        fecha_valida: datetime,
        respuestas: list[int],
        nivel_esperado: str,
    ) -> None:
        """Cada rango de puntaje debe producir el nivel de severidad correcto."""
        cuestionario = CuestionarioPHQ9(
            id="t-002",
            codigo_estudiante="EST-002",
            fecha_aplicacion=fecha_valida,
            respuestas=respuestas,
        )
        assert cuestionario.nivel_severidad == nivel_esperado


class TestCuestionarioPHQ9Validacion:
    """Verifica que las validaciones del modelo lanzan las excepciones correctas."""

    def test_fecha_futura_lanza_excepcion(self) -> None:
        """Una fecha de aplicación futura debe lanzar FechaInvalidaError."""
        with pytest.raises(FechaInvalidaError):
            CuestionarioPHQ9(
                id="t-003",
                codigo_estudiante="EST-003",
                fecha_aplicacion=datetime.now() + timedelta(days=1),
                respuestas=[0] * 9,
            )

    def test_respuestas_fuera_de_rango_lanza_excepcion(
        self, fecha_valida: datetime
    ) -> None:
        """Un valor de respuesta mayor a 3 debe lanzar PuntajeInvalidoError."""
        with pytest.raises(PuntajeInvalidoError):
            CuestionarioPHQ9(
                id="t-004",
                codigo_estudiante="EST-004",
                fecha_aplicacion=fecha_valida,
                respuestas=[0, 0, 0, 0, 4, 0, 0, 0, 0],
            )

    def test_id_vacio_lanza_excepcion(
        self, fecha_valida: datetime
    ) -> None:
        """Un ID vacío o solo espacios debe lanzar FechaInvalidaError."""
        with pytest.raises(FechaInvalidaError):
            CuestionarioPHQ9(
                id="   ",
                codigo_estudiante="EST-005",
                fecha_aplicacion=fecha_valida,
                respuestas=[0] * 9,
            )


class TestCuestionarioPHQ9Serializacion:
    """Verifica la serialización y deserialización del modelo."""

    def test_serializacion_round_trip(
        self, cuestionario_base: CuestionarioPHQ9
    ) -> None:
        """from_dict(to_dict()) debe producir un objeto con los mismos datos."""
        datos = cuestionario_base.to_dict()
        reconstruido = CuestionarioPHQ9.from_dict(datos)

        assert reconstruido.id == cuestionario_base.id
        assert (
            reconstruido.codigo_estudiante
            == cuestionario_base.codigo_estudiante
        )
        assert reconstruido.respuestas == cuestionario_base.respuestas
        assert reconstruido.puntaje_total == cuestionario_base.puntaje_total
        assert (
            reconstruido.nivel_severidad == cuestionario_base.nivel_severidad
        )


class TestRespuesta:
    """Verifica la clase Respuesta individual."""

    def test_respuesta_valor_invalido_lanza_excepcion(self) -> None:
        """Un valor_respuesta de 4 debe lanzar PuntajeInvalidoError."""
        with pytest.raises(PuntajeInvalidoError):
            Respuesta(numero_pregunta=1, valor_respuesta=4)

    def test_respuesta_numero_fuera_de_rango(self) -> None:
        """numero_pregunta=10 debe lanzar PuntajeInvalidoError."""
        with pytest.raises(PuntajeInvalidoError):
            Respuesta(numero_pregunta=10, valor_respuesta=0)
