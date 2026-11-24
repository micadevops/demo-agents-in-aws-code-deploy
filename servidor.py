import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PUERTO = 8000


def _pagina(texto):
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body><h1>{texto}</h1></body></html>"


def responder(path):
    """Devuelve (status, cuerpo) para una ruta con query string."""
    url = urlparse(path)
    if url.path == "/":
        return 200, _pagina("Hola mundo")
    if url.path == "/saludo":
        nombre = parse_qs(url.query).get("nombre", [""])[0] or "desconocido"
        return 200, _pagina("Hola, " + html.escape(nombre))
    return 404, _pagina("No encontrado")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, cuerpo = responder(self.path)
        datos = cuerpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


if __name__ == "__main__":
    HTTPServer(("", PUERTO), Handler).serve_forever()
