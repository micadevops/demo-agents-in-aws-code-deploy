import conversor
from conversor import responder


def test_inicio_formulario():
    status, html = responder("/")
    assert status == 200
    assert "<form" in html
    assert "/convertir" in html
    assert html.count("<select") == 2
    for u in ("C", "F", "K"):
        assert u in html
    assert "Convertir" in html
    assert "<input" in html


def test_c_a_f():
    status, html = responder("/convertir?valor=100&desde=C&hacia=F")
    assert status == 200
    assert "100 °C = 212.0 °F" in html
    assert 'href="/"' in html


def test_c_a_k():
    status, html = responder("/convertir?valor=0&desde=C&hacia=K")
    assert status == 200
    assert "273.15 °K" in html


def test_minusculas():
    status, html = responder("/convertir?valor=100&desde=c&hacia=f")
    assert status == 200
    assert "212.0 °F" in html


def test_redondeo_2_decimales():
    status, html = responder("/convertir?valor=1&desde=C&hacia=F")
    assert status == 200
    assert "33.8 °F" in html
    status, html = responder("/convertir?valor=10&desde=F&hacia=C")
    assert status == 200
    assert "-12.22 °C" in html


def test_misma_unidad():
    status, html = responder("/convertir?valor=50&desde=K&hacia=K")
    assert status == 200
    assert "50.0 °K" in html or "50 °K" in html


def test_unidad_desconocida():
    status, html = responder("/convertir?valor=1&desde=X&hacia=F")
    assert status == 400
    status, html = responder("/convertir?valor=1&desde=C&hacia=Z")
    assert status == 400


def test_valor_no_numerico():
    assert responder("/convertir?valor=abc&desde=C&hacia=F")[0] == 400


def test_parametros_faltantes():
    assert responder("/convertir")[0] == 400
    assert responder("/convertir?valor=&desde=C&hacia=F")[0] == 400


def test_bajo_cero_absoluto():
    assert responder("/convertir?valor=-274&desde=C&hacia=F")[0] == 400
    assert responder("/convertir?valor=-460&desde=F&hacia=C")[0] == 400
    assert responder("/convertir?valor=-1&desde=K&hacia=C")[0] == 400


def test_cero_absoluto_exacto_ok():
    assert responder("/convertir?valor=0&desde=K&hacia=C")[0] == 200
    status, html = responder("/convertir?valor=-273.15&desde=C&hacia=K")
    assert status == 200


def test_mensaje_error_no_vacio():
    status, html = responder("/convertir?valor=abc&desde=C&hacia=F")
    assert status == 400
    assert len(html.strip()) > 0


def test_escape_valor():
    status, html = responder("/convertir?valor=%3Cscript%3Ealert(1)%3C/script%3E&desde=C&hacia=F")
    assert status == 400
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_escape_unidad():
    status, html = responder("/convertir?valor=1&desde=%3Cscript%3E&hacia=F")
    assert status == 400
    assert "<script>" not in html


def test_404():
    assert responder("/otra")[0] == 404
    assert responder("/convertir/x")[0] == 404


def test_puerto_y_main():
    assert hasattr(conversor, "main") or hasattr(conversor, "PUERTO")
