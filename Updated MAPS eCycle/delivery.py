import customtkinter as ctk
from tkinter import messagebox
from collections import defaultdict
from PIL import Image


class Delivery:
          def __init__(self, app):
                  self.app = app


          def valid_delivery(self):
                    delivery_code = self.delivery_pass_entry.get().strip()

                    valid_del = ["a"]
                    if delivery_code in valid_del:
                              messagebox.showinfo("Success", "Successfully Logged In!")

                              self.delivery_screen()
          
                    else:
                              messagebox.showerror("Invalid", "Invalid Admin Code!")

          def delivery_login(self):
                self.app.remove_head_content()
                self.app.clear_frame()

                img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                ctk.CTkLabel(self.app.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                self.frame = ctk.CTkFrame(self.app.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                self.frame.place(relx=0.5, rely=0.5, anchor="center")

                admin_label = ctk.CTkLabel(self.frame, text="deliveryors", font=("Impact", 50), width=200, text_color="black")
                admin_label.place(relx=0.5, rely=0.1, anchor="center")

                admin_login_label = ctk.CTkLabel(self.frame, text="Login", font=("Impact", 50), width=380, text_color="black")
                admin_login_label.place(relx=0.5, rely=0.2, anchor="center")

                self.delivery_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Name", width=380)
                self.delivery_entry.place(relx=0.5, rely=0.4, anchor="center")

                self.delivery_pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter deliveryor login password", width=380)
                self.delivery_pass_entry.place(relx=0.5, rely=0.5, anchor="center")

                login_button = ctk.CTkButton(self.frame, text="LOGIN", width=200, fg_color="black", text_color="white", border_width=2, border_color="grey", command=self.valid_delivery)
                login_button.place(relx=0.5, rely=0.7, anchor="center")

                back_l = ctk.CTkLabel(self.frame, text="Back", font=("Arial", 14), text_color="blue")
                back_l.place(relx=0.5, rely=0.8, anchor="center")

                back_l.bind("<Button-1>", lambda e: self.app.rol.role_screen())


          def delivery_screen(self):
                  self.app.clear_frame()
                  if self.app.content_frame:
                        self.app.clear_content()
                  self.app.head_content_create("delivery")

                  ctk.CTkLabel(self.app.content_frame, text="Dashboard", font=("Impact", 60), text_color="Black").place(relx=0.5, rely=0.08, anchor="center")

                  self.list_m = ["Deliveries", "Pick Ups", "Buyer to Seller"]
                  self.app.me.menu_flag(self.list_m, "delivery")

                  self.column_widths = [100, 270, 250, 140]
                  self.headers = ["DELIVERY ID", "ITEMS", "DESTINATION", "STATUS"]

                  self.FONT_TITLE = ("Helvetica", 18, "bold")
                  self.FONT_HEADER = ("Helvetica", 11, "bold")
                  self.FONT_ROW = ("Helvetica", 11)
                  self.BADGE_FONT = ("Helvetica", 10, "bold")

                  self.STATUS_COLORS = {
                        "pending": "#067FF0",
                        "in transit": "#FF7F27",
                        "delivered": "#00C851",
                        "cancelled":"#E13D3A"
                  }

                  table = ctk.CTkFrame(self.app.content_frame, corner_radius=15, fg_color="#f2f2f2")
                  table.place(relx=0.03, rely=0.13, relwidth=0.65, relheight=0.7)

                  header_frame = ctk.CTkFrame(table, fg_color="#dddddd", height=40)
                  header_frame.pack(fill="x")

                  for idx, h in enumerate(self.headers):
                        ctk.CTkLabel(
                              header_frame,
                              text=h,
                              font=self.FONT_HEADER,
                              text_color="#1B0303",
                              width=self.column_widths[idx],
                              anchor="w"
                        ).pack(side="left", padx=(12 if idx == 0 else 0, 0), pady=10)

                  query = """
                        SELECT o.order_id, p.name, oi.quantity, o.delivery_address, o.status 
                        FROM orders o 
                        JOIN order_item oi ON o.order_id = oi.order_id 
                        JOIN inventory p ON oi.inventory_id = p.inventory_id and o.status = "pending"
                  """
                  self.app.db.cursor.execute(query)
                  rows = self.app.db.cursor.fetchall()

                  grouped_orders = defaultdict(lambda: {"items": [], "destination": "", "status": ""})
                  for order_id, product_name, qty, destination, status in rows:
                        grouped_orders[order_id]["items"].append(f"{product_name} ({qty})")
                        grouped_orders[order_id]["destination"] = destination
                        grouped_orders[order_id]["status"] = status

                  for order_id, info in grouped_orders.items():
                        item_list = ", ".join(info["items"])
                        destination = info["destination"]
                        status = info["status"]

                        row_frame = ctk.CTkFrame(table, fg_color="transparent")
                        row_frame.pack(fill="x", pady=4)

                        ctk.CTkLabel(row_frame, text=order_id, font=self.FONT_ROW, width=self.column_widths[0], anchor="w", text_color="black").pack(side="left", padx=(12, 0))
                        ctk.CTkLabel(row_frame, text=item_list, font=self.FONT_ROW, width=self.column_widths[1], anchor="w", text_color="black").pack(side="left")
                        ctk.CTkLabel(row_frame, text=destination, wraplength=230, font=self.FONT_ROW, width=self.column_widths[2], anchor="w", text_color="black").pack(side="left")

                        status_menu = ctk.CTkOptionMenu(
                              row_frame,
                              values=["pending", "in transit", "delivered", "cancelled"],
                              command=lambda s, m=None, d_id=order_id: self.update_status(m, s, d_id),
                              font=self.BADGE_FONT,
                              width=110,
                              height=28,
                              corner_radius=12,
                              fg_color=self.STATUS_COLORS.get(status),
                              button_color=self.STATUS_COLORS.get(status),
                              dropdown_font=self.BADGE_FONT
                        )
                        status_menu.set(status)
                        status_menu.pack(side="left", padx=5)
                        status_menu._command = lambda s, m=status_menu, d_id=order_id: self.update_status(m, s, d_id)

                  self.insp_notify()

          def update_status(self, menu, selected_status, order_id):
                  status_db = selected_status.lower()
                  update_query = "UPDATE orders SET status = %s WHERE order_id = %s"
                  try:
                        self.app.db.cursor.execute(update_query, (status_db, order_id))
                        self.app.db.db.commit()
                        if menu:
                              color = self.STATUS_COLORS.get(status_db, "#DDDDDD")
                              menu.configure(fg_color=color, button_color=color)
                              menu.set(selected_status.upper())
                        messagebox.showinfo("Success", f"Order {order_id} updated to {selected_status}")
                  except Exception as e:
                        messagebox.showerror("Error", f"Failed to update status: {e}")


          def pickup_screen(self):
                  self.app.clear_content()
                  

                  self.column_widths = [100, 270, 250, 140]
                  self.headers = ["PICKUP ID", "PRODUCT", "ADDRESS", "STATUS"]

                  self.FONT_TITLE = ("Helvetica", 18, "bold")
                  self.FONT_HEADER = ("Helvetica", 11, "bold")
                  self.FONT_ROW = ("Helvetica", 11)
                  self.BADGE_FONT = ("Helvetica", 10, "bold")

                  self.STATUS_COLORS = {
                        "Scheduled": "#067FF0",
                        "Picked": "#00C851",
                        "Cancelled": "#E13D3A"
                  }

                  table = ctk.CTkFrame(self.app.content_frame, corner_radius=15, fg_color="#f2f2f2")
                  table.place(relx=0.03, rely=0.13, relwidth=0.65, relheight=0.7)

                  header_frame = ctk.CTkFrame(table, fg_color="#dddddd", height=40)
                  header_frame.pack(fill="x")

                  for idx, h in enumerate(self.headers):
                        ctk.CTkLabel(
                              header_frame,
                              text=h,
                              font=self.FONT_HEADER,
                              text_color="#1B0303",
                              width=self.column_widths[idx],
                              anchor="w"
                        ).pack(side="left", padx=(12 if idx == 0 else 0, 0), pady=10)

                  query = """
                        SELECT pk.pickup_id, p.product_id, p.product_type, pk.pickup_address, pk.status
                        FROM pickup pk
                        JOIN product p ON pk.product_id = p.product_id and p.status = "approved"
                  """
                  self.app.db.cursor.execute(query)
                  rows = self.app.db.cursor.fetchall()

                  for pickup_id, product_id, product_name, address, status in rows:
                        row_frame = ctk.CTkFrame(table, fg_color="transparent")
                        row_frame.pack(fill="x", pady=4)

                        ctk.CTkLabel(row_frame, text=pickup_id, font=self.FONT_ROW, width=self.column_widths[0], anchor="w", text_color="black").pack(side="left", padx=(12, 0))
                        ctk.CTkLabel(row_frame, text=product_name, font=self.FONT_ROW, width=self.column_widths[1], anchor="w", text_color="black").pack(side="left")
                        ctk.CTkLabel(row_frame, text=address, wraplength=230, font=self.FONT_ROW, width=self.column_widths[2], anchor="w", text_color="black").pack(side="left")

                        status_menu = ctk.CTkOptionMenu(
                              row_frame,
                              values=["Scheduled", "Picked", "Cancelled"],
                              command=lambda s, m=None, pid=pickup_id: self.update_pickup_status(m, s, pid, product_id),
                              font=self.BADGE_FONT,
                              width=110,
                              height=28,
                              corner_radius=12,
                              fg_color=self.STATUS_COLORS.get(status),
                              button_color=self.STATUS_COLORS.get(status),
                              dropdown_font=self.BADGE_FONT
                        )
                        status_menu.set(status)
                        status_menu.pack(side="left", padx=5)
                        command=lambda s, m=status_menu, pid=pickup_id, prod_id=product_id: self.update_pickup_status(m, s, pid, prod_id)


          def update_pickup_status(self, menu, new_status, pickup_id, product_id):
                  try:
                        query = "UPDATE pickup SET status = %s WHERE pickup_id = %s"
                        self.app.db.cursor.execute(query, (new_status, pickup_id))
                        self.app.db.db.commit()

                        if new_status.lower() == "picked":
                              try:
                                    self.app.db.cursor.execute(
                                          "INSERT INTO recycling (product_id, recycle_date) VALUES (%s, NOW())",
                                          (product_id,)
                                    )
                                    print(f"Product {product_id} added to recycling.")

                              except Exception as recycle_err:
                                          print("Failed to insert into recycling:", recycle_err)

                        color = self.STATUS_COLORS.get(new_status, "#DDDDDD")
                        if menu:
                              menu.configure(fg_color=color, button_color=color)
                              menu.set(new_status)

                  except Exception as e:
                        print("Failed to update pickup status:", e)

          def direct_delivery_screen(self):     
                  self.app.clear_content()

                  self.column_widths = [100, 200, 230, 230, 140]
                  self.headers = ["ORDER ID", "PRODUCT", "SELLER ADDRESS", "BUYER ADDRESS", "STATUS"]

                  self.FONT_TITLE = ("Helvetica", 18, "bold")
                  self.FONT_HEADER = ("Helvetica", 11, "bold")
                  self.FONT_ROW = ("Helvetica", 11)
                  self.BADGE_FONT = ("Helvetica", 10, "bold")

                  self.STATUS_COLORS = {
                        "pending": "#FFA500",     
                        "completed": "#00C851",  
                        "cancelled": "#E13D3A"  
                  }

                  table = ctk.CTkFrame(self.app.content_frame, corner_radius=15, fg_color="#f2f2f2")
                  table.place(relx=0.03, rely=0.13, relwidth=0.85, relheight=0.7)

                  header_frame = ctk.CTkFrame(table, fg_color="#dddddd", height=40)
                  header_frame.pack(fill="x")

                  for idx, h in enumerate(self.headers):
                        ctk.CTkLabel(
                              header_frame,
                              text=h,
                              font=self.FONT_HEADER,
                              text_color="#1B0303",
                              width=self.column_widths[idx],
                              anchor="w"
                        ).pack(side="left", padx=(12 if idx == 0 else 0, 0), pady=10)


                  query = """
                        SELECT 
                              o.order_id,
                              s.product_type,
                              s.pickup_location,
                              o.buyer_address,
                              o.status
                        FROM direct_sale_order o
                        JOIN direct_sale s ON o.sale_id = s.sale_id and o.status = "pending"
                  """
                  self.app.db.cursor.execute(query)
                  rows = self.app.db.cursor.fetchall()

                  for order_id, product_type, seller_address, buyer_address, status in rows:
                        row_frame = ctk.CTkFrame(table, fg_color="transparent")
                        row_frame.pack(fill="x", pady=4)

                        ctk.CTkLabel(row_frame, text=order_id, font=self.FONT_ROW, width=self.column_widths[0], anchor="w", text_color="black").pack(side="left", padx=(12, 0))
                        ctk.CTkLabel(row_frame, text=product_type, font=self.FONT_ROW, width=self.column_widths[1], anchor="w", text_color="black").pack(side="left")
                        ctk.CTkLabel(row_frame, text=seller_address, wraplength=210, font=self.FONT_ROW, width=self.column_widths[2], anchor="w", text_color="black").pack(side="left")
                        ctk.CTkLabel(row_frame, text=buyer_address, wraplength=210, font=self.FONT_ROW, width=self.column_widths[3], anchor="w", text_color="black").pack(side="left")

                        status_menu = ctk.CTkOptionMenu(
                              row_frame,
                              values=["pending", "completed", "cancelled"],
                              command=lambda s, m=None, oid=order_id: self.update_direct_delivery_status(m, s, oid),
                              font=self.BADGE_FONT,
                              width=110,
                              height=28,
                              corner_radius=12,
                              fg_color=self.STATUS_COLORS.get(status),
                              button_color=self.STATUS_COLORS.get(status),
                              dropdown_font=self.BADGE_FONT
                        )
                        status_menu.set(status)
                        status_menu.pack(side="left", padx=5)
                        status_menu._command = lambda s, m=status_menu, oid=order_id: self.update_direct_delivery_status(m, s, oid)


          def update_direct_delivery_status(self, menu, new_status, order_id):
                  try:
                        query = "UPDATE direct_sale_order SET status = %s WHERE order_id = %s"
                        self.app.db.cursor.execute(query, (new_status, order_id))
                        self.app.db.db.commit()
                        menu.configure(
                              fg_color=self.STATUS_COLORS.get(new_status),
                              button_color=self.STATUS_COLORS.get(new_status)
                        )
                  except Exception as e:
                        print("Failed to update direct order status:", e)



          def insp_notify(self):
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
