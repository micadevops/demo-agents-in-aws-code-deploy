from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def _pagina(texto):
    return f"<html><body><h1>{texto}</h1></body></html>"


def responder(path):
    """Devuelve (status, body) para un path con query, sin levantar el servidor."""
    url = urlparse(path)
    if url.path == "/":
        return 200, _pagina("Hola mundo")
    if url.path == "/saludo":
        nombre = parse_qs(url.query).get("nombre", [""])[0] or "desconocido"
        return 200, _pagina(f"Hola, {escape(nombre)}")
    return 404, _pagina("No encontrado")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = responder(self.path)
        datos = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
