import pytest
import app as app_module
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestHealth:
    def test_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data == {"status": "ok", "service": "users"}


class TestListUsers:
    def test_returns_all_users(self, client):
        resp = client.get("/users")
        assert resp.status_code == 200
        users = resp.get_json()
        assert len(users) == 3

    def test_user_shape(self, client):
        resp = client.get("/users")
        user = resp.get_json()[0]
        assert {"id", "name", "email"} <= user.keys()


class TestGetUser:
    def test_known_user(self, client):
        resp = client.get("/users/1")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Alice"

    def test_unknown_user_returns_404(self, client):
        resp = client.get("/users/99")
        assert resp.status_code == 404
        assert "error" in resp.get_json()


class TestUserProducts:
    def _mock_products(self, monkeypatch):
        class _Resp:
            def json(self):
                return [{"id": 1, "name": "Laptop", "price": 999.99, "owner_id": 1}]

        monkeypatch.setattr(app_module.requests, "get", lambda *a, **kw: _Resp())

    def test_returns_user_and_products(self, client, monkeypatch):
        self._mock_products(monkeypatch)
        resp = client.get("/users/1/products")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["user"]["name"] == "Alice"
        assert len(data["products"]) == 1

    def test_unknown_user_returns_404(self, client, monkeypatch):
        self._mock_products(monkeypatch)
        resp = client.get("/users/99/products")
        assert resp.status_code == 404

    def test_products_service_down_returns_502(self, client, monkeypatch):
        import requests as req_lib

        monkeypatch.setattr(
            app_module.requests,
            "get",
            lambda *a, **kw: (_ for _ in ()).throw(req_lib.RequestException("down")),
        )
        resp = client.get("/users/1/products")
        assert resp.status_code == 502
