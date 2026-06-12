# 🛒 API E-commerce do JonesZ — Avaliação de Backend

Esta é uma API REST desenvolvida com **FastAPI**, utilizando **SQLAlchemy** para mapeamento de dados (ORM) e **PostgreSQL** provisionado via Docker.

O projeto inclui uma suíte completa de **testes automatizados com Pytest**, executados contra um banco de dados real e isolado, garantindo confiabilidade e independência entre os cenários de teste.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Docker & Docker Compose
- Pytest
- FastAPI TestClient

---

## 🚀 Como subir o banco de testes

A infraestrutura conta com dois bancos de dados separados:

| Ambiente             | Porta  |
| -------------------- | ------ |
| Desenvolvimento      | `5432` |
| Testes Automatizados | `5433` |

Para iniciar **apenas o banco de testes** em segundo plano, execute na raiz do projeto:

```bash
docker-compose up -d db_test
```

> **Observação:** O banco de testes não utiliza volume nomeado, garantindo que os dados sejam descartados após a destruição do container.

---

## 🧪 Como executar os testes

Com o banco de testes em execução, rode a suíte de testes juntamente com o relatório de cobertura:

```bash
pytest --cov=main -v
```

Ou utilize o comando completo de validação:

```bash
docker-compose up -d db_test && pytest --cov=main -v
```

---

## 📸 Saída Esperada do Pytest

Abaixo está um exemplo de execução bem-sucedida da suíte de testes, com **100% dos testes aprovados** e **92% de cobertura de código**.

```text
$ docker-compose up -d db_test && pytest --cov=main -v

[+] Running 1/1
✔ Container provp2proffabricio-db_test-1 Running

=============================================== test session starts ===============================================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0

collected 12 items

tests/test_produtos.py::test_listar_produtos_vazio PASSED
tests/test_produtos.py::test_criar_produto PASSED
tests/test_produtos.py::test_criar_e_listar PASSED
tests/test_produtos.py::test_buscar_produto_sucesso PASSED
tests/test_produtos.py::test_buscar_produto_404 PASSED
tests/test_produtos.py::test_deletar_produto PASSED
tests/test_produtos.py::test_deletar_e_confirmar PASSED
tests/test_produtos.py::test_deletar_produto_404 PASSED
tests/test_produtos.py::test_criar_produto_invalido_422[payload0] PASSED
tests/test_produtos.py::test_criar_produto_invalido_422[payload1] PASSED
tests/test_produtos.py::test_criar_produto_invalido_422[payload2] PASSED
tests/test_produtos.py::test_validar_isolamento PASSED

================================================= tests coverage ==================================================

Name      Stmts   Miss  Cover
-----------------------------
main.py      59      5    92%
-----------------------------
TOTAL        59      5    92%

========================================= 12 passed, 2 warnings in 0.78s =========================================
```

---

## 🛡️ Isolamento entre os Testes

Para garantir que nenhum teste seja afetado pelo estado deixado por execuções anteriores, o projeto utiliza uma fixture principal chamada `client`, localizada em `conftest.py`.

O fluxo de isolamento ocorre da seguinte forma:

### 1️⃣ Criação do ambiente

Antes de cada teste, a instrução abaixo recria as tabelas no banco de testes:

```python
Base.metadata.create_all(bind=engine)
```

### 2️⃣ Override da dependência

A dependência `get_db` da aplicação principal é substituída dinamicamente através de:

```python
app.dependency_overrides
```

Dessa forma, cada teste utiliza exclusivamente o banco `db_test`.

### 3️⃣ Execução

A fixture entrega um `TestClient` através de `yield`, permitindo a execução das validações da API.

### 4️⃣ Teardown

Após a conclusão do teste, todas as tabelas são removidas:

```python
Base.metadata.drop_all(bind=engine)
```

Isso garante que:

- Nenhum registro permaneça após o teste;
- Cada cenário seja executado em ambiente limpo;
- Os testes sejam totalmente independentes e reproduzíveis.

---

## ✅ Resultados

- 12 testes automatizados
- 100% dos testes aprovados
- 92% de cobertura de código
- Banco de dados isolado para testes
- Ambiente reproduzível com Docker
- Estrutura preparada para evolução e manutenção

```

```

👨‍💻 Autor: João Victor Elizeu Silva(JonesZ)
Graduando em Engenharia de Software pela Universidade de Vassouras em Maricá.