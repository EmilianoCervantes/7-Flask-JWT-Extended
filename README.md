# De API Flask a Heroku
## Sección 8 del curso
#### Usando el 4to API

## Paso de arranque
#### En la terminal
```
> virtualenv venv
> source venv/bin/activate
> mkdir code
```

#### Librerías con las que se empezó
```
> pip install Flask-RESTful
> pip install Flask-JWT
> pip install Flask-SQLAlchemy
```

#### Código de arranque
El código de la sección 9 ó llamado por mí como 6to API

## Para el deploy
1. Crear archivo requirements.txt
  - Decir cómo instalar las librerías que utilizamos
  - ALTERNATIVA: en consola ``` pip freeze > requirements.txt ```
  - Agregar la librería uWSGI (esta no se debe instalar localmente)
  - Agregar psycopg2 --\> Librería de python para interactuar con Postgres
2. Crear archivo uwsgi.ini
  - Parámetros de configuración para indicar cómo se va a correr
  - die-on-term = true --\> Matarlo cuando el proceso termina
  - module = app:app --\> Indicar que es el app.py y dentro del app.py, la variable app.
  - memory-report = true --\> Reporte


# Cambios de arranque para el código
1. ```app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False```
  - .
2. ```**data``` para recolectar
  - ```data['price'], data['store_id']```
3. Método de:
  ```
  @classmethod
  def find_all(cls):
      return cls.query.all()
  ```
  Para ItemModel y StoreModel
