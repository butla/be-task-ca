from typing import List
from uuid import UUID
from pydantic import BaseModel, field_serializer


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    shipping_address: str | None


# TODO make the models related
class CreateUserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    shipping_address: str | None


class AddToCartRequest(BaseModel):
    item_id: UUID
    quantity: int

    @field_serializer("item_id")
    def serialize_item_id(self, item_id: UUID, _info):
        del _info  # unused
        return str(item_id)


class AddToCartResponse(BaseModel):
    items: List[AddToCartRequest]
