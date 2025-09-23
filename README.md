# Paso a Paso de Instalación de FastAPI, Ejecución del Schema en MySQL y Librerías a Instalar

## 1. Instalación de FastAPI y Uvicorn

```bash
pip install fastapi[standard] uvicorn
```

## 2. Instalación de Conector MySQL
```
pip install mysql-connector-python
```

## 3. Instalación de Ninja para las Vistas
```
pip install jinja2
```

## 4. Ejecución del script de la base de datos

Ejecuta el script `sql/schema.sql` en tu servidor MySQL para crear las tablas necesarias.

## 5. CheckList Librerías a instalar para el proyecto

- [_] fastapi[standard]
- [_] uvicorn
- [_] mysql-connector-python
- [_] Jinja2

## 6. Notas

- Solo se utilizarán `Cursor` y `mysql-connector-python` para la conexión y manejo de la base de datos.
- Se usará `Jinja2` para las vistas.
- El script de la base de datos se encuentra en `sql/schema.sql`.
- Ninja (Jinja2) se utiliza para renderizar las vistas HTML.
