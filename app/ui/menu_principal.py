"""Vista CLI del sistema PHQ-9; implementa las heurísticas de Nielsen."""

import os
from typing import List, Optional

from app.controllers.cuestionario_controlador import (
    CuestionarioControlador,
)
from app.models.cuestionario_phq9 import (
    OPCIONES_RESPUESTA,
    TEXTOS_ITEMS_PHQ9,
    CuestionarioPHQ9,
)
from app.ui.mensajes import (
    APP_TITULO,
    FORMATO_DETALLE_ITEM,
    FORMATO_ESTADISTICAS,
    FORMATO_NIVEL,
    FORMATO_RESUMEN,
    MENU_PRINCIPAL,
    MSG_CANCELADO,
    MSG_ENTRADA_NUMERICA,
    MSG_LISTA_VACIA,
    MSG_OPCION_INVALIDA,
    MSG_RANGO_INVALIDO,
    MSG_SIN_RESULTADOS,
    PROMPT_CODIGO_BUSQUEDA,
    PROMPT_CODIGO_ESTUDIANTE,
    PROMPT_CONFIRMAR_ELIMINACION,
    PROMPT_FECHA_APLICACION,
    PROMPT_ID_CUESTIONARIO,
    PROMPT_RESPUESTA_ITEM,
    SEPARADOR,
    SEPARADOR_DOBLE,
    TEXTO_AYUDA,
)
from app.utils.constantes_negocio import FORMATO_FECHA_DISPLAY


class MenuPrincipal:
    """Vista principal de la aplicación en consola.

    Implementa las 10 heurísticas de Nielsen en la interacción CLI:
    (1) Estado visible, (2) Lenguaje del dominio, (3) Control/libertad,
    (4) Consistencia, (5) Prevención de errores, (6) Reconocimiento,
    (7) Flexibilidad, (8) Minimalismo, (9) Errores claros, (10) Ayuda.

    Args:
        controlador: instancia del controlador MVC.
    """

    def __init__(self, controlador: CuestionarioControlador) -> None:
        self._controlador = controlador
        self._acciones = {
            "1": self._accion_crear,
            "2": self._accion_listar,
            "3": self._accion_ver_detalle,
            "4": self._accion_editar,
            "5": self._accion_eliminar,
            "6": self._accion_buscar_estudiante,
            "7": self._accion_estadisticas,
            "H": self._mostrar_ayuda,
        }

    def iniciar(self) -> None:
        """Bucle principal; se ejecuta hasta que el usuario elige salir."""
        while True:
            self._limpiar_pantalla()
            opcion = input(
                MENU_PRINCIPAL.format(sep=SEPARADOR, titulo=APP_TITULO)
            ).strip().upper()

            if opcion == "0":
                print("\nHasta luego.\n")
                break

            accion = self._acciones.get(opcion)
            if accion:
                accion()
                input("\nPresione Enter para continuar...")
            else:
                print(f"\n[AVISO] {MSG_OPCION_INVALIDA}")
                input("\nPresione Enter para continuar...")

    # ── Acciones del menú ──────────────────────────────────────────────

    def _accion_crear(self) -> None:
        """Flujo guiado de registro de un nuevo cuestionario."""
        print(f"\n{SEPARADOR}")
        print("  REGISTRAR NUEVO CUESTIONARIO")
        print(SEPARADOR)

        codigo = self._leer_texto(PROMPT_CODIGO_ESTUDIANTE)
        if codigo is None:
            print(f"\n{MSG_CANCELADO}")
            return

        fecha_str = self._leer_fecha()
        if fecha_str is None:
            print(f"\n{MSG_CANCELADO}")
            return

        print(f"\n{SEPARADOR}")
        print("  Responda cada ítem del cuestionario:")
        print(SEPARADOR)
        respuestas = self._leer_respuestas()
        if respuestas is None:
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje, cuestionario = self._controlador.crear_cuestionario(
            codigo, fecha_str, respuestas
        )
        if exito and cuestionario:
            print(f"\n[OK] {mensaje}")
            print(SEPARADOR)
            self._imprimir_resumen(cuestionario)
        else:
            print(f"\n[ERROR] {mensaje}")

    def _accion_listar(self) -> None:
        """Muestra tabla resumida de todos los cuestionarios."""
        print(f"\n{SEPARADOR}")
        print("  TODOS LOS CUESTIONARIOS")
        print(SEPARADOR)

        _, _, lista = self._controlador.listar_cuestionarios()
        if not lista:
            print(f"\n  {MSG_LISTA_VACIA}")
            return

        print(f"  Total: {len(lista)} cuestionario(s)\n")
        for cuestionario in lista:
            self._imprimir_resumen(cuestionario)
            print()

    def _accion_ver_detalle(self) -> None:
        """Solicita ID y muestra detalle completo con cada ítem."""
        print(f"\n{SEPARADOR}")
        print("  DETALLE DEL CUESTIONARIO")
        print(SEPARADOR)

        id_cuestionario = self._leer_texto(PROMPT_ID_CUESTIONARIO)
        if id_cuestionario is None:
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje, cuestionario = self._controlador.ver_cuestionario(
            id_cuestionario
        )
        if not exito or cuestionario is None:
            print(f"\n[ERROR] {mensaje}")
            return

        self._imprimir_resumen(cuestionario)
        print()
        for i, valor in enumerate(cuestionario.respuestas):
            print(
                FORMATO_DETALLE_ITEM.format(
                    numero=i + 1,
                    texto=TEXTOS_ITEMS_PHQ9[i],
                    valor=valor,
                    etiqueta=OPCIONES_RESPUESTA[valor],
                )
            )

    def _accion_editar(self) -> None:
        """Solicita ID, muestra respuestas actuales y captura las nuevas."""
        print(f"\n{SEPARADOR}")
        print("  EDITAR RESPUESTAS")
        print(SEPARADOR)

        id_cuestionario = self._leer_texto(PROMPT_ID_CUESTIONARIO)
        if id_cuestionario is None:
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje, cuestionario = self._controlador.ver_cuestionario(
            id_cuestionario
        )
        if not exito or cuestionario is None:
            print(f"\n[ERROR] {mensaje}")
            return

        print("\n  Respuestas actuales:")
        self._imprimir_resumen(cuestionario)

        print(f"\n{SEPARADOR}")
        print("  Ingrese las nuevas respuestas:")
        print(SEPARADOR)
        nuevas = self._leer_respuestas()
        if nuevas is None:
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje, actualizado = self._controlador.editar_cuestionario(
            id_cuestionario, nuevas
        )
        if exito and actualizado:
            print(f"\n[OK] {mensaje}")
            self._imprimir_resumen(actualizado)
        else:
            print(f"\n[ERROR] {mensaje}")

    def _accion_eliminar(self) -> None:
        """Solicita ID, muestra resumen y pide confirmación explícita."""
        print(f"\n{SEPARADOR}")
        print("  ELIMINAR CUESTIONARIO")
        print(SEPARADOR)

        id_cuestionario = self._leer_texto(PROMPT_ID_CUESTIONARIO)
        if id_cuestionario is None:
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje, cuestionario = self._controlador.ver_cuestionario(
            id_cuestionario
        )
        if not exito or cuestionario is None:
            print(f"\n[ERROR] {mensaje}")
            return

        print("\n  Cuestionario a eliminar:")
        self._imprimir_resumen(cuestionario)

        confirmacion = input(
            "\n"
            + PROMPT_CONFIRMAR_ELIMINACION.format(id=id_cuestionario[:8])
        ).strip().lower()

        if confirmacion not in ("s", "si", "sí"):
            print(f"\n{MSG_CANCELADO}")
            return

        exito, mensaje = self._controlador.eliminar_cuestionario(
            id_cuestionario
        )
        if exito:
            print(f"\n[OK] {mensaje}")
        else:
            print(f"\n[ERROR] {mensaje}")

    def _accion_buscar_estudiante(self) -> None:
        """Lista cuestionarios de un estudiante por su código."""
        print(f"\n{SEPARADOR}")
        print("  BUSCAR POR ESTUDIANTE")
        print(SEPARADOR)

        codigo = self._leer_texto(PROMPT_CODIGO_BUSQUEDA)
        if codigo is None:
            print(f"\n{MSG_CANCELADO}")
            return

        _, _, lista = self._controlador.buscar_por_estudiante(codigo)
        if not lista:
            print(f"\n  {MSG_SIN_RESULTADOS}")
            return

        print(f"\n  Cuestionarios de '{codigo}': {len(lista)}\n")
        for cuestionario in lista:
            self._imprimir_resumen(cuestionario)
            print()

    def _accion_estadisticas(self) -> None:
        """Muestra estadísticas generales de todos los cuestionarios."""
        print(f"\n{SEPARADOR}")
        print("  ESTADÍSTICAS GENERALES")
        print(SEPARADOR)

        exito, mensaje, stats = self._controlador.obtener_estadisticas()
        if not exito or stats is None:
            print(f"\n[ERROR] {mensaje}")
            return

        if stats["total"] == 0:
            print(f"\n  {MSG_LISTA_VACIA}")
            return

        distribucion_str = "\n".join(
            FORMATO_NIVEL.format(nivel=nivel, cantidad=cantidad)
            for nivel, cantidad in stats[
                "distribucion_severidad"
            ].items()
        )
        print(
            "\n"
            + FORMATO_ESTADISTICAS.format(
                total=stats["total"],
                promedio=stats["promedio_puntaje"],
                casos_severos=stats["casos_severos"],
            )
        )
        print(distribucion_str)

    def _mostrar_ayuda(self) -> None:
        """Imprime la ayuda contextual y espera Enter."""
        input(
            TEXTO_AYUDA.format(
                sep_doble=SEPARADOR_DOBLE
            )
        )

    # ── Helpers de entrada ─────────────────────────────────────────────

    def _leer_respuestas(self) -> Optional[List[int]]:
        """Captura las 9 respuestas del cuestionario validando cada una.

        Muestra el progreso 'Ítem N/9' (Nielsen 1).
        Retorna None si el usuario cancela.

        Returns:
            Lista de 9 enteros 0-3, o None si se canceló.
        """
        respuestas: List[int] = []
        for i, texto in enumerate(TEXTOS_ITEMS_PHQ9):
            valor = self._leer_entero_en_rango(
                PROMPT_RESPUESTA_ITEM.format(
                    numero=i + 1, texto=texto
                ),
                minimo=0,
                maximo=3,
                cancelar_con=9,
            )
            if valor is None:
                return None
            respuestas.append(valor)
        return respuestas

    def _leer_entero_en_rango(
        self,
        prompt: str,
        minimo: int,
        maximo: int,
        cancelar_con: int = -1,
    ) -> Optional[int]:
        """Lee un entero en [minimo, maximo]; retorna None si cancela.

        Reintenta en bucle mostrando mensajes de error claros (Nielsen 9).

        Args:
            prompt: texto del prompt al usuario.
            minimo: valor mínimo aceptable.
            maximo: valor máximo aceptable.
            cancelar_con: valor numérico que activa la cancelación.

        Returns:
            Entero dentro del rango, o None si el usuario canceló.
        """
        while True:
            entrada = input(prompt).strip()
            try:
                valor = int(entrada)
            except ValueError:
                print(f"  [AVISO] {MSG_ENTRADA_NUMERICA}")
                continue

            if valor == cancelar_con:
                return None
            if minimo <= valor <= maximo:
                return valor
            print(
                "  [AVISO] "
                + MSG_RANGO_INVALIDO.format(
                    minimo=minimo, maximo=maximo
                )
            )

    def _leer_fecha(self) -> Optional[str]:
        """Lee y valida inmediatamente el formato de fecha DD/MM/AAAA HH:MM.

        Reintenta en bucle si el formato es incorrecto (Nielsen 5 y 9).
        Retorna None si el usuario ingresa '0'.

        Returns:
            Cadena de fecha válida, o None si se canceló.
        """
        from datetime import datetime as _dt

        while True:
            valor = input(PROMPT_FECHA_APLICACION).strip()
            if valor == "0":
                return None
            try:
                _dt.strptime(valor, FORMATO_FECHA_DISPLAY)
                return valor
            except ValueError:
                print(
                    "  [ERROR] Formato incorrecto. "
                    "Use DD/MM/AAAA HH:MM (ej. 19/05/2026 14:30)."
                )

    def _leer_texto(self, prompt: str) -> Optional[str]:
        """Lee una cadena no vacía; retorna None si el usuario ingresa '0'.

        Args:
            prompt: texto del prompt al usuario.

        Returns:
            Cadena ingresada, o None si el usuario ingresó '0'.
        """
        while True:
            valor = input(prompt).strip()
            if valor == "0":
                return None
            if valor:
                return valor
            print("  [AVISO] El campo no puede estar vacío.")

    def _imprimir_resumen(self, cuestionario: CuestionarioPHQ9) -> None:
        """Imprime el resumen compacto de un cuestionario.

        Args:
            cuestionario: instancia a resumir.
        """
        fecha_str = cuestionario.fecha_aplicacion.strftime(
            FORMATO_FECHA_DISPLAY
        )
        print(
            FORMATO_RESUMEN.format(
                id=cuestionario.id,
                codigo=cuestionario.codigo_estudiante,
                fecha=fecha_str,
                puntaje=cuestionario.puntaje_total,
                severidad=cuestionario.nivel_severidad,
            )
        )

    def _limpiar_pantalla(self) -> None:
        """Limpia la consola según el sistema operativo."""
        os.system("cls" if os.name == "nt" else "clear")
