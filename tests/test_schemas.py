import pytest
from pydantic import ValidationError

from schemas import Order, Orders


@pytest.mark.parametrize('isin,limit_price,side,valid_until,quantity', [
    ('123456789009', '12.32', 'sell', 1928745983, 3),
    ('qwertyuiopqw', '1', 'buy', 1928745983, 1),
    ('ASEFasdfasdf', '1', 'Buy', 1928745983, 1),
    ('ASEFasdfasdf', 1, 'seLL', 1928745983, 1),
])
def test_order__valid_data(isin, limit_price, side, valid_until, quantity):
    Order(
        isin=isin,
        limit_price=limit_price,
        side=side,
        valid_until=valid_until,
        quantity=quantity
    )


@pytest.mark.parametrize('isin', [
    '1234567',
    'qwertyuiopqw111',
])
def test_order__invalid_isin(isin):
    with pytest.raises(ValidationError):
        Order(
            isin=isin,
            limit_price='3.15',
            side='buy',
            valid_until=1928745983,
            quantity=1
        )


@pytest.mark.parametrize('limit_price', [
    0,
    -1,
    'aaa',
])
def test_order__invalid_limit_price(limit_price):
    with pytest.raises(ValidationError):
        Order(
            isin='ASEFasdfasdf',
            limit_price=limit_price,
            side='buy',
            valid_until=1928745983,
            quantity=1
        )


@pytest.mark.parametrize('side', [
    'SELLLLL',
    'rent',
])
def test_order__invalid_side(side):
    with pytest.raises(ValidationError):
        Order(
            isin='ASEFasdfasdf',
            limit_price=1,
            side=side,
            valid_until=1928745983,
            quantity=1
        )


@pytest.mark.parametrize('valid_until', [
    'aaa',
    -1,
])
def test_order__invalid_valid_until(valid_until):
    with pytest.raises(ValidationError):
        Order(
            isin='ASEFasdfasdf',
            limit_price=1,
            side='sell',
            valid_until=valid_until,
            quantity=1
        )


@pytest.mark.parametrize('quantity', [
    'aaa',
    -1,
    0
])
def test_order__invalid_valid_quantity(quantity):
    with pytest.raises(ValidationError):
        Order(
            isin='ASEFasdfasdf',
            limit_price=1,
            side='sell',
            valid_until=1928745983,
            quantity=quantity
        )


def test_orders__empty_list():
    with pytest.raises(ValidationError):
        Orders(items=[])
