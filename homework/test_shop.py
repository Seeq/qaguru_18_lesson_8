"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product_postcard():
    return Product("postcard", 10, "This is a postcard", 1000)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product_book):
        assert product_book.check_quantity(product_book.quantity)

    def test_product_buy(self, product_book):
        quantity_before = product_book.quantity
        to_buy = 100
        product_book.buy(to_buy)
        assert product_book.quantity == quantity_before - to_buy

    def test_product_buy_more_than_available(self, product_book):
        with pytest.raises(ValueError, match='Not enough products in stock'):
            product_book.buy(product_book.quantity + 1)


class TestCart:

    def test_add_new_product(self, cart, product_book, product_postcard):
        cart.add_product(product_book, 10)
        cart.add_product(product_postcard, 20)
        assert cart.products[product_book] == 10
        assert cart.products[product_postcard] == 20

    def test_add_an_existing_product(self, cart, product_book):
        cart.add_product(product_book, 10)
        cart.add_product(product_book, 20)
        assert cart.products[product_book] == 30

    def test_partial_remove_product(self, cart, product_book, product_postcard):
        cart.add_product(product_book, 50)
        cart.add_product(product_postcard, 20)
        cart.remove_product(product_book, 30)
        cart.remove_product(product_postcard, 10)
        assert cart.products[product_book] == 20
        assert cart.products[product_postcard] == 10

    def test_remove_one_product(self, cart, product_book):
        cart.add_product(product_book, 1)
        cart.remove_product(product_book, 1)
        assert len(cart.products) == 0

    def test_total_remove_product(self, cart, product_book):
        cart.add_product(product_book, 500)
        cart.remove_product(product_book)
        assert len(cart.products) == 0

    def test_total_remove_product_more_than_available(self, cart, product_book):
        cart.add_product(product_book, 5)
        cart.remove_product(product_book, 6)
        assert len(cart.products) == 0

    def test_clear_cart(self, cart, product_book, product_postcard):
        cart.add_product(product_book, 5)
        cart.add_product(product_postcard, 10)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price_from_non_empty_cart(self, cart, product_book, product_postcard):
        quantity_of_purchased_goods = 3
        total_price = (quantity_of_purchased_goods * product_book.price) + (
                quantity_of_purchased_goods * product_postcard.price)
        cart.add_product(product_book, quantity_of_purchased_goods)
        cart.add_product(product_postcard, quantity_of_purchased_goods)
        assert cart.get_total_price() == total_price

    def test_get_total_price_from_empty_cart(self, cart, first_product):
        assert cart.get_total_price() == 0

    def test_buy(self, cart, product_book, product_postcard):
        products_before_purchase = product_book.quantity
        cart.add_product(product_book, 3)
        cart.add_product(product_postcard, 3)
        cart.buy()
        assert product_book.quantity == products_before_purchase - 3
        assert product_postcard.quantity == 997
