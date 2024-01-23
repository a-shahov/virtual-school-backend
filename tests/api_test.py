import pytest


@pytest.mark.asyncio
async def registration_test(backend_client, reg_data):
    cli = await backend_client
    resp = await cli.post('/auth/registration', json=reg_data)
    print(await resp.text())
    assert resp.status == 200
    