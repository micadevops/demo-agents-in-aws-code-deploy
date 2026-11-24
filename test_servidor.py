import servidor


def _resp(path):
    status, cuerpo = servidor.responder(path)
    if isinstance(cuerpo, bytes):
        cuerpo = cuerpo.decode("utf-8")
    return status, cuerpo


def test_raiz_hola_mundo():
    status, cuerpo = _resp("/")
    assert status == 200
    assert "Hola mundo" in cuerpo
    assert "<html" in cuerpo.lower()


def test_saludo_con_nombre():
    status, cuerpo = _resp("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in cuerpo


def test_saludo_sin_nombre():
    status, cuerpo = _resp("/saludo")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_saludo_nombre_vacio_o_sin_parametro():
    status, cuerpo = _resp("/saludo?otro=x")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_nombre_se_escapa():
    status, cuerpo = _resp("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_nombre_escapado_url_encoded():
    status, cuerpo = _resp("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    assert _resp("/otra")[0] == 404
    assert _resp("/saludo/extra")[0] == 404
    assert _resp("/index.html")[0] == 404


def test_raiz_con_query_sigue_200():
    assert _resp("/?x=1")[0] == 200


def test_servidor_usa_http_server_en_puerto_8000():
    with open("servidor.py", encoding="utf-8") as f:
        fuente = f.read()
    assert "http.server" in fuente
    assert "8000" in fuente
