from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def _pagina(texto):
    return f"<html><body><h1>{texto}</h1></body></html>"


def obtener_respuesta(ruta_con_query):
    """Devuelve (status, cuerpo_html) sin necesitar el servidor."""
    url = urlparse(ruta_con_query)
    if url.path == "/":
        return 200, _pagina("Hola mundo")
    if url.path == "/saludo":
        nombre = parse_qs(url.query).get("nombre", ["desconocido"])[0]
        return 200, _pagina("Hola, " + escape(nombre))
    return 404, _pagina("No encontrado")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, cuerpo = obtener_respuesta(self.path)
        datos = cuerpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
