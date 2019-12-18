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
El código de la sección 6 ó llamado por mí como 4to API

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


# EC2 AWS en consola
1. ```sudo apt update```
2. ```sudo apt install nginx```
  - ```sudo ufw app list``` para checar
3. ```sudo ufw enable```
4. ```sudo ufw allow 'Nginx HTTP'```
5. ```sudo ufw allow 'OpenSSH'``` para no quedarnos afuera
6. Seguir pasos de https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
  - En vez de usar ```sudo apt install python3-venv```, es más práctico ```pip3 install virtualenv```
  - Y luego ```virtualenv venv```. Este ya viene con wheel por ejemplo.
7. Hay que agregar a la línea de app.run() ```host='0.0.0.0'```
8. Para trabajar con MySQL:
  - ```sudo apt-get install python3-mysqldb```
  - ```sudo apt-get install libmysqlclient-dev```
  - ```pip install mysqlclient```
9. En <b>/etc/systemd/system/myproject.service</b> para no poner la base de datos textual en el API:
  - ```Environment=DATABASE_URL=mysql://username:password@localhost/db_name```
  - Y en app.py dejar la línea: ```app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///section4.db')```
10. No olvidar ```database.init_app(app)``` en el archivo que correrá el app.py.
  - Ya sea wsgi.py o run.py o como se llame.
