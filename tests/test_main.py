from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get():
    response = client.get("/orders/orders")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_post__valid():
    response = client.post(
        "/orders/orders",
        json={
            "items": [
                {
                    "isin": "123456789009",
                    "limit_price": 1,
                    "side": "buy",
                    "valid_until": 12342352345,
                    "quantity": 1
                }
            ]
        }
    )
    assert response.status_code == HTTPStatus.OK


def test_post__empty_list():
    response = client.post(
        "/orders/orders",
        json={
            "items": []
        }
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0] == {
        'loc': ['body', 'items'],
        'msg': 'Order list is empty.',
        'type': 'value_error'
    }


def test_post__invalid_data():
    response = client.post(
        "/orders/orders",
        json={
            "items": [
                {
                    "isin": "12345678",
                    "limit_price": -1,
                    "side": "buyyy",
                    "valid_until": 0,
                    "quantity": 0
                }
            ]
        }
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0] == {
        'ctx': {'limit_value': 12},
        'loc': ['body', 'items', 0, 'isin'],
        'msg': 'ensure this value has at least 12 characters',
        'type': 'value_error.any_str.min_length'
    }

    assert response.json()['detail'][1] == {
        'ctx': {'limit_value': 0},
        'loc': ['body', 'items', 0, 'limit_price'],
        'msg': 'ensure this value is greater than 0',
        'type': 'value_error.number.not_gt'
    }

    assert response.json()['detail'][2] == {
        'ctx': {'enum_values': ['buy', 'sell']},
        'loc': ['body', 'items', 0, 'side'],
        'msg': "value is not a valid enumeration member; permitted: 'buy', 'sell'",  # noqa
        'type': 'type_error.enum'
    }

    assert response.json()['detail'][3] == {
        'ctx': {'limit_value': 0},
        'loc': ['body', 'items', 0, 'valid_until'],
        'msg': 'ensure this value is greater than 0',
        'type': 'value_error.number.not_gt'
    }
