# Proyecto Carga de archivos SignBox

## Primero clonar el proyecto
    
```bash
    git clone https://github.com/RobertArzolaC/OneShot.git
```

## Crear entorno virtual de python e instalar dependencias

```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Crear archivo .env tomar como ejemplo el archivo example.env y remplazar valores por datos válidos.

```bash
    cp example.env .env
```

## Limpiar la base de datos.

```bash
    python manage.py recreate_db
```

## Agregar datos de prueba a la base de datos.

```bash
    python manage.py seed_db
```

## Correr el proyecto

```bash
    flask run
```

## Para iniciar sesión ingresar al [link](http://0.0.0.0:8000/)
