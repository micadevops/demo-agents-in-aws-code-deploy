from servidor import obtener_respuesta


def test_raiz_hola_mundo():
    status, cuerpo = obtener_respuesta("/")
    assert status == 200
    assert "Hola mundo" in cuerpo
    assert "<html" in cuerpo.lower()


def test_saludo_con_nombre():
    status, cuerpo = obtener_respuesta("/saludo?nombre=Ana")
    assert status == 200
    assert "Hola, Ana" in cuerpo


def test_saludo_sin_nombre():
    status, cuerpo = obtener_respuesta("/saludo")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_saludo_query_sin_nombre():
    status, cuerpo = obtener_respuesta("/saludo?otro=x")
    assert status == 200
    assert "Hola, desconocido" in cuerpo


def test_nombre_se_escapa():
    status, cuerpo = obtener_respuesta("/saludo?nombre=<script>alert(1)</script>")
    assert status == 200
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_nombre_url_encoded_se_escapa():
    _, cuerpo = obtener_respuesta("/saludo?nombre=%3Cscript%3E")
    assert "<script>" not in cuerpo
    assert "&lt;script&gt;" in cuerpo


def test_ruta_desconocida_404():
    status, _ = obtener_respuesta("/otra")
    assert status == 404


def test_subruta_de_saludo_404():
    status, _ = obtener_respuesta("/saludo/extra")
    assert status == 404
