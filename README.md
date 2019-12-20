# JWT Token Extended
## Sección 11 del curso
#### Usando el 7mo API

## Paso de arranque
#### En la terminal
```
> virtualenv venv
> pip install -r requirements.txt
> source venv/bin/activate
```

#### Código de arranque
El código de la sección 9 ó llamado por mí como 6to API

## Diferencias de JWT con JWT-Extended
1. Es más explícito
  - Lo que también significa que tenemos que programar/poner más cosas.
2. Ya no se requiere el archivo security.py.
3. Se usa ```flask_jwt_extended``` en vez de ```flask_jwt```
  - Librerías completamente DIFERENTES


# Cambios de arranque para el código
1. ```app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False```
  - Si JWT lanza un error, el api no lo va a detectar.
  - Por eso si quiere, por ejemplo, regresar 401 (No autorizado), se manda el error de regreso.
2. ```**data``` para recolectar todo lo que tiene el diccionario
  - Ya no se emplea ```data['price'], data['store_id']```
3. Método de:
  ```
  @classmethod
  def find_all(cls):
      return cls.query.all()
  ```
  Para ItemModel y StoreModel

## Cosas en requirements
1. uwsgi y mysqlclient fueron comentados
  - No hay un equivalente que me haya funcionado en Mac.

# FRESH TOKEN
### ¿Qué significa refrescar un token?
Estás logueado pero debes volver a proveer tu contraseña.

No lo has realiado por un par de días por ejemplo.

**Cuando se realiza una acción crítica, _como en borrar un repo en de Git_.**

Otros ejemplos son:
 - Cambiar contraseña o datos personales
 - Acciones de admin
 - Darle permisos a otro usuario

### Un Fresh Token entonces es
Un token que justo acabas de obtener porque justo acabas de proveer tus credenciales.

Con flask lo hacemos así: ```create_access_token(..., fresh=¿Es fresco?)```
- Con ```fresh=True``` el usuario acaba de ingresar o comprobar que es él.
- ```fresh=False``` lleva un rato sin ingresar su contraseña.
