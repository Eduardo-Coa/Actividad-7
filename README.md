# Sistema de Evaluación PHQ-9

Aplicación de consola para registrar y gestionar cuestionarios de salud mental PHQ-9 de estudiantes.

## Tecnologías

- Python 3.10+
- Persistencia en JSON
- pytest para pruebas unitarias

## Arquitectura

Patrón **MVC + Repository**, principios **SOLID** y heurísticas de **Nielsen**.

```
app/
├── models/       # Entidad CuestionarioPHQ9
├── interfaces/   # Contratos (ABC)
├── repositories/ # Acceso a datos (JSON)
├── services/     # Lógica de negocio
├── controllers/  # Mediador MVC
└── ui/           # Menú de consola
```

## Uso

```bash
python main.py
```

## Pruebas

```bash
python -m pytest -v
```

## Operaciones disponibles

| Opción | Acción |
|--------|--------|
| 1 | Registrar cuestionario |
| 2 | Listar todos |
| 3 | Ver detalle |
| 4 | Editar respuestas |
| 5 | Eliminar |
| 6 | Buscar por estudiante |
| 7 | Estadísticas generales |
| H | Ayuda |
| 0 | Salir |
