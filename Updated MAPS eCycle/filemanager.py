import json
import os
from decimal import Decimal


class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.cart_file = os.path.join(self.base_path, "cart.json")
        self.wishlist_file = os.path.join(self.base_path, "wishlist.json")
        self.nego_file = os.path.join(self.base_path, "negotiations.json")
        self.inspection_file = os.path.join(self.base_path, "inspection_data.json")


        self.cart_data = self._load_json(self.cart_file, {})
        self.wishlist_data = self._load_json(self.wishlist_file, {})
        self.nego_data = self._load_json(self.nego_file, {})
        self.inspection_data = self._load_json(self.inspection_file, {})

    def _load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                   
                    if not isinstance(data, dict):
                        return default
                    return data
            except:
                return default
        return default


    def _save_json(self, path, data):
        def convert(obj):
            if isinstance(obj, list):
                return [convert(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return float(obj)
            else:
                return obj

        with open(path, "w") as f:
            json.dump(convert(data), f, indent=4)

    # -----------     CART      -----------------

    def add_to_cart(self, buyer_id, product, quantity):
        buyer_id = str(buyer_id)
        for item in self.cart_data[buyer_id]:
            if item[0] == product[0]: 
                available_qty = product[4] 
                new_qty = item[4] + quantity
                item[4] = min(new_qty, available_qty) 
                self._save_json(self.cart_file, self.cart_data)
                return

        quantity = min(quantity, product[4])
        self.cart_data[buyer_id].append([product[0], product[1], product[2], product[3], quantity])
        self._save_json(self.cart_file, self.cart_data)

    def get_cart(self, buyer_id):
        return self.cart_data.get(str(buyer_id), [])

    def update_cart_quantity(self, buyer_id, inventory_id, change, stock):
        buyer_id = str(buyer_id)
        if buyer_id not in self.cart_data:
            self.cart_data[buyer_id] = []
        for i, item in enumerate(self.cart_data[buyer_id]):
            if item[0] == inventory_id:
                new_qty = item[4] + change
                if new_qty <= 0:
                    self.cart_data[buyer_id].pop(i)
                elif new_qty > stock:
                    return
                else:
                    self.cart_data[buyer_id][i][4] = new_qty
                break
        self._save_json(self.cart_file, self.cart_data)

    def add_to_cart(self, buyer_id, product, quantity):
        buyer_id = str(buyer_id)

        if buyer_id not in self.cart_data:
            self.cart_data[buyer_id] = []

        for item in self.cart_data[buyer_id]:
            if item[0] == product[0]:  # product_id
                item[4] += quantity     # quantity
                break
        else:
            self.cart_data[buyer_id].append([
                product[0],  # product_id
                product[1],  # name
                product[2],  # price
                product[3],  # category
                quantity,
                product[5]
            ])

        self._save_json(self.cart_file, self.cart_data)



    def remove_from_cart(self, buyer_id, inventory_id):
        buyer_id = str(buyer_id)
        if buyer_id in self.cart_data:
            self.cart_data[buyer_id] = [item for item in self.cart_data[buyer_id] if item[0] != inventory_id]
            self._save_json(self.cart_file, self.cart_data)

    def clear_cart(self, buyer_id):
        buyer_id = str(buyer_id)
        if buyer_id in self.cart_data:
            self.cart_data[buyer_id] = []
            self._save_json(self.cart_file, self.cart_data)


    # -----------     wishlist     -----------------

    def add_to_wishlist(self, buyer_id, product):
        buyer_id = str(buyer_id)
        if buyer_id not in self.wishlist_data:
            self.wishlist_data[buyer_id] = []
        if not any(item[0] == product[0] for item in self.wishlist_data[buyer_id]):
            self.wishlist_data[buyer_id].append([product[0], product[1], product[2], product[3], product[4], product[5]])
        self._save_json(self.wishlist_file, self.wishlist_data)

    def get_wishlist(self, buyer_id):
        return self.wishlist_data.get(str(buyer_id), [])

    def remove_from_wishlist(self, buyer_id, inventory_id):
        buyer_id = str(buyer_id)
        if buyer_id in self.wishlist_data:
            self.wishlist_data[buyer_id] = [item for item in self.wishlist_data[buyer_id] if item[0] != inventory_id]
            self._save_json(self.wishlist_file, self.wishlist_data)

    # -----------     negotiations      -----------------

    def add_negotiation_message(self, seller_id, sender, message):
        seller_id = str(seller_id)
        if seller_id not in self.nego_data:
            self.nego_data[seller_id] = []
        self.nego_data[seller_id].append({
            "sender": sender,
            "message": message
        })
        self._save_json(self.nego_file, self.nego_data)

    def get_negotiations(self, seller_id):
        return self.nego_data.get(str(seller_id), [])
    
    # ----------        inspection        ------------------------

    def save_inspection_data(self, product_id, price, condition):
        self.inspection_data[str(product_id)] = {
            "price": price,
            "condition": condition
        }
        self._save_json(self.inspection_file, self.inspection_data)

    def get_inspection_data(self, product_id):
        return self.inspection_data.get(str(product_id), {})

    def get_all_inspection_data(self):
        return self.inspection_data