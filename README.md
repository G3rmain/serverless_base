# Microservice Base

Este es un proyecto base para aplicaciones de microservicios.

## Requisitos

- Python 3.12


## Estructura de carpetas

Las siguientes carpetas son las carpetas principales, estas se pueden extender según las necesidades del proyecto.

- `src` - Source code
- `src/adapters` - Adapters: Clases que permitan la integración con servicios externos.
- `src/controllers` - Controllers: Clases con los controladores de la aplicación.
- `src/repositories` - Repositories: Clases que permitan realizar consultas a través de los adaptadores.
- `src/utils` - Utils: Clases y funciones con utilidades generales.

En caso de que se requiera extender la estructura de carpetas, se debe hacer de la siguiente manera:

- `src/adapters/module_name/file.py`
- `src/controllers/module_name/file.py`
- `src/repositories/module_name/file.py`
- `src/utils/module_name/file.py`


## Importaciones
La importación de módulos debe realizarse de la siguiente manera:

1. Las importaciones deben realizarse al inicio del archivo.
2. Se debe realizar una importación por línea.
3. Las importaciones de un módulo deben realizarse juntas.
4. Gerarquía de importaciones:
	* Importaciones de módulos internos
	* Importaciones de módulos externos
	* Importaciones de módulos python


Por ejemplo:

```python
from src.adapters import APIAdapter
from src.controllers import Controller
from src.repositories import Repository
from src.utils import Utils
from src.utils import SecretsSingleton

from pandas import DataFrame
from pandas import read_csv

from datetime import datetime
from datetime import timedelta
```


## Pruebas Unitarias

Todos los módulos deben tener pruebas unitarias con la siguiente estructura:

- `module/tests/test_*.py` - Pruebas unitarias para cada módulo.

Se debe crear un archivo `test_*.py` para cada archivo `*.py` en el módulo.

Deberá crearse por lo menos una prueba unitaria exitosa y una fallida para cada método de la clase.

Las pruebas unitarias deben tener el siguiente formato:

```python
import unittest
from module import Module


class TestModule(unittest.TestCase):

    def setUp(self):
        self.module = Module()

    def test_success(self):
        self.assertEqual(1, 1)

    def test_failure(self):
        self.assertEqual(1, 2)
```


## Environment Variables

Se debe crear un archivo `.env` en la raíz del proyecto con las variables de entorno.

Por ejemplo:

```.env
BUCKET_NAME=your-bucket-name
```


