import math
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs

UNIDADES = ("C", "F", "K")


def _pagina(cuerpo):
    return ("<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
            "<title>Conversor de temperaturas</title></head><body>"
            + cuerpo + "</body></html>")


def _opciones():
    return "".join(f'<option value="{u}">{u}</option>' for u in UNIDADES)


def _inicio():
    return _pagina(
        "<h1>Conversor de temperaturas</h1>"
        '<form action="/convertir" method="get">'
        '<input type="text" name="valor">'
        f'<select name="desde">{_opciones()}</select>'
        f'<select name="hacia">{_opciones()}</select>'
        '<button type="submit">Convertir</button></form>')


def _error(mensaje):
    return 400, _pagina(f"<p>Error: {escape(mensaje)}</p>"
                        '<a href="/">Volver al inicio</a>')


def _a_kelvin(v, u):
    if u == "C":
        return v + 273.15
    if u == "F":
        return (v - 32) * 5 / 9 + 273.15
    return v


def _desde_kelvin(k, u):
    if u == "C":
        return k - 273.15
    if u == "F":
        return (k - 273.15) * 9 / 5 + 32
    return k


def _convertir(params):
    texto = params.get("valor", [""])[0].strip()
    desde = params.get("desde", [""])[0].strip().upper()
    hacia = params.get("hacia", [""])[0].strip().upper()
    if desde not in UNIDADES:
        return _error(f"Unidad de origen desconocida: {desde}")
    if hacia not in UNIDADES:
        return _error(f"Unidad de destino desconocida: {hacia}")
    try:
        valor = float(texto)
    except ValueError:
        return _error(f"El valor no es un número: {texto}")
    if not math.isfinite(valor):
        return _error(f"El valor no es un número válido: {texto}")
    k = _a_kelvin(valor, desde)
    if k < -1e-9:
        return _error("La temperatura está por debajo del cero absoluto")
    resultado = round(_desde_kelvin(max(k, 0.0), hacia), 2)
    return 200, _pagina(
        f"<p>{escape(texto)} °{desde} = {resultado} °{hacia}</p>"
        '<a href="/">Volver al inicio</a>')


def manejar_peticion(ruta_con_query):
    partes = urlsplit(ruta_con_query)
    if partes.path == "/":
        return 200, _inicio()
    if partes.path == "/convertir":
        return _convertir(parse_qs(partes.query, keep_blank_values=True))
    return 404, _pagina("<p>No encontrado</p>")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, html = manejar_peticion(self.path)
        cuerpo = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


if __name__ == "__main__":
    HTTPServer(("", 8001), Handler).serve_forever()
