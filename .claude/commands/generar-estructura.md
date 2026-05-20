# Generar Estructura del Proyecto

Crea la estructura de carpetas y archivos base del proyecto siguiendo la arquitectura definida en CLAUDE.md.

Genera:
- `main.py` — punto de entrada mínimo
- `app/__init__.py`
- `app/interfaces/__init__.py` — ABCs base del dominio
- `app/models/__init__.py`
- `app/services/__init__.py`
- `app/repositories/__init__.py`
- `app/ui/__init__.py`
- `app/ui/mensajes.py` — constantes de mensajes al usuario
- `app/exceptions.py` — jerarquía de excepciones del dominio
- `tests/__init__.py`

Cada archivo debe incluir únicamente el esqueleto necesario (imports, clases vacías con docstring), sin lógica de negocio inventada.
Respeta PEP 8 y los principios SOLID desde el primer archivo.

Después muestra el árbol de directorios resultante.
