import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from PIL import Image
import json
import os

class Buyer:
          def __init__(self, app):
                    self.app = app
                    
                    self.rating = 0
                    self.star_buttons = []

                    self.anyy = None




          def buyer_shop_screen(self):
                    self.app.clear_frame()
                    if self.app.content_frame:
                              self.app.clear_content()
                    self.app.update_idletasks()

                    self.app.head_content_create("buyer")

                    menu_list = ["Shop", "Direct S to B",  "Cart", "Payment", "Status", "Wishlist", "History", "Feedback", "Report"]

                    self.app.me.menu_flag(menu_list, "buyer")

                    self.buyer_notify()

                    self.app.db.cursor.reset()
                    self.app.db.cursor.execute("select buyer_id from buyer where email=%s",(self.app.p_mail, ))
                    self.buyer_id = self.app.db.cursor.fetchone()[0]


                    ctk.CTkLabel(self.app.content_frame, text="Shop Recycled Products", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.05, anchor="center")

                    self.shop_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#E4E7EB")
                    self.shop_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.9, anchor="center")

                    self.shop_products = self.app.db.get_product()

                    wishlist_items = self.app.fm.get_wishlist(self.buyer_id)

                    for i, product in enumerate(self.shop_products):
                              inventory_id, name, type, price_per_unit, stock, img_path = product

                              row = i // 3  
                              col = i % 3


                              p_frame = ctk.CTkFrame(self.shop_frame, fg_color="white", corner_radius=0, width=280, height=340)
                              p_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                              img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 200))
                              ctk.CTkLabel(p_frame, image=img, text="").pack(pady=5)


                              ctk.CTkLabel(p_frame, text=name, font=("Arial", 18, "bold"), text_color="black").pack(pady=(5, 2))

                                
                              ctk.CTkLabel(p_frame, text=f"₹{price_per_unit}", font=("Arial", 16), text_color="green").pack()

                               
                              ctk.CTkLabel(p_frame, text=f"Category: {type}", font=("Arial", 14), text_color="black").pack()

                              ctk.CTkLabel(p_frame, text=f"Stock: {stock}", font=("Arial", 14), text_color="black").pack()

                              ctk.CTkButton(
                                                p_frame,
                                                text="View Details",
                                                fg_color="#2563EB",
                                                hover_color="#1E3A8A",
                                                command=lambda prod=product: self.show_product_details(prod)
                                                ).pack(pady=10)

                              is_in_wishlist = any(prod[0] == product[0] for prod in wishlist_items)

                              wishlist_symbol = "♥" if is_in_wishlist else "♡"
                              wishlist_btn = ctk.CTkButton(
                                                  p_frame,
                                                  text=wishlist_symbol,
                                                  width=30,
                                                  height=30,
                                                  font=("Imapct", 20, "bold"),
                                                  fg_color="transparent",
                                                  hover_color="#FCA5A5",
                                                  text_color="red"
                                                  )
                              wishlist_btn.configure(command=lambda prod=product, btn=wishlist_btn: self.toggle_wishlist(prod, btn))
                              wishlist_btn.place(relx=0.85, rely=0.05)


                    for col in range(3):
                              self.shop_frame.grid_columnconfigure(col, weight=1)

          def buyer_s_to_b_screen(self):
                self.app.clear_content()

                self.direct_shop_frame = ctk.CTkScrollableFrame(
                        self.app.content_frame,
                        fg_color="#E4E7EB"
                )
                self.direct_shop_frame.place(relx=0.5, rely=0.6, relheight=0.8, relwidth=0.9, anchor="center")

                ctk.CTkLabel(self.app.content_frame, text="Purchase From Seller", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.05, anchor="center")


                direct_products = self.app.db.get_direct_sales()

                for i, product in enumerate(direct_products):
                        sale_id, seller_name, product_type, brand, model, condition, buyer_price, quantity, image_paths = product
                        row = i // 3
                        col = i % 3

                        p_frame = ctk.CTkFrame(self.direct_shop_frame, fg_color="white", corner_radius=0, width=280, height=340)
                        p_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                        imgs_path = json.loads(image_paths)[0] if image_paths else "default.png"
                        img = ctk.CTkImage(light_image=Image.open(imgs_path), size=(200, 200))
                        ctk.CTkLabel(p_frame, image=img, text="").pack(pady=5)

                        ctk.CTkLabel(p_frame, text=f"Sale ID: {sale_id}", font=("Arial", 14), text_color="black").pack()
                        ctk.CTkLabel(p_frame, text=f"Seller: {seller_name}", font=("Arial", 14), text_color="black").pack()
                        ctk.CTkLabel(p_frame, text=f"Type: {product_type}", font=("Arial", 14), text_color="black").pack()
                        ctk.CTkLabel(p_frame, text=f"Condition: {condition}", font=("Arial", 14), text_color="black").pack()
                        ctk.CTkLabel(p_frame, text=f"Price: ₹{buyer_price}", font=("Arial", 14), text_color="green").pack()
                        ctk.CTkLabel(p_frame, text=f"Qty: {quantity}", font=("Arial", 14), text_color="black").pack()

                        ctk.CTkButton(
                        p_frame,
                        text="View Details",
                        fg_color="#2563EB",
                        hover_color="#1E3A8A",
                        command=lambda prod=product: self.show_direct_product_details(prod, sale_id)
                        ).pack(pady=10)

                for col in range(3):
                        self.direct_shop_frame.grid_columnconfigure(col, weight=1)


          def buyer_cart_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(
                        self.app.content_frame,
                        text="Your Cart",
                        text_color="black",
                        font=("Impact", 50)
                ).place(relx=0.5, rely=0.05, anchor="center")

                self.cart_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#E4E7EB")
                self.cart_frame.place(relx=0.5, rely=0.55, relheight=0.7, relwidth=0.9, anchor="center")

                cart_items = self.app.fm.get_cart(self.buyer_id)

                if not cart_items:
                        ctk.CTkLabel(
                        self.cart_frame,
                        text="Your cart is empty.",
                        text_color="gray",
                        font=("Arial", 20, "italic")
                        ).pack(pady=50)
                        return

                self.cart_total = 0

                for i, item in enumerate(cart_items):
                        inventory_id, name, type_, price_per_unit, quantity, img_path = item
                        total_price = float(price_per_unit) * float(quantity)
                        self.cart_total += total_price

                        self.app.db.cursor.execute(f"select stock from inventory where inventory_id = {inventory_id}")
                        stock = self.app.db.cursor.fetchone()[0]

                        row = i // 2
                        col = i % 2

                        c_frame = ctk.CTkFrame(self.cart_frame, fg_color="white", corner_radius=10, width=400, height=180)
                        c_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                        img = ctk.CTkImage(light_image=Image.open(img_path), size=(100, 100))
                        ctk.CTkLabel(c_frame, image=img, text="").place(relx=0.1, rely=0.5, anchor="center")

                        ctk.CTkLabel(c_frame, text=name, font=("Arial", 18, "bold"), text_color="black").place(relx=0.3, rely=0.25, anchor="w")
                        ctk.CTkLabel(c_frame, text=f"₹{price_per_unit} each", font=("Arial", 14), text_color="green").place(relx=0.3, rely=0.45, anchor="w")
                        ctk.CTkLabel(c_frame, text=f"Total: ₹{total_price}", font=("Arial", 14, "bold"), text_color="black").place(relx=0.3, rely=0.65, anchor="w")

                        ctk.CTkButton(
                        c_frame,
                        text="-",
                        width=25,
                        command=lambda inv_id=inventory_id: self.update_cart_qty(inv_id, -1, stock)
                        ).place(relx=0.75, rely=0.5, anchor="center")

                        ctk.CTkLabel(c_frame, text=str(quantity), font=("Arial", 14, "bold"), text_color="black").place(relx=0.82, rely=0.5, anchor="center")

                        ctk.CTkButton(
                        c_frame,
                        text="+",
                        width=25,
                        command=lambda inv_id=inventory_id: self.update_cart_qty(inv_id, 1, stock)
                        ).place(relx=0.89, rely=0.5, anchor="center")

                        ctk.CTkButton(
                        c_frame,
                        text="Remove",
                        fg_color="#EF4444",
                        hover_color="#DC2626",
                        command=lambda inv_id=inventory_id: self.remove_cart_item(inv_id)
                        ).place(relx=0.8, rely=0.8, anchor="center")

                for col in range(2):
                        self.cart_frame.grid_columnconfigure(col, weight=1)

                self.total_label = ctk.CTkLabel(
                        self.app.content_frame,
                        text=f"Total: ₹{self.cart_total}",
                        text_color="black",
                        font=("Impact", 30)
                )
                self.total_label.place(relx=0.5, rely=0.9, anchor="center")

                map_b = ctk.CTkButton(self.app.content_frame, text="Select Delivery Location", fg_color="#2563EB", hover_color="#1E3A8A")
                map_b.place(relx=0.75, rely=0.9, anchor="center")

                pay_btn = ctk.CTkButton(
                        self.app.content_frame,
                        text="Confirm and Pay",
                        fg_color="#2563EB",
                        hover_color="#1E3A8A",
                        command=lambda : self.app.db.order_details(self.buyer_id, self.cart_total, self.delivery_location)
                )

                map_b.configure(command=lambda : self.get_locations(map_b, pay_btn))

      
          def buyer_pay_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(self.app.content_frame, text="Complete Your Payment", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.05, anchor="center")

                pay_frame = ctk.CTkFrame(self.app.content_frame, fg_color="white")
                pay_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.95, anchor="center")


                result = self.app.db.for_payment(self.buyer_id, "by")

                if not result:
                        ctk.CTkLabel(pay_frame, text="No pending orders to pay.", font=("Helvetica", 20), text_color="black").pack(pady=10)
                        return

                order_id, products, amount = result

                ctk.CTkLabel(pay_frame, text="Order Details", text_color="black", font=("Impact", 30)).place(relx=0.02, rely=0.05)


                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.15)
                ctk.CTkLabel(row, text="Order ID:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=str(order_id), font=("Helvetica", 22, "bold"), text_color="black").pack(side="left")

                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.215)
                ctk.CTkLabel(row, text="Products:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=products, font=("Helvetica", 22, "bold"), text_color="black", wraplength=500).pack(side="left")

                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.28)
                ctk.CTkLabel(row, text="Total:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=f"₹{amount}", font=("Helvetica", 22, "bold"), text_color="black").pack(side="left")


                option_frames = {}

 
                payment_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                payment_frame.place(relx=0.1, rely=0.38)

                def select_method(method):
                        for key, frame in option_frames.items():
                                frame.configure(border_color="#0A84FF" if key == method else "#F0F0F0", border_width=2)
                        if method == "UPI":
                                upi_section_frame.place(relx=0.5, rely=0.7, anchor="center")
                                cod_info_frame.place_forget()
                        else:
                                upi_section_frame.place_forget()
                                cod_info_frame.place(relx=0.5, rely=0.7, anchor="center")

                for method in ["UPI", "Cash on Delivery"]:
                        outer = ctk.CTkFrame(payment_frame, fg_color="#F0F0F0", corner_radius=8, border_width=2, border_color="#F0F0F0", width=180, height=50)
                        outer.pack(side="left", padx=10, pady=5)
                        outer.pack_propagate(False)
                        btn = ctk.CTkButton(outer, text=method, fg_color="transparent", hover_color="#0A84FF", text_color="black", font=("Helvetica", 14), command=lambda m=method: select_method(m))
                        btn.pack(expand=True, fill="both")
                        option_frames[method] = outer


                upi_section_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                upi_section_frame.place(relx=0.5, rely=0.7, anchor="center")

                upi_label = ctk.CTkLabel(upi_section_frame, text="UPI ID", font=("Helvetica", 14, "bold"), text_color="black")
                upi_label.pack(padx=40, pady=(30, 0), anchor="w")

                upi_input = ctk.CTkEntry(upi_section_frame, placeholder_text="yourname@bankupi", width=400, height=40, font=("Helvetica", 14))
                upi_input.pack(padx=40, pady=(10, 10), anchor="w")

                upi_btn_frame = ctk.CTkFrame(upi_section_frame, fg_color="transparent")
                upi_btn_frame.pack(pady=(20, 30))

                upi_cancel_btn = ctk.CTkButton(upi_btn_frame, text="Cancel", fg_color="#E0E0E0", text_color="#6d6d6d", font=("Helvetica", 14), width=120, height=40, hover_color="#d0d0d0", command=lambda: self.cancel_payment("by"))
                upi_cancel_btn.pack(side="left", padx=10)

                def confirm_upi():
                        upi_id = upi_input.get().strip()
                        if upi_id:
                                self.insert_payment(self.buyer_id, order_id, amount, "UPI", "by")

                upi_confirm_btn = ctk.CTkButton(upi_btn_frame, text="Confirm Payment", fg_color="#0A84FF", hover_color="#0066CC", font=("Helvetica", 14), width=160, height=40, command=confirm_upi)
                upi_confirm_btn.pack(side="left", padx=10)


                cod_info_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                cod_info_frame.place_forget()

                cod_title = ctk.CTkLabel(cod_info_frame, text="Cash on Delivery", font=("Helvetica", 16, "bold"), text_color="black")
                cod_title.pack(anchor="w", pady=(10, 5), padx=40)

                cod_desc = ctk.CTkLabel(cod_info_frame, text="You will pay in cash upon delivery of the e-waste collection service.", font=("Helvetica", 14), text_color="#6d6d6d", wraplength=600, justify="left")
                cod_desc.pack(anchor="w", padx=40)

                cod_note = ctk.CTkLabel(cod_info_frame, text="Please have the exact amount ready for the collection agent.", font=("Helvetica", 12), text_color="#a0a0a0", wraplength=600, justify="left")
                cod_note.pack(anchor="w", pady=(10, 20), padx=40)

                cod_btn_frame = ctk.CTkFrame(cod_info_frame, fg_color="transparent")
                cod_btn_frame.pack(pady=(10, 20))

                cod_cancel_btn = ctk.CTkButton(cod_btn_frame, text="Cancel", fg_color="#E0E0E0", text_color="#6d6d6d", font=("Helvetica", 14), width=120, height=40, hover_color="#d0d0d0", command=lambda: self.cancel_payment("by"))
                cod_cancel_btn.pack(side="left", padx=10)

                cod_confirm_btn = ctk.CTkButton(cod_btn_frame, text="Confirm Payment", fg_color="#0A84FF", hover_color="#0066CC", font=("Helvetica", 14), width=160, height=40, command=lambda: self.insert_payment(self.buyer_id, order_id, amount, "COD", "by"))
                cod_confirm_btn.pack(side="left", padx=10)


                select_method("UPI")

          def buyer_direct_pay_screen(self, sale_id):
                self.app.clear_content()

                self.sale_id = sale_id

                ctk.CTkLabel(self.app.content_frame, text="Complete Your Payment", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.05, anchor="center")

                pay_frame = ctk.CTkFrame(self.app.content_frame, fg_color="white")
                pay_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.95, anchor="center")


                result = self.app.db.for_payment(self.buyer_id, "dir")

                if not result:
                        ctk.CTkLabel(pay_frame, text="No pending orders to pay.", font=("Helvetica", 20), text_color="black").pack(pady=10)
                        return

                order_id, products, amount = result

                ctk.CTkLabel(pay_frame, text="Order Details", text_color="black", font=("Impact", 30)).place(relx=0.02, rely=0.05)


                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.15)
                ctk.CTkLabel(row, text="Order ID:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=str(order_id), font=("Helvetica", 22, "bold"), text_color="black").pack(side="left")

                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.215)
                ctk.CTkLabel(row, text="Products:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=products, font=("Helvetica", 22, "bold"), text_color="black", wraplength=500).pack(side="left")

                row = ctk.CTkFrame(pay_frame, fg_color="transparent")
                row.place(relx=0.1, rely=0.28)
                ctk.CTkLabel(row, text="Total:", width=120, anchor="w", font=("Helvetica", 20, "bold"), text_color="black").pack(side="left")
                ctk.CTkLabel(row, text=f"₹{amount}", font=("Helvetica", 22, "bold"), text_color="black").pack(side="left")


                option_frames = {}

 
                payment_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                payment_frame.place(relx=0.1, rely=0.38)

                def select_method(method):
                        for key, frame in option_frames.items():
                                frame.configure(border_color="#0A84FF" if key == method else "#F0F0F0", border_width=2)
                        if method == "UPI":
                                upi_section_frame.place(relx=0.5, rely=0.7, anchor="center")
                                cod_info_frame.place_forget()
                        else:
                                upi_section_frame.place_forget()
                                cod_info_frame.place(relx=0.5, rely=0.7, anchor="center")

                for method in ["UPI", "Cash on Delivery"]:
                        outer = ctk.CTkFrame(payment_frame, fg_color="#F0F0F0", corner_radius=8, border_width=2, border_color="#F0F0F0", width=180, height=50)
                        outer.pack(side="left", padx=10, pady=5)
                        outer.pack_propagate(False)
                        btn = ctk.CTkButton(outer, text=method, fg_color="transparent", hover_color="#0A84FF", text_color="black", font=("Helvetica", 14), command=lambda m=method: select_method(m))
                        btn.pack(expand=True, fill="both")
                        option_frames[method] = outer


                upi_section_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                upi_section_frame.place(relx=0.5, rely=0.7, anchor="center")

                upi_label = ctk.CTkLabel(upi_section_frame, text="UPI ID", font=("Helvetica", 14, "bold"), text_color="black")
                upi_label.pack(padx=40, pady=(30, 0), anchor="w")

                upi_input = ctk.CTkEntry(upi_section_frame, placeholder_text="yourname@bankupi", width=400, height=40, font=("Helvetica", 14))
                upi_input.pack(padx=40, pady=(10, 10), anchor="w")

                upi_btn_frame = ctk.CTkFrame(upi_section_frame, fg_color="transparent")
                upi_btn_frame.pack(pady=(20, 30))

                upi_cancel_btn = ctk.CTkButton(upi_btn_frame, text="Cancel", fg_color="#E0E0E0", text_color="#6d6d6d", font=("Helvetica", 14), width=120, height=40, hover_color="#d0d0d0", command=lambda: self.cancel_payment("dir"))
                upi_cancel_btn.pack(side="left", padx=10)

                def confirm_upi():
                        upi_id = upi_input.get().strip()
                        if upi_id:
                                self.insert_payment(self.buyer_id, order_id, amount, "UPI", "dir")

                upi_confirm_btn = ctk.CTkButton(upi_btn_frame, text="Confirm Payment", fg_color="#0A84FF", hover_color="#0066CC", font=("Helvetica", 14), width=160, height=40, command=confirm_upi)
                upi_confirm_btn.pack(side="left", padx=10)


                cod_info_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
                cod_info_frame.place_forget()

                cod_title = ctk.CTkLabel(cod_info_frame, text="Cash on Delivery", font=("Helvetica", 16, "bold"), text_color="black")
                cod_title.pack(anchor="w", pady=(10, 5), padx=40)

                cod_desc = ctk.CTkLabel(cod_info_frame, text="You will pay in cash upon delivery of the e-waste collection service.", font=("Helvetica", 14), text_color="#6d6d6d", wraplength=600, justify="left")
                cod_desc.pack(anchor="w", padx=40)

                cod_note = ctk.CTkLabel(cod_info_frame, text="Please have the exact amount ready for the collection agent.", font=("Helvetica", 12), text_color="#a0a0a0", wraplength=600, justify="left")
                cod_note.pack(anchor="w", pady=(10, 20), padx=40)

                cod_btn_frame = ctk.CTkFrame(cod_info_frame, fg_color="transparent")
                cod_btn_frame.pack(pady=(10, 20))

                cod_cancel_btn = ctk.CTkButton(cod_btn_frame, text="Cancel", fg_color="#E0E0E0", text_color="#6d6d6d", font=("Helvetica", 14), width=120, height=40, hover_color="#d0d0d0", command=lambda: self.cancel_payment("dir"))
                cod_cancel_btn.pack(side="left", padx=10)

                cod_confirm_btn = ctk.CTkButton(cod_btn_frame, text="Confirm Payment", fg_color="#0A84FF", hover_color="#0066CC", font=("Helvetica", 14), width=160, height=40, command=lambda: self.insert_payment(self.buyer_id, order_id, amount, "COD", "dir"))
                cod_confirm_btn.pack(side="left", padx=10)


                select_method("UPI")

          def cancel_payment(self, ty):
                if ty == "by":
                        try:
                                self.app.db.cursor.execute(
                                "SELECT order_id FROM orders WHERE buyer_id = %s AND payment_id IS NULL",
                                (self.buyer_id,)
                                )
                                order_ids = self.app.db.cursor.fetchall()

                                if not order_ids:
                                        return  # No unpaid orders to cancel

                                for (order_id,) in order_ids:
                                        self.app.db.cursor.execute(
                                        "DELETE FROM order_item WHERE order_id = %s", (order_id,)
                                )

                                        self.app.db.cursor.execute(
                                        "DELETE FROM orders WHERE buyer_id = %s AND payment_id IS NULL",
                                        (self.buyer_id,)
                                )

                                self.app.db.db.commit()

                        except Exception as e:
                                print("Cancel Payment Error:", e)
                elif ty == "dir":
                        return self.buyer_shop_screen()


                self.buyer_shop_screen()


          def insert_payment(self, buyer_id, order_id, amount, method, ty):
                if ty == "by":
                        try:
                               
                                while self.app.db.cursor.nextset():
                                        pass

                                self.app.db.cursor.execute("""
                                INSERT INTO payments (buyer_id, amount, payment_method, payment_status)
                                VALUES (%s, %s, %s, 'successful')
                                """, (buyer_id, amount, method))

                                payment_id = self.app.db.cursor.lastrowid

                                self.app.db.cursor.execute("""
                                UPDATE orders SET payment_id = %s WHERE order_id = %s
                                """, (payment_id, order_id))

                                self.app.db.db.commit()
                                
                                self.app.db.reduce_inventory_stock(order_id)
                                invoice_path = self.app.inv.generate_invoice(order_id)

                        except Exception as e:
                                print(f"Error during payment insert: {e}")

                elif ty == "dir":
                        self.app.db.cursor.nextset()
                        self.app.db.cursor.execute("UPDATE direct_sale SET status = 'sold' WHERE sale_id = %s", (self.sale_id,))
                        self.app.db.db.commit()

                        invoice_path = self.app.inv.generate_invoice(self.sale_id)

                if invoice_path:
                        print("Invoice saved at:", invoice_path)
                        os.startfile(invoice_path)

                self.buyer_shop_screen()


          def buyer_status_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(
                        self.app.content_frame,
                        text="Order Status",
                        text_color="black",
                        font=("Impact", 40)
                ).place(relx=0.5, rely=0.05, anchor="center")

                status_frame = ctk.CTkFrame(
                        self.app.content_frame,
                        fg_color="#FFFFFF",
                        corner_radius=10
                )
                status_frame.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.6, anchor="center")

                columns = ("Order ID", "Product", "Quantity", "Date", "Status")

                style = ttk.Style()
                style.configure("Custom.Treeview", font=("Arial", 14), rowheight=30)
                style.configure("Custom.Treeview.Heading", font=("Arial", 16, "bold"))

                self.status_tree = ttk.Treeview(
                        status_frame, columns=columns,
                        show="headings", height=12,
                        style="Custom.Treeview"
                )

                column_widths = [100, 200, 100, 150, 120]
                for col, width in zip(columns, column_widths):
                        self.status_tree.heading(col, text=col)
                        self.status_tree.column(col, width=width, anchor="center")

                self.status_tree.pack(fill="both", expand=True)

                rows = self.app.db.get_buyer_status(self.buyer_id)

                self.status_tree.delete(*self.status_tree.get_children())
                if rows:
                        for row in rows:
                                order_id, product, qty, date, status = row
                                if status.lower() == "pending":
                                        tag = "pending"
                                elif status.lower() in ("completed", "delivered"):
                                        tag = "completed"
                                elif status.lower() == "cancelled":
                                        tag = "cancelled"
                                elif status.lower() == "shipped":
                                        tag = "shipped"
                                else:
                                        tag = ""
                                self.status_tree.insert("", "end", values=row, tags=(tag,))
                else:
                        self.status_tree.insert("", "end", values=("No Orders", "", "", "", ""))

                self.status_tree.tag_configure("pending", background="#FFF27C")
                self.status_tree.tag_configure("completed", background="#76FC76")
                self.status_tree.tag_configure("cancelled", background="#F95858")
                self.status_tree.tag_configure("shipped", background="#8ADDF9")


          def buyer_wishlist_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(
                        self.app.content_frame, 
                        text="Your Wishlist", 
                        text_color="black", 
                        font=("Impact", 50)
                ).place(relx=0.5, rely=0.05, anchor="center")

                self.wishlist_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#E4E7EB")
                self.wishlist_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.9, anchor="center")

                wishlist_items = self.app.fm.get_wishlist(self.buyer_id)

                if not wishlist_items:
                        ctk.CTkLabel(
                        self.wishlist_frame,
                        text="Your wishlist is empty.",
                        text_color="gray",
                        font=("Arial", 20, "italic")
                        ).pack(pady=50)
                        return

                for i, product in enumerate(wishlist_items):
                        inventory_id, name, type, price_per_unit, stock, img_path = product

                        row = i // 3
                        col = i % 3

                        p_frame = ctk.CTkFrame(self.wishlist_frame, fg_color="white", corner_radius=0, width=280, height=340)
                        p_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                        img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 200))
                        ctk.CTkLabel(p_frame, image=img, text="").pack(pady=5)

                        ctk.CTkLabel(p_frame, text=name, font=("Arial", 18, "bold"), text_color="black").pack(pady=(5, 2))
                        ctk.CTkLabel(p_frame, text=f"₹{price_per_unit}", font=("Arial", 16), text_color="green").pack()
                        ctk.CTkLabel(p_frame, text=f"Category: {type}", font=("Arial", 14), text_color="black").pack()
                        ctk.CTkLabel(p_frame, text=f"Stock: {stock}", font=("Arial", 14), text_color="black").pack()

                        remove_btn = ctk.CTkButton(
                        p_frame, 
                        text="Remove", 
                        fg_color="#EF4444", 
                        hover_color="#DC2626", 
                        command=lambda prod=product: self.remove_wishlist_item(prod)
                        )
                        remove_btn.pack(pady=10)

                for col in range(3):
                        self.wishlist_frame.grid_columnconfigure(col, weight=1)


          def buyer_history_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(
                        self.app.content_frame,
                        text="Your Purchase History",
                        text_color="black",
                        font=("Impact", 40)
                ).place(relx=0.5, rely=0.05, anchor="center")

                history_frame = ctk.CTkFrame(
                        self.app.content_frame,
                        fg_color="#FFFFFF",
                        corner_radius=10
                )
                history_frame.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.6, anchor="center")

                columns = ("Order ID", "Product", "Price", "Quantity", "Date")

                style = ttk.Style()
                style.configure("Custom.Treeview",
                                font=("Arial", 14),
                                rowheight=30)  
                style.configure("Custom.Treeview.Heading",
                                font=("Arial", 16, "bold")) 

                self.history_tree = ttk.Treeview(
                        history_frame, columns=columns,
                        show="headings", height=12,
                        style="Custom.Treeview"
                )

                column_widths = [100, 200, 100, 80, 150]
                for col, width in zip(columns, column_widths):
                        self.history_tree.heading(col, text=col)
                        self.history_tree.column(col, width=width, anchor="center")

                self.history_tree.pack(fill="both", expand=True)

                rows = self.app.db.get_buyer_history(self.buyer_id)

                self.history_tree.delete(*self.history_tree.get_children())
                if rows:
                        for row in rows:
                                self.history_tree.insert("", "end", values=row)
                else:
                        self.history_tree.insert("", "end", values=("No Purchase History", "", "", "", ""))

          def buyer_fb_screen(self):
                    self.app.clear_content()
                    self.star_buttons.clear()

                    ctk.CTkLabel(self.app.content_frame, text="FEEDBACK", font=("Impact", 40), text_color="#993D00").place(relx=0.5, rely=0.05, anchor="center")

                    self.fb_frame = ctk.CTkFrame(self.app.content_frame, fg_color="White", corner_radius=20)
                    self.fb_frame.place(relx=0.5, rely=0.55, relheight=0.7, relwidth=0.4, anchor="center")

                    ctk.CTkLabel(self.fb_frame, text="Rate Us", font=("Impact", 35), text_color="#993D00").place(relx=0.5, rely=0.1, anchor="center")

          
                    for i in range(5):
                              btn = ctk.CTkButton(
                                        self.fb_frame,
                                        text="☆", 
                                        font=("Arial", 30),
                                        width=50,
                                        fg_color="transparent",
                                        text_color="black",
                                        hover=False,
                                        command=lambda i=i: self.set_rating(i + 1)
                              )
                              btn.place(x=90 + i * 60, y=100)
                              self.star_buttons.append(btn)

                    ctk.CTkLabel(self.fb_frame, text="Enter Your Feedback ", text_color="black", font=("Arial", 20, "bold"), anchor="w").place(relx=0.5, rely=0.36, anchor="center")

                    self.fb_text = ctk.CTkTextbox(self.fb_frame, height=200, width=400, corner_radius=15, bg_color="transparent", fg_color="transparent", border_width=5, text_color="black")
                    self.fb_text.place(relx=0.5, rely=0.6, anchor="center")

                    self.submit_b = ctk.CTkButton(self.fb_frame, width=200, text="Submit", fg_color="#993D00",hover_color="#a64300", border_width=2, border_color="black", command = self.submit_fb)
                    self.submit_b.place(relx=0.5, rely=0.9, anchor="center")

          def buyer_report_screen(self):
                    self.app.clear_content()

                    ctk.CTkLabel(self.app.content_frame, text="Report an Issue", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.07, anchor="center")

                    self.report_frame = ctk.CTkFrame(self.app.content_frame, fg_color="white", corner_radius=20)
                    self.report_frame.place(relx=0.5, rely=0.5, relheight=0.7, relwidth=0.32, anchor="center")

                    row = 0
                    ctk.CTkLabel(self.report_frame, text="Type of Issue", font=("Arial", 16, "bold"), text_color="#1E3A8A").grid(row=row, column=0, pady=(20, 5), sticky="w", padx=20)

                    row += 1
                    self.report_type = ctk.CTkComboBox(self.report_frame, values=["Bug", "Scam", "Payment Issue", "Delivery Issue", "Inspector Issue", "Other"], font=("Arial", 14), corner_radius=8, width=350)
                    self.report_type.set("Select Type")
                    self.report_type.grid(row=row, column=0, padx=20, sticky="ew")

                    row += 1
                    ctk.CTkLabel(self.report_frame, text="Description", font=("Arial", 16, "bold"), text_color="#1E3A8A").grid(row=row, column=0, pady=(20, 5), sticky="w", padx=20)

                    row += 1
                    self.report_desc = ctk.CTkTextbox(self.report_frame, font=("Arial", 14), height=150, corner_radius=10, width=350)
                    self.report_desc.grid(row=row, column=0, padx=20, sticky="ew")

                    row += 1
                    self.upload_report_btn = ctk.CTkButton(self.report_frame, text="Upload Evidence", command=self.upload_report_image, font=("Arial", 14), corner_radius=10, fg_color="#10B981", hover_color="#059669", width=150)
                    self.upload_report_btn.grid(row=row, column=0, pady=15, padx=20, sticky="w")

                    row += 1
                    self.report_image_label = ctk.CTkLabel(self.report_frame, text="No file selected", font=("Arial", 12), text_color="gray")
                    self.report_image_label.grid(row=row, column=0, pady=(0, 10), padx=20, sticky="w")

                    row += 1
                    self.submit_report_btn = ctk.CTkButton(self.report_frame, text="Submit Report", command=self.submit_report, font=("Arial", 16, "bold"), height=45, corner_radius=12, fg_color="#2563EB", hover_color="#1E40AF", width=170)
                    self.submit_report_btn.grid(row=row, column=0, pady=20, padx=20, sticky="ew")

          def buyer_profile(self):
                    if self.anyy:
                        self.anyy.destroy()
                        self.anyy = None
                    
                    mail = self.app.p_mail

                    query = f"select buyer_id, name, phone_no, email, address from buyer where email=%s"

                    self.app.db.cursor.execute(query, (mail,))
                    result = self.app.db.cursor.fetchone()
                    
                    self.sid = result[0]
                    name = result[1]
                    phone = result[2]
                    email = result[3]
                    addr = result[4]

                    self.anyy = ctk.CTkFrame(self.app.main_frame, height=410, width=310, fg_color="white", corner_radius=0)
                    self.anyy.place(relx=0.97, rely=0.4, anchor="e")

                    self.pro_frame = ctk.CTkFrame(self.anyy, height=400, width=300, bg_color="transparent",fg_color="#EAF2FB", corner_radius=20)
                    self.pro_frame.place(relx=0.5, rely=0.5, anchor="center")

                    ctk.CTkLabel(self.pro_frame, text="PROFILE", text_color="#074B65", font=("Impact", 28, "underline")).place(relx=0.5, rely=0.1, anchor="center")

                    text = f"ID : {self.sid}\n Name : {name}\n Phone No. : {phone}\n Email : {email}\n Address : {addr}"

                    ctk.CTkLabel(self.pro_frame, text=text, text_color="#074B65", font=("Impact", 25)).place(relx=0.5, rely=0.4, anchor="center")

                    
                    ctk.CTkFrame(self.pro_frame, height=2, fg_color="black").place(relx=0.5, rely=0.75, relwidth=1, anchor="center")

                    ctk.CTkLabel(self.pro_frame, text="Want to Logout?", text_color="red", font=("Arial", 15)).place(relx=0.5, rely=0.8, anchor="center")

                    self.logout = ctk.CTkButton(self.pro_frame, text="LOGOUT", fg_color="#EF4444", hover_color="#F87171",
                                                  text_color="#FFFFFF", font=("Poppins", 15),
                                                  height=30, width=100, corner_radius=10, command=self.conf_logout)
                    self.logout.place(relx=0.5, rely=0.87, anchor="center")

                    back_btn = ctk.CTkLabel(self.pro_frame, text="Back", text_color="blue", fg_color="transparent", font=("Arial", 15))
                    back_btn.place(relx=0.5, rely=0.95, anchor="center")
                    back_btn.bind("<Button-1>", lambda e: self.remove_profile())

                    self.pro_frame.bind("<Button-1>", lambda e: "break")

                    self.app.bind("<Button-1>", self.check_click_outside_profile, add="+")

                    self.anyy.lift()


          def check_click_outside_profile(self, event):
                    if self.anyy:
                              x1 = self.anyy.winfo_rootx()
                              y1 = self.anyy.winfo_rooty()
                              x2 = x1 + self.anyy.winfo_width()
                              y2 = y1 + self.anyy.winfo_height()

                              if not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
                                        self.remove_profile()
                                        self.app.unbind("<Button-1>") 


          def remove_profile(self):
                    if self.anyy:
                                self.anyy.destroy()
                                self.anyy = None



          def buyer_notify(self):
                    qwerty = [
                                                  "Product uploaded successfully.",
                                                  "Awaiting admin approval.",
                                                  "Product approved for inspection.",
                                                  "Product rejected by admin.",
                                                  "Inspector assigned.",
                                                  "Inspection completed.",
                                                  "Final price offered by admin.",
                                                  "Action required: Accept/Reject price.",
                                                  "Pickup scheduled.",
                                                  "Product sold successfully.",
                                                  "Payment initiated.",
                                                  "Reminder: Pending action on your product."
                                        ]

                    self.app.mg.create_msg_frame(qwerty)

          def update_cart_qty(self, inventory_id, change, stock):
                self.app.fm.update_cart_quantity(self.buyer_id, inventory_id, change, stock)
                self.buyer_cart_screen()

          def remove_cart_item(self, inventory_id):
                self.app.fm.remove_from_cart(self.buyer_id, inventory_id)
                self.buyer_cart_screen()

          def get_locations(self, m, p):
                    self.app.mp.get_map(self.set_pickup_addres)

                    m.destroy()
                    p.place(relx=0.75, rely=0.9, anchor="center")

          def set_pickup_addres(self, address):
                    self.delivery_location = address


          def show_product_details(self, product):
                self.app.clear_content()

                inventory_id, name, category, price, stock, img_path = product

                product_img = ctk.CTkImage(
                        light_image=Image.open(img_path),
                        size=(350, 350)
                )
                ctk.CTkLabel(
                        self.app.content_frame,
                        image=product_img,
                        text=""
                ).place(relx=0.25, rely=0.5, anchor="center")

                details_frame = ctk.CTkFrame(
                        self.app.content_frame,
                        fg_color="#E4E7EB",
                        corner_radius=15
                )
                details_frame.place(relx=0.7, rely=0.5, relwidth=0.5, relheight=0.7, anchor="center")

                ctk.CTkLabel(
                        details_frame,
                        text=name,
                        font=("Impact", 40, "bold"),
                        text_color="black"
                ).place(relx=0.5, rely=0.05, anchor="center")

                details_text = (
                                        "✔ 1-Year Standard Warranty\n"
                                        "✔ 75% Service Fee Post-Warranty\n"
                                        "✔ Free Delivery within Mumbai\n"
                                        "✔ 24/7 Customer Support"
                                        )
                
                ctk.CTkLabel(
                                details_frame,
                                text=details_text,
                                text_color="#074B65",
                                font=("Arial", 18, "bold"),
                                justify="left"
                                ).place(relx=0.5, rely=0.25, anchor="center")

                ctk.CTkLabel(
                        details_frame,
                        text=f"Category: {category}",
                        font=("Arial", 18), 
                        text_color="black"
                ).place(relx=0.5, rely=0.4, anchor="center")

                ctk.CTkLabel(
                        details_frame,
                        text=f"Price: ₹{price}",
                        font=("Arial", 18),
                        text_color="green"
                ).place(relx=0.5, rely=0.5, anchor="center")

                ctk.CTkLabel(
                        details_frame,
                        text=f"Available Stock: {stock}",
                        font=("Arial", 16),
                        text_color="gray"
                ).place(relx=0.5, rely=0.6, anchor="center")

                qty_frame = ctk.CTkFrame(
                        details_frame,
                        fg_color="transparent",
                        height=15
                )
                qty_frame.place(relx=0.5, rely=0.7, relwidth=0.8, anchor="center")

                self.qty_var = ctk.IntVar(value=1)

                def decrease_qty():
                        current = self.qty_var.get()
                        if current > 1:
                                self.qty_var.set(current - 1)

                def increase_qty():
                        current = self.qty_var.get()
                        if current < stock:
                                self.qty_var.set(current + 1)

                ctk.CTkButton(details_frame, text="-", width=30, command=lambda: self.qty_var.set(max(1, self.qty_var.get() - 1))).place(relx=0.4, rely=0.7, anchor="center")
                ctk.CTkEntry(details_frame, textvariable=self.qty_var, width=50, justify="center").place(relx=0.5, rely=0.7, anchor="center")
                ctk.CTkButton(details_frame, text="+", width=30, command=lambda: self.qty_var.set(self.qty_var.get() + 1)).place(relx=0.6, rely=0.7, anchor="center")

                self.add_btn = ctk.CTkButton(
                                details_frame,
                                text="Add to 🛒 Cart",
                                fg_color="#2563EB",
                                hover_color="#1E3A8A",
                                command = lambda prod = product: self.after_cart(prod)
                                )
                self.add_btn.place(relx=0.5, rely=0.8, anchor="center")

                bk_bt = ctk.CTkLabel(self.app.content_frame, text="Back", text_color="blue", font=("Arial", 14), cursor="hand1")
                bk_bt.place(relx=0.5, rely=0.9, anchor="center")
                bk_bt.bind("<Button-1>", lambda e: self.buyer_shop_screen())

          def show_direct_product_details(self, product, sale_id):
                self.app.clear_content()

                inventory_id, name, category, brand, model, condition, price, stock, images_paths = product

                img_path = json.loads(images_paths)[0] if images_paths else "default.png"
                img = ctk.CTkImage(light_image=Image.open(img_path), size=(350, 350))
                ctk.CTkLabel(self.app.content_frame, image=img, text="").place(relx=0.25, rely=0.5, anchor="center")

                details_frame = ctk.CTkFrame(self.app.content_frame, fg_color="#E4E7EB", corner_radius=15)
                details_frame.place(relx=0.7, rely=0.5, relwidth=0.5, relheight=0.7, anchor="center")

                ctk.CTkLabel(details_frame, text=name, font=("Impact", 40, "bold"), text_color="black").place(relx=0.5, rely=0.1, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Category : {category}", font=("Arial", 18), text_color="black").place(relx=0.5, rely=0.25, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Brand : {brand}", font=("Arial", 18), text_color="black").place(relx=0.5, rely=0.3, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Model : {model}", font=("Arial", 18), text_color="black").place(relx=0.5, rely=0.35, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Quantity : {stock}", font=("Arial", 18), text_color="grey").place(relx=0.5, rely=0.43, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Condition : {condition}", font=("Arial", 18), text_color="blue").place(relx=0.5, rely=0.51, anchor="center")
                ctk.CTkLabel(details_frame, text=f"Price : ₹{price}", font=("Arial", 16), text_color="green").place(relx=0.5, rely=0.6, anchor="center")

                map_b = ctk.CTkButton(self.app.content_frame, text="Select Delivery Location", fg_color="#2563EB", hover_color="#1E3A8A")
                map_b.place(relx=0.75, rely=0.9, anchor="center")

                buy_now_btn = ctk.CTkButton(
                        details_frame,
                        text="Buy Now",
                        fg_color="#2563EB",
                        hover_color="#1E3A8A",
                        command=lambda: self.app.db.direct_order_details(self.buyer_id, sale_id, self.delivery_location)
                )
                

                bk_bt = ctk.CTkLabel(self.app.content_frame, text="Back", text_color="blue", font=("Arial", 14), cursor="hand1")
                bk_bt.place(relx=0.5, rely=0.93, anchor="center")
                bk_bt.bind("<Button-1>", lambda e: self.buyer_s_to_b_screen())

                map_b.configure(command=lambda : self.get_locations(map_b, buy_now_btn))
                
          def after_cart(self, product):
                  self.app.fm.add_to_cart(self.buyer_id, product, int(self.qty_var.get()))

                  self.buyer_cart_screen()


          def toggle_wishlist(self, product, button):
                wishlist = self.app.fm.get_wishlist(self.buyer_id)
                exists = any(prod[0] == product[0] for prod in wishlist)

                if exists:
                        self.app.fm.remove_from_wishlist(self.buyer_id, product[0])
                        button.configure(text="♡")
                else:
                        self.app.fm.add_to_wishlist(self.buyer_id, product)
                        button.configure(text="♥")

          def remove_wishlist_item(self, product):
                self.app.fm.remove_from_wishlist(self.buyer_id, product[0])
                messagebox.showinfo("Wishlist", f"{product[1]} removed from your wishlist.")
                self.buyer_wishlist_screen()

          def update_cart_quantity(self, inventory_id, change):
                self.app.fm.update_cart_quantity(self.buyer_id, inventory_id, change)
                self.buyer_cart_screen()


          def remove_cart_item(self, inventory_id):
                self.app.fm.remove_from_cart(self.buyer_id, inventory_id)
                messagebox.showinfo("Cart", "Item removed from your cart.")
                self.buyer_cart_screen()


          def upload_report_image(self):
                    files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")], multiple=True)
                    self.report_files = files
                    self.report_image_label.configure(text=", ".join([os.path.basename(f) for f in files]) if files else "No file selected")


          def submit_fb(self):
                    rate = self.rating
                    review = self.fb_text.get("1.0", "end-1c").lower()
                    try:
                              query = "insert into feedback (buyer_id, rate, review) values (%s, %s, %s)"
                              self.app.db.cursor.execute(query, (self.buyer_id, rate, review))
                              self.app.db.db.commit()
                              return self.after_fb() 
                    
                                        

                    except Exception as e:
                              print(f"Database Error: {e}")

          def after_fb(self):
                    self.app.clear_content()
                    ctk.CTkLabel(self.app.content_frame, text=f"Feedback Submitted, \n Thank You For Feedback...!!", text_color="Black", font=("Impact", 30)).place(relx=0.5, rely=0.5, anchor="center")



          def set_rating(self, stars):
                    self.rating = stars
                    
                    for i in range(5):
                              if i < stars:
                                        self.star_buttons[i].configure(text="★")
                                        self.star_buttons[i].configure(text_color="gold")
                              else:
                                        self.star_buttons[i].configure(text="☆")
                                        self.star_buttons[i].configure(text_color="black")

          def upload_report_image(self):
                    files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")], multiple=True)
                    self.report_files = files
                    self.report_image_label.configure(text=", ".join([os.path.basename(f) for f in files]) if files else "No file selected")


          def submit_report(self):
                    
                    r_type = self.report_type.get()
                    desc = self.report_desc.get("1.0", "end").strip()
                    files_path = ",".join(self.report_files)
                    if r_type == "Choose Type" or not desc:
                              messagebox.showerror("Error", "Please select a report type and enter a description.")
                              return
                    print(f"Report Type: {r_type}\nDescription: {desc}\nFiles: {self.report_files if hasattr(self,'report_files') else 'None'}")
                    messagebox.showinfo("Success", "Your report has been submitted!")

                    what = self.app.db.submit_report_all("buyer", self.buyer_id, r_type, desc, files_path)

                    if what == "S":
                            self.app.clear_content()

                            ctk.CTkLabel(self.app.content_frame, text=f"Report Submitted, \n Thank You For Reporting...!!", text_color="Black", font=("Impact", 30)).place(relx=0.5, rely=0.5, anchor="center")

                    else:
                            self.seller_report_screen()

          def conf_logout(self):
                    for widget in self.pro_frame.winfo_children():
                              widget.destroy()

                    ctk.CTkLabel(self.pro_frame, text=f"Are you Sure \n You Want To LOGOUT?", text_color="#074B65", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.4, anchor="center")

                    logout = ctk.CTkButton(self.pro_frame, text="LOGOUT", fg_color="#EF4444", hover_color="#F87171",
                                                  text_color="#FFFFFF", font=("Poppins", 15),
                                                  height=30, width=100, corner_radius=10, command=self.app.rol.role_screen)
                    logout.place(relx=0.5, rely=0.5, anchor="center")

                    back_btn = ctk.CTkLabel(self.pro_frame, text="Back", text_color="blue", fg_color="transparent", font=("Arial", 15))
                    back_btn.place(relx=0.5, rely=0.9, anchor="center")
                    back_btn.bind("<Button-1>", lambda e: self.remove_profile())

                    self.app.unbind("<Button-1>")

