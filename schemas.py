from decimal import Decimal
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, validator


class Side(str, Enum):
    BUY = 'buy'
    SELL = 'sell'

    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class Order(BaseModel):
    isin: str = Field(max_length=12, min_length=12)
    limit_price: Decimal = Field(gt=0)
    side: Side
    valid_until: int = Field(gt=0)
    quantity: int = Field(gt=0)

    class Config:
        schema_extra = {
            'example': {
                'isin': 'ABCD',
                'limit_price': '3.15',
                'side': 'sell',
                'valid_until': 1928745983,
                'quantity': 3,
            }
        }


class Orders(BaseModel):
    items: List[Order]

    @validator('items')
    def validate_items_size(cls, v):
        if len(v) == 0:
            raise ValueError('Order list is empty.')
        return v

    class Config:
        schema_extra = {
            'example': {
                'items': [
                    {
                        'isin': '123456789009',
                        'limit_price': 1,
                        'side': 'buy',
                        'valid_until': 1345346246,
                        'quantity': 3
                    }
                ]
            }
        }