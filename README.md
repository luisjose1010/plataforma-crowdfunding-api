# Plataforma Crowdfunding API

## Table of Contents

1. [Descripción](#descripción)
2. [Guías de estilos](#guía-de-estilos)
3. [Tecnologías](#tecnologías)
4. [Scripts](#scripts)

## Descripción

API para plataforma crowdfunding desarrollado sobre el framework [FastApi](https://fastapi.tiangolo.com/ "FastApi"), implementado en el lenguaje de programación [Python](https://www.python.org/ "[Python]").

El usuario Admin creado por defecto tiene de constraseña "admin".

## Guía de estilos

### Código Python

Se utiliza en el proyecto el estilo básico que se recomienda de forma oficial por [Python](https://www.python.org/ "[Python]") en su guia de estilo [PEP 8](https://peps.python.org/pep-0008/ "[PEP 8]"), así como la consideración del resto de "PEPs" indicados en [PEPs](https://peps.python.org/ "[PEPs]"). Se tiene el objetivo de utilizar también las prácticas recomendadas en la documentación del framework [FastApi](https://fastapi.tiangolo.com/ "FastApi") en su página oficial [FastApi Learn](https://fastapi.tiangolo.com/learn/ "FastApi Learn"); en la cuál se especifica de forma recomendada la estructura de archivos a utilizar:

```other
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

También se toma en consideración la primera respuesta de este [hilo](https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project) y el repositorio de la herramienta creadora de proyectos oficial de la [biblioteca](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/src/backend), pero se parte desde la segunda, que hace referencia a la página oficial del framework. Además de tomarse en cuenta las diferentes páginas de documentación de las tecnologías utilizadas: [SQLAlchemy](https://docs.sqlalchemy.org/en/20/index.html "SQLAlchemy"), [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [Pydantic](https://docs.pydantic.dev/ "Pydantic") y el siguiente [Tutorial de FastApi](https://www.fastapitutorial.com/blog/database-connection-fastapi/).

### Commits de GIT

Se sigue la siguiente convención:

1. Un encabezado con el titulo o un resumen del commit, describiendo la razón del commit. Debe comenzar por un sustantivo o un imperativo. No debe tener más de 50 caracteres.

2. Un cuerpo donde se describen todos los cambios realizados en el commit y su función. Se recomienda comenzar con un sustantivo o imperativo, pero es más flexible. Pueden haber varios parrafos de información, separados por lineas en blanco. Cada linea debe tener máximo 72 caracteres. Debe terminar en punto.

3. Referencias a issues que se están resolviendo en el commit o que están relacionados (opcional).

#### Forma

Forma y descripción de un commit válido, según los puntos anteriores (se encuentra en el idioma inglés).

```text
Short (50 chars or less) summary

More detailed explanatory text. Wrap it to 72 characters. The blank
line separating the summary from the body is critical (unless you omit
the body entirely).

Write your commit message in the imperative: "Fix bug" and not "Fixed
bug" or "Fixes bug." This convention matches up with commit messages
generated by commands like git merge and git revert.

Further paragraphs come after blank lines.

- Bullet points are okay, too.
- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space. Use a hanging indent.

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```

#### Ejemplos

```text
Fix typo in introduction to user guide
```

```text
Derezz the master control program

MCP turned out to be evil and had become intent on world domination.
This commit throws Tron's disc into MCP (causing its deresolution)
and turns it back into a chess game.
```

```text
Simplify serialize.h's exception handling

Remove the 'state' and 'exceptmask' from serialize.h's stream
implementations, as well as related methods.

As exceptmask always included 'failbit', and setstate was always
called with bits = failbit, all it did was immediately raise an
exception. Get rid of those variables, and replace the setstate
with direct exception throwing (which also removes some dead
code).

As a result, good() is never reached after a failure (there are
only 2 calls, one of which is in tests), and can just be replaced
by !eof().

fail(), clear(n) and exceptions() are just never called. Delete
them.
```

#### Véase también

<https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53>

<https://chris.beams.io/posts/git-commit/>

## Tecnologías

### Features

- [Python](https://www.python.org/ "[Python]")
- [FastApi](https://fastapi.tiangolo.com/ "FastApi")
- [Pydantic](https://docs.pydantic.dev/ "Pydantic")
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Uvicorn](https://www.uvicorn.org/ "Uvicorn")

El proyecto está desarrollado en forma de API sobre el framework [FastApi](https://fastapi.tiangolo.com/ "FastApi"), implementado en el lenguaje [Python](https://www.python.org/ "[Python]"), incluyendo la herramienta [Pydantic](https://docs.pydantic.dev/ "Pydantic") a forma de validador de recursos, como ORM a [SQLAlchemy](https://docs.sqlalchemy.org/en/20/index.html "SQLAlchemy") y utilizando la herramienta [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) para gestionar las "migrations" y el "seeding" de la base de datos; con la finalidad de ser utilizada esta API por la aplicación principal desarrollada en React como cliente objetivo, mediante Javascript y recursos Json. Tanto en este parrafo y el listado, como más arriba en la sección de "Guía de estilos" se encuentran los enlaces adjuntos de la documentación respectiva de las diversas tecnologías utilizadas. Como servidor de desarrollo se utiliza [Uvicorn](https://www.uvicorn.org/ "Uvicorn"), de forma que sea desplegada la API con el comando indicado más adelante. Se implementa la autenticación de los usuarios, para su posterior autorización, mediante el uso del estandar OAuth 2.0 y el manejo de los tokens de acceso con la biblioteca [python-jose](https://python-jose.readthedocs.io/en/latest/ "python-jose").

Se puede obtener la documentación autogenerada de la API según la especificación OpenAPI, sirviendo como una guia estructurada para la parte del cliente, incluyendo sus endpoints, parametros, solicitudes y respuestas, en la ruta `/redoc` del servidor donde se esté ejecutandose la API. Mediante el script `redoc-export` que se ejecuta en el `manage.py`, se puede exportar el ReDoc de documentación actual de la API, colocándolo en la carpeta de documentación `/documentation/redoc`

Se creó un gestor de scripts llamado `manage.py`, con los que se encuentran a continuación, tanto en el apartado de condiguración del proyecto, como en el apartado general de scripts.

### Configuración inicial del proyecto

Para configurar el entorno de Python se necesita instalar las dependencias necesarias enlistadas en el archivo `requeriments.txt`, sea un entorno local o virtual, mediante los comandos que se mencionan luego de este apartado. Se debe configurar un archivo `.env` en la raiz del proyecto con las variables de entorno necesarias. El archivo `.env.example` se puede encontrar como un ejemplo de archivo `.env`. Por último se debe crear y rellenar con los datos básicos a la base de datos establecida, para finalmente ejecutar el servidor que despliega la API en modo de desarrollo, en este caso, con los script mencionados a continuación.

```bash
pip install -r requirements.txt
```

```bash
cd app
```

```bash
alembic upgrade head
```

```bash
python manage.py run
```

## Scripts

En el proyecto se pueden ejecutar tanto scripts de las bibliotecas como Alembic, que se describen los básicos, como del gestor integrado `manage.py`:

### `source ../env/Scripts/activate`

Asumiendo que se utiliza un virtual env para ejecutar el proyecto.\
Asmuniendo que la carpeta de un entorno virtual llamado `env` se encuentra en la carpeta superior a la raíz del proyecto.

### `cd app`

El comando básico que se utiliza para situar la linea de comandos en la carpeta donde se inicia la API.\
Es un comando sumamente básico pero útil del sistema operativ.

### `python manage.py run`

Ejecuta la aplicación en modo de desarrollo según la configuración de la aplicación, en el archivo de configuración o el archivo `.env`.\
Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) o la configuración establecida en el proyecto.

### `alembic upgrade head`

Ejecuta las migraciones de Alembic hasta la última disponible.\
Se supone deja al día a la base de datos con la estructura necesaria (y datos, según la migracion).

### `python manage.py redoc_export`

Exporta el archivo ReDoc para documentar la API según la especificación OpenAPI.\
El archivo se exporta en formato HTML y se encuentra en la carpeta `documentation/redoc`

### `uvicorn main:app --reload`

Ejecuta la aplicación en modo de desarrollo según la configuración de la aplicación con la configuración predeterminada de uvicorn.\
Realiza basciamente lo mismo que el script `python manage.py run` con la configuración predeterminada de Uvicorn, permitiendo el 'reload' del proyecto en cuánto al código modificado "en caliente".

### `alembic revision --autogenerate -m "message"`

Ejecuta una nueva migración autogenerada de Alembic para las tablas de la base de datos conectada, con el mensaje especificado entre comillas.\
Realiza un "diff" con la conexión actual de la base de datos, importante tomar en cuenta el contenido actual
