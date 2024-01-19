class ShoppingCart:
    def __init__(self):
        self.products = {
            "Product A": {"price": 20, "quantity": 0, "gift_wrap": 0},
            "Product B": {"price": 40, "quantity": 0, "gift_wrap": 0},
            "Product C": {"price": 50, "quantity": 0, "gift_wrap": 0}
        }
        self.discount_rules = {
            "flat_10_discount": {"threshold": 200, "discount_amount": 10},
            "bulk_5_discount": {"threshold": 10, "discount_percent": 5},
            "bulk_10_discount": {"threshold": 20, "discount_percent": 10},
            "tiered_50_discount": {"quantity_threshold": 30, "single_product_threshold": 15, "discount_percent": 50}
        }
        self.gift_wrap_fee = 1
        self.shipping_fee_per_package = 5
        self.units_per_package = 10

    def apply_discount(self, cart_total):
        applicable_discounts = []

        # Apply flat $10 discount if cart total exceeds $200
        if cart_total > self.discount_rules["flat_10_discount"]["threshold"]:
            applicable_discounts.append(("flat_10_discount", self.discount_rules["flat_10_discount"]["discount_amount"]))

        # Apply bulk 5% discount if any single product quantity exceeds 10 units
        for product_name, product_info in self.products.items():
            if product_info["quantity"] > self.discount_rules["bulk_5_discount"]["threshold"]:
                discounted_amount = product_info["quantity"] * product_info["price"] * (
                        self.discount_rules["bulk_5_discount"]["discount_percent"] / 100)
                applicable_discounts.append(("bulk_5_discount", discounted_amount))

        # Apply bulk 10% discount if total quantity exceeds 20 units
        total_quantity = sum(product_info["quantity"] for product_info in self.products.values())
        if total_quantity > self.discount_rules["bulk_10_discount"]["threshold"]:
            discounted_amount = cart_total * (self.discount_rules["bulk_10_discount"]["discount_percent"] / 100)
            applicable_discounts.append(("bulk_10_discount", discounted_amount))

        # Apply tiered 50% discount if total quantity exceeds 30 units and any single product quantity greater than 15
        if total_quantity > self.discount_rules["tiered_50_discount"]["quantity_threshold"]:
            for product_name, product_info in self.products.items():
                if product_info["quantity"] > self.discount_rules["tiered_50_discount"]["single_product_threshold"]:
                    discounted_amount = (product_info["quantity"] - self.discount_rules["tiered_50_discount"][
                        "single_product_threshold"]) * product_info["price"] * (
                                                self.discount_rules["tiered_50_discount"]["discount_percent"] / 100)
                    applicable_discounts.append(("tiered_50_discount", discounted_amount))

        # Choose the most beneficial discount
        if applicable_discounts:
            best_discount = max(applicable_discounts, key=lambda x: x[1])
            return best_discount
        else:
            return None

    def calculate_cost(self):
        subtotal = 0
        cart_total = 0

        # Calculate subtotal and apply discounts
        for product_name, product_info in self.products.items():
            product_total = product_info["quantity"] * product_info["price"]
            subtotal += product_total
        discount_info = self.apply_discount(subtotal)

        if discount_info:
            discount_name, discount_amount = discount_info
            cart_total = subtotal - discount_amount
        else:
            cart_total = subtotal
            discount_name, discount_amount = "No discount applied", 0

        # Calculate shipping fee and gift wrap fee
        shipping_fee = (total_units := sum(product_info["quantity"] for product_info in self.products.values())) // self.units_per_package * self.shipping_fee_per_package
        gift_wrap_fee = sum(product_info["gift_wrap"] for product_info in self.products.values()) * self.gift_wrap_fee

        # Calculate total cost
        total = cart_total + shipping_fee + gift_wrap_fee

        return subtotal, discount_name, discount_amount, shipping_fee, gift_wrap_fee, total

    def display_cart_details(self):
        print("\nShopping Cart Details:")
        print("Product\t\tQuantity\t\tTotal Amount")
        for product_name, product_info in self.products.items():
            print(f"{product_name}\t\t{product_info['quantity']}\t\t\t${product_info['quantity'] * product_info['price']:.2f}")

        subtotal, discount_name, discount_amount, shipping_fee, gift_wrap_fee, total = self.calculate_cost()

        print("\nSubtotal:", f"${subtotal:.2f}")
        print("Discount Applied:", f"{discount_name} - ${discount_amount:.2f}")
        print("Shipping Fee:", f"${shipping_fee:.2f}")
        print("Gift Wrap Fee:", f"${gift_wrap_fee:.2f}")
        print("Total:", f"${total:.2f}")


def main():
    shopping_cart = ShoppingCart()

    for product_name, product_info in shopping_cart.products.items():
        quantity = int(input(f"Enter the quantity of {product_name}: "))
        gift_wrap = input(f"Is {product_name} wrapped as a gift? (yes/no): ").lower() == "yes"
        shopping_cart.products[product_name]["quantity"] = quantity
        shopping_cart.products[product_name]["gift_wrap"] = quantity if gift_wrap else 0

    shopping_cart.display_cart_details()


if __name__ == "__main__":
    main()
