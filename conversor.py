import math
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs

PUERTO = 8001
UNIDADES = ("C", "F", "K")

OPCIONES = "".join(f'<option value="{u}">{u}</option>' for u in UNIDADES)


def _pagina(cuerpo):
    return f"<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>Conversor</title></head><body>{cuerpo}</body></html>"


def _error(mensaje):
    return 400, _pagina(f'<p>Error: {escape(mensaje)}</p><a href="/">Volver al inicio</a>')


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


def responder(ruta):
    """Devuelve (status, html) para una ruta con query string."""
    partes = urlsplit(ruta)
    if partes.path == "/":
        return 200, _pagina(
            '<form action="/convertir" method="get">'
            '<input type="text" name="valor">'
            f'<select name="desde">{OPCIONES}</select>'
            f'<select name="hacia">{OPCIONES}</select>'
            '<button type="submit">Convertir</button></form>'
        )
    if partes.path != "/convertir":
        return 404, _pagina('<p>No encontrado</p><a href="/">Volver al inicio</a>')

    q = parse_qs(partes.query, keep_blank_values=True)
    texto = q.get("valor", [""])[0].strip()
    desde = q.get("desde", [""])[0].strip().upper()
    hacia = q.get("hacia", [""])[0].strip().upper()

    if desde not in UNIDADES:
        return _error(f"Unidad de origen desconocida: {desde}")
    if hacia not in UNIDADES:
        return _error(f"Unidad de destino desconocida: {hacia}")
    try:
        valor = float(texto)
        if not math.isfinite(valor):
            raise ValueError
    except ValueError:
        return _error(f"El valor no es un número: {texto}")

    kelvin = _a_kelvin(valor, desde)
    if kelvin < -1e-9:
        return _error("La temperatura está por debajo del cero absoluto")
    resultado = round(_desde_kelvin(max(kelvin, 0.0), hacia), 2)
    return 200, _pagina(
        f'<p>{escape(texto)} °{desde} = {resultado} °{hacia}</p>'
        '<a href="/">Volver al inicio</a>'
    )


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, html = responder(self.path)
        datos = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


def main():
    HTTPServer(("", PUERTO), Handler).serve_forever()


if __name__ == "__main__":
    main()
