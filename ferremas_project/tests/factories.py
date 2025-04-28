import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

from .factories import (
    UserFactory, 
    CategoryFactory, 
    ProductFactory, 
    BranchFactory,
    BranchInventoryFactory,
    OrderFactory,
    OrderItemFactory,
    PriceHistoryFactory
)

# Registrar factories
register(UserFactory)
register(CategoryFactory)
register(ProductFactory)
register(BranchFactory)
register(BranchInventoryFactory)
register(OrderFactory)
register(OrderItemFactory)
register(PriceHistoryFactory)

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    user = UserFactory(
        user_type='ADMINISTRADOR',
        is_staff=True,
        is_superuser=True,
        is_verified=True
    )
    return user

@pytest.fixture
def authenticated_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def customer_user(db):
    user = UserFactory(
        user_type='CLIENTE',
        is_staff=False,
        is_superuser=False
    )
    return user

@pytest.fixture
def seller_user(db):
    user = UserFactory(
        user_type='VENDEDOR',
        is_staff=True,
        is_superuser=False
    )
    return user

@pytest.fixture
def warehouseman_user(db):
    user = UserFactory(
        user_type='BODEGUERO',
        is_staff=True,
        is_superuser=False
    )
    return user

@pytest.fixture
def accountant_user(db):
    user = UserFactory(
        user_type='CONTADOR',
        is_staff=True,
        is_superuser=False
    )
    return user

@pytest.fixture
def customer_client(customer_user):
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client

@pytest.fixture
def seller_client(seller_user):
    client = APIClient()
    client.force_authenticate(user=seller_user)
    return client

@pytest.fixture
def category_with_products(db):
    category = CategoryFactory()
    ProductFactory.create_batch(5, category=category)
    return category

@pytest.fixture
def branch_with_inventory(db, product):
    branch = BranchFactory()
    BranchInventoryFactory(branch=branch, product=product, stock=100)
    return branch

@pytest.fixture
def order_with_items(db, customer_user, branch):
    order = OrderFactory(user=customer_user, branch=branch)
    products = ProductFactory.create_batch(3)
    for product in products:
        OrderItemFactory(order=order, product=product)
    return order