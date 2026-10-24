# Informe de replica y levantamiento — 24-10-2026

## Estado comprobado

Replica funcionando desde Cmder en http://127.0.0.1:8001/.
Raiz real: E:\cmder\Unidad2. Se preservo E:\cmder\u2_proyecto1, sus cambios
sin confirmar y su servidor anterior en 8000. No se reemplazo su codigo.
El remoto origin de esta nueva carpeta corresponde a Jomiancto/Unidad2.

La ejecucion inicial por GUI no era utilizable con la habilidad computer-use.
Se encontro y probo la interfaz de linea de comandos del propio Cmder.exe:
/START y /X con -run @archivo.task. Las instalaciones, verificaciones, configuracion
local, respaldo, migraciones y arranque corrieron bajo procesos hijos de Cmder/ConEmu,
con CMDER_ROOT y ConEmuPID registrados. PowerShell solo preparo/leyo archivos y lanzo
el ejecutable; no ejecuto el levantamiento de Django ni las migraciones directamente.
Se conservaron los scripts de fase y logs locales para revisar exactamente la ejecucion.

## Comparacion con el profesor

Fuente: https://github.com/enriquepalaciosc/pbe-2026_u2_proyecto1
Revision: 01966d65548bc41cb09249d956c67f2306c85b68.
Se reviso el arbol completo y todo el codigo Python de manage.py, u2_proyecto1 y pedidos_app.
No habia README, requirements ni pyproject.toml en el origen.
Se omitieron .idea y __pycache__ porque son archivos del editor y caches.
Los otros 15 archivos Python originales coinciden con sus blobs Git admitiendo
solo normalizacion del salto de linea final. Models, admin, apps, views, tests,
las tres migraciones y urls conservan el codigo original.
settings.py se adapto para cargar variables de entorno/.env con credenciales propias;
la clave y contraseña del profesor no se escribieron en la replica ni en commits.
Se agregaron documentacion, dependencias, iniciador y herramientas de diagnostico.

La ultima migracion fue generada con Django 6.1.2 y las primeras con 6.1.1;
se instalo 6.1.2 en un entorno nuevo, sin actualizar el entorno anterior.
DRF 3.18.3 y mysqlclient 2.2.8 quedaron fijados, junto con sus dependencias transitivas.

La descripcion relacional solicitada coincide con el codigo: Cliente->Pedido CASCADE,
Pedido->Item CASCADE, Producto->Item PROTECT y Producto<->Categoria M2M automatica.
No se adjunto otro diagrama en esta solicitud para comparar mas detalles.
Se conservaron los related_name del profesor: cliente, pedido, producto y categorias.
Los enteros positivos de Django permiten cero; no se cambiaron estas reglas.
CASCADE/PROTECT son politicas del ORM; no se presentan como acciones CASCADE fisicas
de las claves foraneas de MariaDB.

## MariaDB y migraciones

Servidor confirmado mediante SELECT VERSION(), DATABASE(), @@port, @@datadir:
12.3.2-MariaDB, u2_p1_bd, puerto 3306 y directorio portable existente en E:\MariaDB.
La instancia ya estaba activa; no se inicializo ni reinicio ni se cambio su servicio.
Se uso la credencial local preexistente y se genero una SECRET_KEY nueva en .env ignorado.
Se preservo root local; crear un usuario limitado queda pendiente de una configuracion posterior.

Antes de migrar existian 12 tablas, incluidas productos_app_categoria y productos_app_producto.
No existian tablas pedidos_app_. El plan contenia exclusivamente tres migraciones nuevas:

1. 0001_initial: Categoria, Cliente y Producto.
2. 0002_pedido: Pedido y relacion a Cliente.
3. 0003_producto_categorias_item: M2M categorias e Item.

Se creo respaldo local con mariadb-dump antes de migrar (17369 bytes).
Ruta: .local/respaldos/u2_p1_bd_20261024_140655.sql; no se publica.
Se aplicaron las tres migraciones originales; todas figuran [X].
Las tablas anteriores permanecen. Las nuevas tablas verificadas son:

- pedidos_app_categoria
- pedidos_app_cliente
- pedidos_app_producto
- pedidos_app_pedido
- pedidos_app_item
- pedidos_app_producto_categorias

Se comprobaron PK en las seis, FK Pedido->Cliente, Item->Pedido, Item->Producto
y ambas FK de la tabla M2M; unicidad de Categoria.nombre, Cliente.email y del par
producto_id/categoria_id; tambien las politicas ORM CASCADE/PROTECT.
Los seis modelos/tablas nuevos tienen 0 registros; no se insertaron datos de prueba.

## Pruebas y servidor

Python 3.12.3; Django 6.1.2; pip check sin dependencias rotas.
manage.py check: sin errores. migrate --check: correcto.
makemigrations --check --dry-run: sin cambios; no se generaron migraciones nuevas.
manage.py test: encontro 0 tests, conservando el archivo vacio de clases.
La inspeccion de esquema y pruebas HTTP adicionales terminaron correctamente.
git diff --check: correcto. Fuentes originales: comparacion correcta.

| Peticion | Resultado observado |
|---|---|
| GET /admin/ | 302 a /admin/login/?next=/admin/ |
| GET /admin/login/ | 200 |
| GET / | 200, bienvenida Django con DEBUG |
| GET /api/ | 404, no existe |
| GET /pedidos/ | 404, no existe |

El proceso Django en 8001 es PID 6236, bajo el ConEmu de Cmder PID 1728;
su cadena incluye cmd.exe, tools/ejecutar.py y runserver. Los PID cambiaran al reiniciar.
MariaDB PID 3232 permanece en loopback 3306; se conserva el servidor anterior PID 16772 en 8000.
No se publico ningun servidor en Internet.

## GitHub

Ambos repositorios se revisaron antes de copiar archivos: el del profesor contenia
el codigo indicado y Jomiancto/Unidad2 estaba vacio (API contents devolvio empty).
Se creo una carpeta independiente y un historial nuevo saneado, sin arrastrar
commits con credenciales del profesor ni del proyecto anterior.
Origin: https://github.com/Jomiancto/Unidad2.git. Rama: main.
Se creo el commit local tras revisar archivos preparados, sintaxis, exclusiones y secretos.
El push fallo con codigo 128: Git no tiene credenciales disponibles y la ejecucion
sin interaccion no puede solicitar inicio de sesion. La conexion GitHub del plugin
confirma permisos de lectura y push=false. Por tanto, Unidad2 remoto sigue vacio:
el respaldo Git local esta preparado, pero aun no existe respaldo remoto.
No se intento publicar al profesor y no se utilizo force push.

Para completar el respaldo, el usuario debe abrir Cmder, entrar a E:\cmder\Unidad2
y ejecutar git push -u origin main, completando el inicio de sesion oficial si se solicita.
No escribir tokens ni contrasenas en comandos o archivos. La autenticacion interactiva
requiere participacion del usuario; no es un fallo de Django o MariaDB.

## Archivos y pendientes

La primera revision previa a publicar se detuvo por un falso positivo: el verificador
encontro en su propio codigo el patron que buscaba. Se corrigio esa coincidencia
sin omitir la revision de archivos privados ni de valores sensibles. Los avisos
LF/CRLF de Git se atendieron con .gitattributes; no cambiaron la logica original.
El primer historial generado en Windows presento finales de linea duplicados al
incorporar salidas de consola; git diff --check lo detecto antes del commit.
Se corrigio la generacion a LF y se normalizaron espacios al final de cada linea.

Copiados: manage.py, pedidos_app completo y fuentes de u2_proyecto1.
Adaptado: u2_proyecto1/settings.py. Agregados: entorno.py, requirements.txt,
.gitignore, .env.example, README.md, este informe, COMANDOS_CMDER.md,
ORIGEN_PROFESOR.json, AGENTS.md, INICIAR_BACKEND.cmd y tools/ de diagnostico.
Locales ignorados: .env, .venv, .local (respaldos/logs), scripts y tareas de fases.

Faltan CRUD/API REST, serializers, routers, vistas de negocio, plantillas propias,
registro de modelos en admin, tests de negocio y superusuario. No se agregaron
funcionalidades distintas del punto de partida del profesor.
El administrador tiene la pagina de login, pero no se crearon credenciales ni usuarios.
