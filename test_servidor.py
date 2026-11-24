import servidor


def test_raiz_hola_mundo():
    status, body = servidor.responder("/")
    assert status == 200
    assert "Hola mundo" in body
    assert "<html" in body.lower()


def test_saludo_con_nombre():
    status, body = servidor.responder("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in body


def test_saludo_sin_nombre():
    status, body = servidor.responder("/saludo")
    assert status == 200
    assert "Hola, desconocido" in body


def test_saludo_nombre_vacio_es_desconocido():
    status, body = servidor.responder("/saludo?nombre=")
    assert status == 200
    assert "Hola, desconocido" in body


def test_nombre_se_escapa():
    status, body = servidor.responder("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in body
    assert "&lt;script&gt;" in body


def test_nombre_url_encoded_se_escapa():
    status, body = servidor.responder("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in body
    assert "&lt;script&gt;" in body


def test_ruta_desconocida_404():
    status, _ = servidor.responder("/otra")
    assert status == 404


def test_ruta_desconocida_con_query_404():
    status, _ = servidor.responder("/nada?nombre=Ana")
    assert status == 404
