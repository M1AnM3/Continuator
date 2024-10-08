# Continuator
Este repositorio contiene un archivo, Continuator.py, que genera continuaciones de oraciones utilizando la última palabra de la oración como base.

Las continuaciones no buscan preservar la coherencia si no la jerarquía de las palabras dentro de una digráfica que genera una base de datos, llamada A en el archivo.

La jerarquía esta dada por un conjunto de vértices llamado quasi-núcleo, que es un conjunto de vétices independiente y 2-absorbente.

## Características

- Generación de continuaciones basadas en la última palabra de la oración.
- Fácil de usar y personalizar para diferentes propósitos.

# Uso
Compilar el archivo, luego aparecera "User: " que es donde se pone la oración que se desea extender. Es posible que tarde en compilar el archivo, ya que depende del tamaño de la base de datos.

```bash
python Continuator.py
```

# Ejemplo
```bash
User: Un
Continuator: Un gato ve un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en un gato. Es naranja. Excepto en
```

## Cómo Funciona

1. **Entrada:** El usuario proporciona una oración.
2. **Procesamiento:** El sistema analiza la última palabra de la oración y genera continuaciones utilizando la jerarquía una digráfica.
3. **Salida:** Se devuelve una opción de continuación.

Creado por Miguel (https://github.com/M1AnM3).
