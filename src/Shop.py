
class InvalidQuantityError(ValueError):
    pass

class InsufficientStockError(ValueError):
    pass

class ProductNotFoundError(KeyError):
    pass

class ItemNotInCartError(KeyError):
    pass

class InvalidPromoCodeError(ValueError):
    pass


class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if not product_id:
            raise ValueError("ID товара не может быть пустым")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if stock < 0:
            raise ValueError("Количество на складе не может быть отрицательным")

        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock



class ShoppingCart:
    def __init__(self, product_catalog: dict[str, Product]):
        self.product_catalog = product_catalog
        self.items: dict[str, int] = {}
        self.applied_promo = None
        self.promo_codes = {
            "DISCOUNT10": 0.10,
            "SALE20": 0.20,
            "VIP50": 0.50,
        }

    def add_item(self, product_id: str, count: int):
        if count <= 0:
            raise InvalidQuantityError("Количество должно быть больше нуля")
        if product_id not in self.product_catalog:
            raise ProductNotFoundError(f"Товар '{product_id}' не найден")

        product = self.product_catalog[product_id]
        current = self.items.get(product_id, 0)

        if current + count > product.stock:
            raise InsufficientStockError(
                f"Недостаточно '{product.name}' на складе. "
                f"Доступно: {product.stock - current}, запрошено: {count}"
            )

        self.items[product_id] = current + count

    def remove(self, product_id: str, quantity: int = None):
        if product_id not in self.items:
            raise ItemNotInCartError(f"Товар '{product_id}' не в корзине")

        if quantity is None:
            del self.items[product_id]
        else:
            if quantity <= 0:
                raise InvalidQuantityError("Количество для удаления должно быть > 0")
            self.items[product_id] -= quantity
            if self.items[product_id] <= 0:
                del self.items[product_id]

    def apply_promo(self, code: str):
        if code not in self.promo_codes:
            raise InvalidPromoCodeError(f"Промокод '{code}' недействителен")
        self.applied_promo = code

    def clear_promo(self):
        self.applied_promo = None

    def calculate(self) -> float:
        total = 0.0
        for product_id, quantity in self.items.items():
            product = self.product_catalog[product_id]
            total += product.price * quantity

        if self.applied_promo:
            discount = self.promo_codes[self.applied_promo]
            total *= (1 - discount)

        return round(total, 2)