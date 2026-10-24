"""Genera el historial legible a partir de ejecuciones reales de Cmder."""
import json
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
registros = [json.loads(linea) for linea in (raiz / '.local' / 'comandos.jsonl').read_text(encoding='utf-8').splitlines()]
for indice, registro in enumerate(registros):
    if 'tools\\verificar_http.py 8001' in registro['comando']:
        registros.insert(indice, {
            'fecha': 'Inicio previo a la primera prueba HTTP; proceso sigue activo',
            'directorio': str(raiz), 'comando': 'python manage.py runserver 127.0.0.1:8001 --noreload',
            'cmder': r'E:\cmder', 'conemu_pid': '1728', 'codigo': 'EN EJECUCION',
            'salida': 'Iniciado mediante INICIAR_BACKEND.cmd 8001; PID 6236. Respuesta HTTP verificada en el comando siguiente.'
        })
        break
documento = '''# Comandos de Cmder — levantamiento de la replica del profesor

Fecha: 24-10-2026, America/Santiago.

Los comandos de instalacion, configuracion local, comprobacion, respaldo, migracion
y arranque se ejecutaron bajo Cmder.exe mediante su interfaz de tareas de linea de comandos.
Cada registro comprueba CMDER_ROOT y ConEmuPID; no son ejecuciones de levantamiento en PowerShell.
La herramienta externa utilizo PowerShell solo para leer/preparar archivos y lanzar Cmder.
No se automatizo el teclado de la terminal. Un comando Python registra los procesos hijos
y sus resultados, manteniendo la consola de Cmder como proceso antecesor.

## Acceso y lanzamiento real de tareas

Se ejecutaron estas invocaciones externas (PowerShell, no dentro de Cmder):

```powershell
Start-Process -FilePath 'E:\\cmder\\Cmder.exe' -ArgumentList '/START C:\\Users\\cal_lab117\\Downloads\\Kit_Backend_Codex /X "-NoSingle -run @C:\\Users\\cal_lab117\\Downloads\\Kit_Backend_Codex\\CMDER_COMPROBAR.task"' -WorkingDirectory 'E:\\cmder' -WindowStyle Hidden
```

La tarea de acceso ejecuto, en este orden, desde Kit_Backend_Codex:

```bat
@echo off
call E:\\cmder\\vendor\\init.bat
cd /d C:\\Users\\cal_lab117\\Downloads\\Kit_Backend_Codex
echo CMDER_ROOT=%CMDER_ROOT%> CMDER_ACCESO.log
echo ConEmuPID=%ConEmuPID%>> CMDER_ACCESO.log
echo ConEmuDir=%ConEmuDir%>> CMDER_ACCESO.log
echo CMDCMDLINE=%CMDCMDLINE%>> CMDER_ACCESO.log
echo ACCESO_CMDER_CORRECTO>> CMDER_ACCESO.log
type CMDER_ACCESO.log
```

Resultado: CMDER_ROOT=E:\\cmder, ConEmuPID=13616, ACCESO_CMDER_CORRECTO.
El lanzador de tareas se uso luego con /START E:\\cmder\\Unidad2 y archivos
FASE1_CMDER.task, FASE2_CMDER.task, FASE3_CMDER.task y FASE4_CMDER.task, en ese orden.
Las tareas contienen cmd.exe /d /k y el archivo .cmd correspondiente.
Los scripts usan call E:\\cmder\\vendor\\init.bat, cd /d E:\\cmder\\Unidad2 y
call .venv\\Scripts\\activate.bat. Los controles if errorlevel interrumpen ante fallos.
Los scripts de fase, logs y respaldos completos permanecen locales, sin publicarse.

## Comandos reales, en orden de ejecucion

Todos los siguientes procesos se ejecutaron en E:\\cmder\\Unidad2.
Se incluyen resultado exacto y codigo de salida. Las ordenes extensas se conservan
sin contrasenas; la credencial se lee de .env y nunca se pasa como argumento.
El envoltorio utilizado es python tools\\ejecutar.py seguido del comando registrado;
antes de crear .venv se utilizo "C:\\Program Files\\Python312\\python.exe" para ese envoltorio.

'''
for numero, registro in enumerate(registros, 1):
    comando = registro['comando']
    if 'pip' in comando:
        finalidad = 'Comprobar o instalar dependencias en el interprete indicado.'
    elif 'migrate' in comando or 'showmigrations' in comando:
        finalidad = 'Inspeccionar/aplicar/verificar migraciones segun las opciones del comando.'
    elif 'git' in comando:
        finalidad = 'Comprobar o preparar exclusivamente el repositorio personal.'
    elif 'respaldo' in comando:
        finalidad = 'Guardar respaldo local antes de migrar, sin publicar datos.'
    else:
        finalidad = 'Preparar o verificar el componente indicado y registrar el resultado real.'
    documento += (f"### {numero}. {registro['fecha']}\n\nDirectorio: `{registro['directorio']}`. "
                  f"Cmder: `{registro['cmder']}`; ConEmuPID: `{registro['conemu_pid']}`.\n\n"
                  f"Finalidad: {finalidad}\n\n```bat\n{comando}\n```\n\n"
                  f"Codigo de salida: **{registro['codigo']}**. Resultado:\n\n```text\n{registro['salida'].strip()}\n```\n\n")
documento += '''## Servidor activo (comando aun en ejecucion)

La fase de arranque llamo INICIAR_BACKEND.cmd 8001. Este activo .venv,
comprobo MariaDB, Django, migraciones y puerto, y ejecuto:

```bat
python tools\\ejecutar.py python manage.py runserver 127.0.0.1:8001 --noreload
```

El proceso continua, por lo que todavia no tiene codigo de salida. HTTP se verifica
por separado en los registros. No debe confundirse con el proyecto anterior en 8000.

## Volver a iniciar al encender el computador (recomendados, no una nueva ejecucion)

Abrir E:\\cmder\\Cmder.exe, sesion cmd. Forma abreviada:

```bat
cd /d E:\\cmder\\Unidad2
INICIAR_BACKEND.cmd 8001
```

Forma manual equivalente, en orden:

```bat
cd /d E:\\cmder\\Unidad2
call .venv\\Scripts\\activate.bat
python tools\\mariadb_local.py
python manage.py check
python manage.py showmigrations
python manage.py migrate --check
python manage.py runserver 127.0.0.1:8001 --noreload
```

MariaDB solo se inicia si no esta escuchando y se verifica la instancia existente;
no se inicializan datos. Si migrate --check falla, revisar primero migrate --plan.
No ejecutar migraciones automaticamente cada vez que se inicia.

Host: http://127.0.0.1:8001/ ; administrador: http://127.0.0.1:8001/admin/.
Para detener Django: Ctrl+C en la consola del servidor. MariaDB permanece activa;
no detenerla si otros proyectos la usan. Para usar 8000 cuando este libre:

```bat
INICIAR_BACKEND.cmd
```

Si se pierde .venv, desde Cmder y solo cuando no exista:

```bat
"C:\\Program Files\\Python312\\python.exe" -m venv .venv
call .venv\\Scripts\\activate.bat
python -m pip install -r requirements.txt
```

Los archivos .task son solo el mecanismo de despacho; la inicializacion interna
de Cmder/Clink no se considera un comando del proyecto escrito por Codex.
Las lecturas externas del codigo y del estado de Windows fueron consultas de
preparacion, no levantamientos alternativos. No se registran valores de secretos.
'''
documento = '\n'.join(linea.rstrip() for linea in documento.splitlines()) + '\n'
(raiz / 'COMANDOS_CMDER.md').write_text(documento, encoding='utf-8', newline='\n')
print('COMANDOS_CMDER.md actualizado:', len(registros), 'comandos finalizados y servidor activo documentado.')
