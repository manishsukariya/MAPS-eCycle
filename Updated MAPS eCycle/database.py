import mysql.connector as my

class Database:
          def __init__(self, app):
                    self.app = app

                    self.db = my.connect(
                                        host="localhost",
                                        user="root",
                                        password="root",
                                        database="project"
                              )

                    self.cursor = self.db.cursor()

          def new_user(self, role, r_name, r_phone, r_email, r_addr, r_pass):
                    try:
                              self.cursor.execute(f"select * from {role} where phone_no = %s or email = %s", (r_phone, r_email))
                              result = self.cursor.fetchone()
                              if result:
                                        return "Exist"
                              
                              else:
                                        query = f"INSERT INTO {role} (name, phone_no, email, address, password) VALUES (%s, %s, %s, %s, %s)"
                                        self.cursor.execute(query, (r_name, r_phone, r_email, r_addr, r_pass))
                                        self.db.commit()
                                        return "S"
                                        
                    except my.IntegrityError:
                              return "Error: Email or Phone already exists!"
                    except Exception as e:
                              return f"Database Error: {e}"

          def check_user(self, role, l_name, l_pass, l_email):
                    try:
                              query = f"select * from {role} where name = %s and password = %s and email = %s"
                              print(role)
                              self.cursor.execute(query, (l_name, l_pass, l_email))
                              result = self.cursor.fetchone()

                              if result:
                                        return "S"
                              else:
                                        return None

                    except Exception as e:
                              return f"Database Error: {e}"
                    
          def get_buyer_history(self, buyer_id):
                    try:
                            query = f"select o.order_id, i.name as product, oi.total_price, oi.quantity, o.order_date from orders o join order_item oi on o.order_id = oi.order_id join inventory i ON oi.inventory_id = i.inventory_id where o.buyer_id = {buyer_id} order by o.order_date desc"
                            self.cursor.execute(query)
                            result = self.cursor.fetchall()
                            return result
                    
                    except Exception as e:
                            return f"Database Error: {e}"
                    
          def get_buyer_status(self, buyer_id):
                    try:
                            query = f"select o.order_id, p.name as product, oi.quantity, o.order_date, o.status from orders o JOIN order_item oi ON o.order_id = oi.order_id JOIN inventory p ON oi.inventory_id = p.inventory_id WHERE o.buyer_id = {buyer_id} ORDER BY o.order_date DESC"
                            self.cursor.execute(query)
                            result = self.cursor.fetchall()
                            return result
                    
                    except Exception as e:
                            return f"Database Error: {e}"
                    
          def order_details(self, buyer_id, tot, addr):
                    try:
                            query = f"insert into orders (buyer_id, delivery_address, total_amount) values (%s, %s, %s)"
                            self.cursor.execute(query, (buyer_id, addr, tot))
                            self.db.commit()
                            last_order_id = self.cursor.lastrowid
                            if last_order_id:
                                self.order_item_details(last_order_id, buyer_id)
                            else:
                                self.app.be.messagebox.showerror("Error", "Order ID not retrieved.")
                    
                    except Exception as e:
                            return f"Database Error: {e}"
                    
          def order_item_details(self, order_id, buyer_id):
                cart_items = self.app.fm.get_cart(buyer_id)

                try:
                        for item in cart_items:
                                inventory_id = item[0]
                                print(inventory_id)
                                price_per_unit = float(item[3])
                                print(price_per_unit)
                                quantity = int(item[4])
                                print(quantity)

                                query = "INSERT INTO order_item (order_id, inventory_id, quantity, price_per_unit) VALUES (%s, %s, %s, %s)"
                                print("insert")
                                self.cursor.execute(query, (order_id, inventory_id, quantity, price_per_unit, ))
                                
                        
                        self.db.commit()
                        self.app.fm.clear_cart(buyer_id)
                        self.app.be.buyer_pay_screen()  
                        
                except Exception as e:
                        self.db.rollback()
                        self.app.be.messagebox.showerror("Error", f"Failed to save order items: {e}")

          def direct_order_details(self, buyer_id, sale_id, addr):
                try:
                        insert_query = """
                        INSERT INTO direct_sale_order (sale_id, buyer_id, buyer_address, status)
                        VALUES (%s, %s, %s, 'pending')
                        """
                        self.cursor.execute(insert_query, (sale_id, buyer_id, addr))

                        self.db.commit()

                        self.app.be.buyer_direct_pay_screen(sale_id)

                except Exception as e:
                        self.db.rollback()
                        self.app.be.messagebox.showerror("Error", f"Failed to place direct order: {e}")


          def for_payment(self, buyer_id, t):
                  if t == "by":
                        self.app.db.cursor.execute("""
                                SELECT o.order_id, GROUP_CONCAT(CONCAT(i.type, ' - ', i.name) SEPARATOR ', ') AS products, o.total_amount
                                FROM orders o
                                JOIN order_item oi ON o.order_id = oi.order_id
                                JOIN inventory i ON oi.inventory_id = i.inventory_id
                                WHERE o.buyer_id = %s AND o.payment_id IS NULL
                                GROUP BY o.order_id
                        """, (buyer_id,))
                        result = self.app.db.cursor.fetchone()
                        return result
                  
                  elif t == "dir":
                        self.app.db.cursor.execute("""
                          SELECT dso.order_id, 
                                GROUP_CONCAT(CONCAT(ds.brand, ' ', ds.model) SEPARATOR ', ') AS products, 
                                SUM(ds.buyer_price * ds.quantity) AS total_amount
                                FROM direct_sale_order dso
                                JOIN direct_sale ds ON dso.sale_id = ds.sale_id
                                WHERE dso.buyer_id = %s AND dso.status = 'pending'
                                GROUP BY dso.order_id;""", (buyer_id, ))
                        result = self.app.db.cursor.fetchone()
                        return result

          def reduce_inventory_stock(self, order_id):
                try:
                        self.app.db.cursor.execute("""
                        SELECT inventory_id, quantity
                        FROM order_item
                        WHERE order_id = %s
                        """, (order_id,))
                        items = self.app.db.cursor.fetchall()

                        for inventory_id, quantity in items:
                                self.app.db.cursor.execute("""
                                UPDATE inventory
                                SET stock = stock - %s
                                WHERE inventory_id = %s
                        """, (quantity, inventory_id))

                        self.app.db.db.commit()

                except Exception as e:
                        print("Error reducing inventory stock:", e)


          def get_direct_sales(self):
                   try:
                        query = f"SELECT ds.sale_id, s.name AS seller_name, ds.product_type, ds.brand, ds.model, ds.condition, ds.buyer_price, ds.quantity, ds.image_paths FROM direct_sale ds JOIN seller s ON ds.seller_id = s.seller_id and status = 'pending'"
                        self.cursor.execute(query)
                        result = self.cursor.fetchall()
                        return result
                    
                   except Exception as e:
                            return f"Database Error: {e}"
                   
          

                    
          def submit_product(self, id, ty, br, md, con, pr, qty, loc, img):
                    try:
                            query = "insert into product (seller_id, product_type, brand, model, `condition`, price, quantity, pickup_location, image_paths) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            values = (id, ty, br, md, con, pr, qty, loc, img)

                            self.cursor.execute(query, values)
                            self.db.commit()
                            return "S"
                    except Exception as e:
                            return f"Database Error: {e}"
                    
          def get_s2b_product(self):
                    try:
                              query = "select sale_id, product_type, brand, model, condition, buyer_price, quantity from direct_sale"

                              self.cursor.execute(query)
                              result = self.cursor.fetchall()
                              return result

                    except Exception as e:
                          return f"Database Error: {e}"
                    
          def get_product(self):
                    try:
                            query = "select inventory_id, name, type, price_per_unit, stock, image_path from inventory"

                            self.cursor.execute(query)
                            result = self.cursor.fetchall()
                            return result
                    
                    except Exception as e:
                            return f"Database Error: {e}"


                    
          def submit_report_all(self, role, id, type, desc, path):
                    try:
                              column = f"{role}_id"
                              query = f"insert into report ({column}, report_type, description, evidence_path) values (%s, %s, %s, %s)"
                              self.cursor.execute(query, (id, type, desc, path, ))
                              self.db.commit()
                              return "S"
                    except Exception as e:
                            return f"Database Error: {e}"
