# Programacion Backend — Unidad 2

Replica del proyecto de clases [pbe-2026_u2_proyecto1](https://github.com/enriquepalaciosc/pbe-2026_u2_proyecto1),
revision `01966d65548bc41cb09249d956c67f2306c85b68`.
Repositorio personal: [Jomiancto/Unidad2](https://github.com/Jomiancto/Unidad2).
La estructura Django y la app `pedidos_app` conservan los archivos originales.
`ORIGEN_PROFESOR.json` registra los hashes de origen; `tools/comparar_fuentes.py`
verifica los archivos admitiendo diferencias de salto de linea final.
Solo `settings.py` se adapto para cargar configuracion local segura.
No se requiere acceso al repositorio del profesor para ejecutar esta copia.

## Entorno verificado

- Windows, Cmder: `E:\cmder\Cmder.exe`.
- Carpeta de trabajo: `E:\cmder\Unidad2`.
- Python 3.12.3, Django 6.1.2, DRF 3.18.3, mysqlclient 2.2.8.
- Dependencias y versiones transitivas fijadas en `requirements.txt`.
- MariaDB 12.3.2, base `u2_p1_bd`, host `127.0.0.1`, puerto `3306`.
- Instancia portatil existente: `E:\MariaDB\mariadb-12.3.2-winx64\mariadb-12.3.2-winx64`.

## Iniciar desde Cmder

Abrir Cmder, seleccionar sesion cmd y ejecutar:

```bat
cd /d E:\cmder\Unidad2
INICIAR_BACKEND.cmd 8001
```

El puerto 8000 esta ocupado por el proyecto anterior. Se conservo ese proceso y se
uso 8001 para esta replica. Cuando 8000 este libre, `INICIAR_BACKEND.cmd` lo usa por defecto.
El iniciador activa `.venv`, verifica/inicia la instancia MariaDB ya inicializada,
comprueba Django y migraciones, revisa el puerto y ejecuta runserver solo en loopback.
No instala dependencias ni aplica migraciones ni realiza operaciones Git al iniciar.

Host: [http://127.0.0.1:8001/](http://127.0.0.1:8001/).
Administrador: [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/).
Detener Django con Ctrl+C en su consola. MariaDB permanece activa y se comparte
con el trabajo anterior; no detenerla mientras otros proyectos la usen.
No iniciar un segundo servidor en el mismo puerto si este ya esta ejecutandose.

## Configuracion privada y reinstalacion

`.env` no se publica. Se genero SECRET_KEY propia y se conservo la credencial local
existente, sin copiar la del profesor. El entorno del proceso tiene prioridad sobre `.env`.
Variables: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
Se conserva el usuario local heredado `root`; queda pendiente crear un usuario de
desarrollo con permisos limitados cuando se configure expresamente.

En una reinstalacion, desde Cmder y sin sobrescribir un entorno existente:

```bat
cd /d E:\cmder\Unidad2
"C:\Program Files\Python312\python.exe" -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
copy .env.example .env
```

Completar `.env` localmente con credenciales propias y una SECRET_KEY nueva.
Para generar una clave se puede utilizar `secrets.token_urlsafe(64)` en una sesion
Python local; no copiar su valor a conversaciones ni archivos versionados.
El formato del ejemplo usa cadenas JSON entre comillas dobles.
No repetir el comando copy si ya existe `.env`.

Comprobar servidor DB, alcance y respaldo antes de aplicar migraciones en otra BD.
La preparacion inicial en otro equipo debe revisar las rutas reales de MariaDB;
`tools/mariadb_local.py` contiene las rutas verificadas de este computador.

## Avance del profesor conservado

- Categoria: nombre unico.
- Producto: nombre, descripcion nullable, precio y stock no negativos, activo nullable,
  creado automatico, codigo y categorias mediante relacion muchos a muchos.
- Cliente: nombre y email unico.
- Pedido: fecha, pagado y cliente con CASCADE en el ORM.
- Item: cantidad, precio_unitario, pedido con CASCADE y producto con PROTECT en el ORM.
- Tres migraciones originales, sin regenerarlas.

Solo existe `/admin/` y sus subrutas. `/` muestra la bienvenida de Django en DEBUG,
sin vista de negocio. No hay API CRUD, serializers, routers, plantillas propias,
modelos registrados en admin ni pruebas implementadas en `pedidos_app/tests.py`.
No se creo superusuario. Estos elementos corresponden al avance pendiente de clases.

## Verificar

Desde el entorno virtual en Cmder:

```bat
python manage.py check
python manage.py showmigrations
python manage.py migrate --check
python manage.py makemigrations --check --dry-run
python tools\inspeccionar_bd.py --despues
python tools\comparar_fuentes.py
python tools\verificar_http.py 8001
```

`makemigrations --check --dry-run` solo comprueba diferencias y no genera migraciones.
Los scripts de verificacion no crean datos de negocio. Los respaldos se conservan
en `.local/respaldos`, ignorados por Git, junto a los registros de las tareas Cmder.
`manage.py test` encuentra cero tests; no equivale a cobertura automatizada del negocio.
Consultar `COMANDOS_CMDER.md` e `INFORME_BACKEND.md` para resultados reales.
