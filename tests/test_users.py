import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_update_and_delete(async_client: AsyncClient):
    await async_client.post("/register", json={
        "username": "charlie",
        "password": "initpass"
    })
    resp = await async_client.post("/token", data={
        "username": "charlie",
        "password": "initpass"
    })
    token = resp.json()["access_token"]

    resp = await async_client.put("/update/charlie",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "charlie",
            "password": "newpass",
            "role": "string",
            "disabled": "false"
        }
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "charlie"

    resp = await async_client.post("/token", data={
        "username": "charlie",
        "password": "newpass"
    })
    assert resp.status_code == 200

    resp = await async_client.delete("/users/delete/charlie",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code in (200, 204)

    resp = await async_client.delete("/users/delete/charlie",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 401
