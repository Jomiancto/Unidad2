"""Comprueba HTTP local, incluida la redireccion del administrador."""
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import build_opener, HTTPRedirectHandler, urlopen

puerto = int(sys.argv[1])
base = f'http://127.0.0.1:{puerto}'
for intento in range(40):
    try:
        with urlopen(base + '/admin/login/', timeout=2) as respuesta:
            assert respuesta.status == 200
        break
    except URLError:
        time.sleep(0.25)
else:
    raise SystemExit('Servidor sin respuesta; revisar el log de inicio.')


class SinRedireccion(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


sin_redireccion = build_opener(SinRedireccion())
try:
    sin_redireccion.open(base + '/admin/')
    raise AssertionError('Se esperaba redireccion al login')
except HTTPError as respuesta:
    assert respuesta.code == 302
    print('GET /admin/:', respuesta.code, 'Location:', respuesta.headers['Location'])
for ruta, esperado in [('/', 200), ('/admin/login/', 200), ('/api/', 404), ('/pedidos/', 404)]:
    try:
        with urlopen(base + ruta, timeout=5) as respuesta:
            codigo = respuesta.status
            cuerpo = respuesta.read()
            if ruta == '/':
                assert b'install worked successfully' in cuerpo.lower()
    except HTTPError as respuesta:
        codigo = respuesta.code
    print('GET', ruta, codigo)
    assert codigo == esperado, (ruta, codigo, esperado)
print('HTTP_OK:', base)
