import pytest
from src.Shop import (
    Product, ShoppingCart, InvalidQuantityError, 
    InsufficientStockError, ProductNotFoundError, 
    ItemNotInCartError, InvalidPromoCodeError
)

@pytest.fixture
def catalog():
    p1 = Product(product_id="p1", name="Ноутбук", price=1000.0, stock=10)
    p2 = Product(product_id="p2", name="Мышь", price=50.0, stock=5)
    return {"p1": p1, "p2": p2}

@pytest.fixture
def cart(catalog):
    return ShoppingCart(product_catalog=catalog)

def test_create_valid_product():
    product = Product(product_id="p3", name="Товар", price=100.0, stock=10)
    assert product.id == "p3"
    assert product.name == "Товар"
    assert product.price == 100.0
    assert product.stock == 10

def test_create_product_empty_id():
    with pytest.raises(ValueError):
        Product(product_id="", name="Товар", price=100.0, stock=10)


def test_create_product_negative_price():
    with pytest.raises(ValueError):
        Product(product_id="p1", name="Товар", price=-10.0, stock=10)


def test_create_product_negative_stock():
    with pytest.raises(ValueError):
        Product(product_id="p1", name="Товар", price=100.0, stock=-1)



def test_add_item_success(cart):
    cart.add_item("p1", 3)
    assert cart.items["p1"] == 3

def test_add_item_increase_quantity(cart):
    cart.add_item("p1", 3)
    cart.add_item("p1", 2)
    assert cart.items["p1"] == 5

def test_add_item_zero_quantity(cart):
    with pytest.raises(InvalidQuantityError, match="Количество должно быть больше нуля"):
        cart.add_item("p1", 0)

def test_add_item_negative_quantity(cart):
    with pytest.raises(InvalidQuantityError, match="Количество должно быть больше нуля"):
        cart.add_item("p1", -5)



