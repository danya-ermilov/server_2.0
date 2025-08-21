import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_update_and_delete(async_client: AsyncClient):
    await async_client.post(
        "/register", json={"username": "charlie", "password": "initpass"}
    )
    resp = await async_client.post(
        "/token", data={"username": "charlie", "password": "initpass"}
    )
    token = resp.json()["access_token"]

    resp = await async_client.put(
        "/users/update",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "charlie",
            "password": "newpass",
            "role": "string",
            "disabled": "false",
        },
    )
    assert resp.status_code == 200, f"token failed: {resp.status_code} {resp.text}"
    assert resp.json()["username"] == "charlie"

    resp = await async_client.post(
        "/token", data={"username": "charlie", "password": "newpass"}
    )
    assert resp.status_code == 200

    resp = await async_client.delete(
        "/users/delete", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code in (200, 204)

    resp = await async_client.delete(
        "/users/delete", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 404
