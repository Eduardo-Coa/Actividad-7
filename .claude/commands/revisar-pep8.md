# Revisar PEP 8

Revisa todos los archivos `.py` del proyecto en busca de violaciones a PEP 8.

Verifica:
- Longitud de líneas (máx. 79 caracteres)
- Indentación (4 espacios, sin tabs)
- Espacios en blanco alrededor de operadores y después de comas
- Orden de imports (stdlib → third-party → local)
- Nomenclatura: `snake_case` en funciones/variables, `PascalCase` en clases, `UPPER_CASE` en constantes
- Líneas en blanco entre definiciones (2 entre clases/funciones top-level, 1 entre métodos)
- Ausencia de espacios dentro de paréntesis/corchetes

Para cada violación proporciona: archivo, número de línea, regla violada y corrección.
Después aplica todas las correcciones directamente en los archivos.
