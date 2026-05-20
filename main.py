"""Punto de entrada del sistema de evaluación PHQ-9.

Composition root: único lugar donde se instancian las clases concretas.
Todo el resto del código recibe dependencias por inyección.
"""

from app.controllers.cuestionario_controlador import (
    CuestionarioControlador,
)
from app.repositories.cuestionario_json_repositorio import (
    CuestionarioJsonRepositorio,
)
from app.services.cuestionario_servicio import CuestionarioServicio
from app.ui.menu_principal import MenuPrincipal


def main() -> None:
    """Ensambla la cadena de dependencias y lanza la aplicación."""
    repositorio = CuestionarioJsonRepositorio()
    servicio = CuestionarioServicio(repositorio)
    controlador = CuestionarioControlador(servicio)
    MenuPrincipal(controlador).iniciar()


if __name__ == "__main__":
    main()
