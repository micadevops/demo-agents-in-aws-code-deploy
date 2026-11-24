import servidor


def test_raiz_hola_mundo():
    status, cuerpo = servidor.responder("/")
    assert status == 200
    assert "Hola mundo" in cuerpo
    assert "<html" in cuerpo.lower()


def test_saludo_con_nombre():
    status, cuerpo = servidor.responder("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in cuerpo


def test_saludo_sin_nombre():
    status, cuerpo = servidor.responder("/saludo")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_saludo_nombre_vacio_es_desconocido():
    status, cuerpo = servidor.responder("/saludo?nombre=")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_nombre_se_escapa():
    status, cuerpo = servidor.responder("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_nombre_escapado_urlencoded():
    _, cuerpo = servidor.responder("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    status, _ = servidor.responder("/otra")
    assert status == 404


def test_ruta_similar_404():
    status, _ = servidor.responder("/saludo/extra")
    assert status == 404
