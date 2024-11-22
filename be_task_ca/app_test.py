import http
import uuid

import httpx
import pytest
import faker

from be_task_ca import common
from be_task_ca.user import schema as user_schema
from be_task_ca.item import schema as item_schema


APP_URL = f"http://localhost:{common.APP_PORT}"


@pytest.mark.integrated
def test_app_responds_on_root_url() -> None:
    """Test that goes through the entire application, showing that it's working."""
    response = httpx.get(f"{APP_URL}")
    assert response.status_code == http.HTTPStatus.OK


@pytest.fixture
def _faker() -> faker.Faker:
    return faker.Faker()


@pytest.fixture
def user_create_payload(_faker: faker.Faker) -> user_schema.CreateUserRequest:
    return user_schema.CreateUserRequest(
        first_name="Bob",
        last_name="Martin",
        # This needs to be unique.
        # TODO Faker defaults might not have enough entropy, so this would need to be tweaked.
        email=_faker.email(),
        password="letmein",
        shipping_address="Schmetterlinghaus Hofburg Burggarten, 1010 Wien, Austria",
    )


@pytest.fixture
def item_create_payload(_faker: faker.Faker) -> item_schema.CreateItemRequest:
    return item_schema.CreateItemRequest(
        name=_faker.pystr(min_chars=16, prefix="item_"),
        description=_faker.pystr(min_chars=20, prefix="descr_"),
        price=_faker.pyfloat(min_value=0.1),
        # At least one, to make the positive test easier.
        quantity=_faker.pyint(min_value=1, max_value=1000000),
    )


# Yes, this test will result in garbage building up in the database.
# That's not a problem, as this might sometimes lead to errors, which leads to uncovering bugs.
# So the tests are doing what they're supposed to - find issues in the code.
#
# TODO factor out our apps API usage into test utils.
@pytest.mark.integrated
def test_create_user_items_and_cart(
    user_create_payload: user_schema.CreateUserRequest,
    item_create_payload: item_schema.CreateItemRequest,
) -> None:
    """
    Test that goes through the entire application, showing that it's working.
    Tests like these are very useful when we need to refactor an untested application fast.
    """
    # Stage 1 - create a user =============
    #
    # Using the schema objects here might be dangerous,
    # since we can change and thus break the interface for external clients.
    # But since we should do code reviews, changes to the schema/interface objects would be examined with care.
    user_response = httpx.post(
        f"{APP_URL}/users/", json=user_create_payload.model_dump()
    )

    # TODO should be changed to 201
    assert user_response.status_code == http.HTTPStatus.OK
    # We should get the same values as in the creation payload, plus an ID, minus the password.
    user_response_values = set(user_response.json().values())
    expected_user_response_values = set(user_create_payload.model_dump().values()) - {
        user_create_payload.password
    }
    assert user_response_values.issuperset(expected_user_response_values)
    # Checking that the 'id' field is a UUID
    user_id = uuid.UUID(user_response.json()["id"])

    # Stage 2 - create an item =============
    item_response = httpx.post(
        f"{APP_URL}/items/", json=item_create_payload.model_dump()
    )

    # TODO should be changed to 201
    assert user_response.status_code == http.HTTPStatus.OK
    item_response_values = set(item_response.json().values())
    expected_item_response_values = set(item_create_payload.model_dump().values())
    assert item_response_values.issuperset(expected_item_response_values)
    item_id = uuid.UUID(item_response.json()["id"])

    # Stage 3 - add item to cart ===========
    cart_quantity = 1
    add_to_cart_payload = user_schema.AddToCartRequest(
        item_id=item_id, quantity=cart_quantity
    )
    expected_cart_items = [{"item_id": str(item_id), "quantity": cart_quantity}]
    user_cart_url = f"{APP_URL}/users/{user_id}/cart"

    add_to_cart_response = httpx.post(
        user_cart_url, json=add_to_cart_payload.model_dump()
    )

    assert add_to_cart_response.status_code == http.HTTPStatus.OK
    assert add_to_cart_response.json()["items"] == expected_cart_items

    # Stage 4 - check cart =============
    get_cart_response = httpx.get(user_cart_url)

    assert get_cart_response.status_code == http.HTTPStatus.OK
    assert get_cart_response.json()["items"] == expected_cart_items

    # TODO factor out the asserts into smaller focused tests
