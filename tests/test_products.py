import uuid
import pytest
from httpx import AsyncClient
from typing import Dict
from app.main import app


async def _register_and_get_token(
    client: AsyncClient, username: str, password: str
) -> str:

    resp = await client.post(
        "/register", json={"username": username, "password": password}
    )
    assert resp.status_code in (
        200,
        201,
    ), f"Register failed ({username}): {resp.status_code} {resp.text}"

    token_resp = await client.post(
        "/token", data={"username": username, "password": password}
    )
    assert (
        token_resp.status_code == 200
    ), f"Token request failed ({username}): {token_resp.status_code} {token_resp.text}"
    token = token_resp.json().get("access_token")
    assert token, f"No access_token returned for {username}: {token_resp.text}"
    return token


def _auth_header(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_create_get_update_delete_product_flow(async_client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "pass123"

    token = await _register_and_get_token(async_client, username, password)
    headers = _auth_header(token)

    create_payload = {"name": "TestChair", "description": "19.99"}
    create_resp = await async_client.post(
        "/products/", json=create_payload, headers=headers
    )
    assert create_resp.status_code in (
        200,
        201,
    ), f"Create product failed: {create_resp.status_code} {create_resp.text}"
    created = create_resp.json()
    assert "id" in created, f"Create response missing id: {created}"
    prod_id = created["id"]
    assert created["name"] == create_payload["name"]

    get_resp = await async_client.get(f"/products/{prod_id}", headers=headers)
    assert (
        get_resp.status_code == 200
    ), f"Get product failed: {get_resp.status_code} {get_resp.text}"
    got = get_resp.json()
    assert got["id"] == prod_id and got["name"] == create_payload["name"]

    update_payload = {"name": "UpdatedChair", "description": "29.99"}
    upd_resp = await async_client.put(
        f"/products/{prod_id}", json=update_payload, headers=headers
    )
    assert (
        upd_resp.status_code == 200
    ), f"Update product failed: {upd_resp.status_code} {upd_resp.text}"
    updated = upd_resp.json()
    assert updated["name"] == update_payload["name"] and updated["id"] == prod_id

    del_resp = await async_client.delete(f"/products/{prod_id}", headers=headers)
    assert del_resp.status_code in (
        200,
        204,
    ), f"Delete product failed: {del_resp.status_code} {del_resp.text}"

    not_found = await async_client.get(f"/products/{prod_id}", headers=headers)
    assert (
        not_found.status_code == 404
    ), f"Expected 404 after delete, got: {not_found.status_code} {not_found.text}"
