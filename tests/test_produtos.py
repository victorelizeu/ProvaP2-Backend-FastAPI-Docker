import pytest


def test_listar_produtos_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto(client):
    response = client.post(
        "/produtos", json={"nome": "Teclado Mecânico", "preco": 300.0, "estoque": 5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nome"] == "Teclado Mecânico"


def test_criar_e_listar(client):
    client.post("/produtos", json={"nome": "Mouse Gamer", "preco": 150.0})
    response = client.get("/produtos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Mouse Gamer"


def test_buscar_produto_sucesso(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.get(f"/produtos/{id_produto}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Base"


def test_buscar_produto_404(client):
    response = client.get("/produtos/999")
    assert response.status_code == 404


def test_deletar_produto(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.delete(f"/produtos/{id_produto}")
    assert response.status_code == 204


def test_deletar_e_confirmar(client, produto_existente):
    id_produto = produto_existente["id"]
    client.delete(f"/produtos/{id_produto}")
    response = client.get(f"/produtos/{id_produto}")
    assert response.status_code == 404


def test_deletar_produto_404(client):
    response = client.delete("/produtos/999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 10.0},
        {"nome": "Monitor", "preco": 0},
        {"nome": "Cadeira", "preco": -15.0},
    ],
)
def test_criar_produto_invalido_422(client, payload):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_validar_isolamento(client):
    response = client.get("/produtos")
    assert response.json() == []
