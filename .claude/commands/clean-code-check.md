# Clean Code Check

Analiza el código Python del proyecto y detecta violaciones a los principios de Clean Code.

Busca específicamente:
- **Nombres poco descriptivos**: variables de una letra, abreviaturas crípticas
- **Funciones largas**: más de ~20 líneas o que hacen más de una cosa
- **Números mágicos**: literales numéricos sin nombre (`if edad > 18` → debe ser constante)
- **Comentarios innecesarios**: comentarios que explican el *qué* en lugar del *por qué*
- **Código duplicado**: lógica repetida que debería extraerse
- **Niveles de anidamiento excesivos**: más de 2-3 niveles de `if`/`for` anidados
- **Parámetros en exceso**: funciones con más de 3-4 parámetros (candidatas a recibir un objeto)

Para cada problema: archivo, línea, descripción del problema y refactorización sugerida.
Aplica las correcciones directamente en los archivos al terminar el análisis.
