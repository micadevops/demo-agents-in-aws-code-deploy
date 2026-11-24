import pytest

from conversor import manejar_peticion


def test_inicio_formulario():
    status, html = manejar_peticion("/")
    assert status == 200
    assert "<form" in html
    assert "/convertir" in html
    assert "Convertir" in html
    assert html.count("<select") == 2
    assert "<input" in html
    for u in ("C", "F", "K"):
        assert u in html


def test_c_a_f():
    status, html = manejar_peticion("/convertir?valor=100&desde=C&hacia=F")
    assert status == 200
    assert "100 °C = 212.0 °F" in html


def test_link_volver():
    _, html = manejar_peticion("/convertir?valor=100&desde=C&hacia=F")
    assert 'href="/"' in html


def test_c_a_k():
    status, html = manejar_peticion("/convertir?valor=0&desde=C&hacia=K")
    assert status == 200
    assert "273.15 °K" in html


def test_minusculas():
    status, html = manejar_peticion("/convertir?valor=100&desde=c&hacia=f")
    assert status == 200
    assert "212.0 °F" in html


def test_redondeo_2_decimales():
    status, html = manejar_peticion("/convertir?valor=1&desde=F&hacia=C")
    assert status == 200
    assert "-17.22 °C" in html


def test_k_a_c():
    _, html = manejar_peticion("/convertir?valor=0&desde=K&hacia=C")
    assert "-273.15 °C" in html


def test_unidad_desconocida():
    status, html = manejar_peticion("/convertir?valor=1&desde=X&hacia=C")
    assert status == 400
    assert html


def test_unidad_destino_desconocida():
    status, _ = manejar_peticion("/convertir?valor=1&desde=C&hacia=Z")
    assert status == 400


def test_valor_no_numerico():
    status, _ = manejar_peticion("/convertir?valor=abc&desde=C&hacia=F")
    assert status == 400


def test_valor_vacio_o_faltante():
    assert manejar_peticion("/convertir?valor=&desde=C&hacia=F")[0] == 400
    assert manejar_peticion("/convertir")[0] == 400


@pytest.mark.parametrize("u,v", [("C", "-300"), ("F", "-500"), ("K", "-1")])
def test_bajo_cero_absoluto(u, v):
    status, _ = manejar_peticion(f"/convertir?valor={v}&desde={u}&hacia=K")
    assert status == 400


def test_cero_absoluto_valido():
    status, _ = manejar_peticion("/convertir?valor=-273.15&desde=C&hacia=K")
    assert status == 200


def test_escapa_valor():
    status, html = manejar_peticion("/convertir?valor=<script>&desde=C&hacia=F")
    assert status == 400
    assert "<script>" not in html


def test_escapa_unidad():
    status, html = manejar_peticion("/convertir?valor=1&desde=<script>&hacia=F")
    assert status == 400
    assert "<script>" not in html


def test_404():
    status, _ = manejar_peticion("/otra")
    assert status == 404
