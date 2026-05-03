import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image


class Admin:
          def __init__(self, app):
                self.app = app
                self.main_frame = self.app.main_frame
                self.list_m = ["Users", "Inventory", "Managements", "Operators", "Negotiations", "Transactions", "Logistics"]

          def valid_admin(self):
                admin_code = self.admin_pass_entry.get().strip()

                valid_admins = ["a", "ajay24", "manish56", "shantanu57", "pawan"]
                if admin_code in valid_admins:
                        messagebox.showinfo("Success", "Successfully Logged In!")
                        self.app.ad_name = admin_code

                        self.admin_users_screen()
        
                else:
                        messagebox.showerror("Invalid", "Invalid Admin Code!")

          def admin_login(self):
                self.app.remove_head_content()
                self.app.clear_frame()

                img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                self.frame = ctk.CTkFrame(self.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                self.frame.place(relx=0.5, rely=0.5, anchor="center")

                admin_label = ctk.CTkLabel(self.frame, text="Administration", font=("Impact", 50), width=200, text_color="black")
                admin_label.place(relx=0.5, rely=0.1, anchor="center")

                admin_login_label = ctk.CTkLabel(self.frame, text="Login", font=("Impact", 50), width=380, text_color="black")
                admin_login_label.place(relx=0.5, rely=0.2, anchor="center")

                self.admin_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Name", width=380)
                self.admin_entry.place(relx=0.5, rely=0.4, anchor="center")

                self.admin_pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter admin login password", width=380)
                self.admin_pass_entry.place(relx=0.5, rely=0.5, anchor="center")

                login_button = ctk.CTkButton(self.frame, text="LOGIN", width=200, fg_color="black", text_color="white", border_width=2, border_color="grey", command=self.valid_admin)
                login_button.place(relx=0.5, rely=0.7, anchor="center")

                back_l = ctk.CTkLabel(self.frame, text="Back", font=("Arial", 14), text_color="blue")
                back_l.place(relx=0.5, rely=0.8, anchor="center")

                back_l.bind("<Button-1>", lambda e: self.app.rol.role_screen())

          
          def admin_negotiation_screen(self):
                self.app.clear_content()
                ctk.CTkLabel(
                              self.app.content_frame, 
                              text="Negotiations", 
                              text_color="black", 
                              font=("Impact", 50)
                    ).place(relx=0.5, rely=0.05, anchor="center")

                sell_id = ctk.CTkEntry(self.app.content_frame, placeholder_text="Enter Seller ID to Negotiate", height=40, width=300, font=("Arial", 20))
                sell_id.place(relx=0.5, rely=0.4, anchor="center")

                def check_seller():
                        seller_id = sell_id.get().strip()
                        self.app.db.cursor.execute("select name from seller where seller_id = %s", (seller_id,))
                        result = self.app.db.cursor.fetchone()

                        if result:
                                sell_id.destroy()

                                self.nego_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#ffffff", corner_radius=20)
                                self.nego_frame.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.5, anchor="center")

                                self.nego_head = ctk.CTkFrame(self.app.content_frame, height=60, corner_radius=0, fg_color="#A8F1FE")
                                self.nego_head.place(relx=0.5, rely=0.18, relwidth=0.5, anchor="center")

                                ctk.CTkLabel(self.nego_head, text="Admin", text_color="blue", font=("Arial", 20, "bold")).place(relx=0.5, rely=0.5, anchor="center")

                                messages = self.app.fm.get_negotiations(seller_id)

                                if messages:
                                        for msg in messages:
                                                sender = "You" if msg["sender"] == "seller" else "Admin"
                                                self.add_nego_message(sender, msg["message"])
                                else:
                                        self.add_nego_message("Admin", "No messages yet.")

                                self.msg_entry = ctk.CTkEntry(self.app.content_frame, placeholder_text="Type your message...", font=("Arial", 16), width=420, corner_radius=10)
                                self.msg_entry.place(relx=0.44, rely=0.83, anchor="center")

                                self.send_btn = ctk.CTkButton(
                                self.app.content_frame,
                                text="Send",
                                fg_color="#007bff",
                                hover_color="#005dc1",
                                command=lambda: self.send_nego_message(seller_id)
                                )
                                self.send_btn.place(relx=0.68, rely=0.83, anchor="center")

                ctk.CTkButton(self.app.content_frame, text="Search", height=50, width=150, fg_color="red", command=check_seller).place(relx=0.5, rely=0.6, anchor="center")

          def admin_users_screen(self):
                self.app.clear_frame()
                if self.app.content_frame:
                        self.app.clear_content()
                self.app.head_content_create("admin")

                self.list_m = [
                        "Users", "Inventory", "All Inspection", "Pending Pickups"
                        , "Pending Deliveries",
                        "Pending Payments", 
                         "Negotiation" ,"Feedbacks", "Reports" , "Products For Repair"
                ]

                self.app.me.menu_flag(items=self.list_m, type ="admin")

                self.notifications()


                frame = ctk.CTkFrame(self.app.content_frame, fg_color="#E5E7EB", corner_radius=15)
                frame.pack(padx=20, pady=20, fill="both", expand=True)

                button_frame = ctk.CTkFrame(frame, fg_color="transparent")
                button_frame.pack(pady=10)

                buyer_btn = ctk.CTkButton(button_frame, text="Show Buyers", command=self.show_buyers)
                buyer_btn.pack(side="left", padx=10)

                seller_btn = ctk.CTkButton(button_frame, text="Show Sellers", command=self.show_sellers)
                seller_btn.pack(side="left", padx=10)

                tree_frame = ctk.CTkFrame(frame, fg_color="transparent")
                tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

                
                vsb = ttk.Scrollbar(tree_frame, orient="vertical")
                vsb.pack(side="right", fill="y")

                self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "phone", "email", "address"), show="headings", yscrollcommand=vsb.set)
                vsb.config(command=self.tree.yview)

               
                for col in ("id", "name", "phone", "email", "address"):
                        self.tree.heading(col, text=col.capitalize(), anchor="center")
                        self.tree.column(col, anchor="center")

               
                self.tree.column("id", width=60)
                self.tree.column("name", width=150)
                self.tree.column("phone", width=130)
                self.tree.column("email", width=220)
                self.tree.column("address", width=250)

                
                style = ttk.Style()
                style.configure("Treeview", font=("Arial", 14), rowheight=30)  
                style.configure("Treeview.Heading", font=("Arial", 15, "bold"))

                self.tree.pack(fill="both", expand=True)

                self.show_buyers() 

          def show_buyers(self):
                if not hasattr(self, "tree"):
                        return 

                self.tree.delete(*self.tree.get_children())


                self.app.db.cursor.execute("SELECT buyer_id, name, phone_no, email, address FROM buyer")
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)


          def show_sellers(self):
                if not hasattr(self, "tree"):
                        return  

                self.tree.delete(*self.tree.get_children())

                self.app.db.cursor.execute("SELECT seller_id, name, phone_no, email, address FROM seller")
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)


                
          def admin_inventory_screen(self):
                self.render_table_screen("Inventory")

            
                bottom_frame = ctk.CTkFrame(self.app.content_frame, fg_color="transparent")
                bottom_frame.pack(fill="x", padx=20, pady=(5, 15), anchor="se")

                add_btn = ctk.CTkButton(
                        bottom_frame, 
                        text="+ Add Inventory", 
                        command=self.add_inventory_popup,
                        fg_color="#2563EB", 
                        font=("Arial", 14), 
                        width=160, 
                        height=40,
                        corner_radius=10
                )
                add_btn.pack(side="right", padx=10)
                
                self.load_inventory_data()


          def load_inventory_data(self):
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("inventory_id", "name", "type", "price_per_unit", "stock")

               
                self.tree.heading("inventory_id", text="Inventory ID", anchor="center")
                self.tree.heading("name", text="Name", anchor="center")
                self.tree.heading("type", text="Type", anchor="center")
                self.tree.heading("price_per_unit", text="Price per unit", anchor="center")
                self.tree.heading("stock", text="Stock", anchor="center")

                self.tree.column("inventory_id", anchor="center", width=120)
                self.tree.column("name", anchor="center", width=200)
                self.tree.column("type", anchor="center", width=160)
                self.tree.column("price_per_unit", anchor="center", width=160)
                self.tree.column("stock", anchor="center", width=100)

                self.app.db.cursor.execute("SELECT inventory_id, name, type, price_per_unit, stock FROM inventory")
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          
          def add_inventory_popup(self):
                popup = ctk.CTkToplevel()
                popup.title("Add Inventory")
                popup.geometry("400x400")

                name_entry = ctk.CTkEntry(popup, placeholder_text="Name")
                name_entry.pack(pady=10)

                type_entry = ctk.CTkEntry(popup, placeholder_text="Type")
                type_entry.pack(pady=10)

                price_entry = ctk.CTkEntry(popup, placeholder_text="Price per unit")
                price_entry.pack(pady=10)

                stock_entry = ctk.CTkEntry(popup, placeholder_text="Stock")
                stock_entry.pack(pady=10)

                def submit_inventory():
                        name = name_entry.get().strip()
                        type_ = type_entry.get().strip()
                        price = price_entry.get().strip()
                        stock = stock_entry.get().strip()

                        if not name or not price or not stock:
                                messagebox.showerror("Error", "Name, Price, and Stock are required")
                                return

                        try:
                                self.app.db.cursor.execute("INSERT INTO inventory (name, type, price_per_unit, stock) VALUES (%s, %s, %s, %s)",
                                                (name, type_, float(price), int(stock)))
                                self.app.db.db.commit()
                                
                                popup.destroy()
                                self.load_inventory_data()
                                messagebox.showinfo("Success", "Inventory item added successfully!")
                        except Exception as e:
                                messagebox.showerror("Database Error", str(e))

                submit_btn = ctk.CTkButton(popup, text="Add", command=submit_inventory)
                submit_btn.pack(pady=20)

          def admin_all_inspection_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(self.app.content_frame, text="All Inspected Products", font=("Arial", 24, "bold"), text_color="black").place(relx=0.5, rely=0.05, anchor="center")

                inn_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#E4E7EB")
                inn_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.9, anchor="center")

                get_all_inspection_data = self.app.fm.get_all_inspection_data() 

                if not get_all_inspection_data:
                        ctk.CTkLabel(self.app.content_frame, text="No inspection data found.", text_color="red").place(relx=0.5, rely=0.15, anchor="center")
                        return

                y = 0.12  
                spacing = 0.16  
                i = 0

                for product_id, info in get_all_inspection_data.items():
                        frame = ctk.CTkFrame(inn_frame, width=700, height=100, fg_color="#fcc1c1", corner_radius=12)
                        frame.grid(row=i, column=0, pady = 10, padx=100)

                        ctk.CTkLabel(frame, text=f"Product ID: {product_id}", font=("Arial", 16, "bold"), text_color="black").place(relx=0.02, rely=0.2)
                        ctk.CTkLabel(frame, text=f"Price: {info.get('price', 'N/A')}", font=("Arial", 14), text_color="black").place(relx=0.02, rely=0.55)
                        ctk.CTkLabel(frame, text=f"Condition: {info.get('condition', 'N/A')}", font=("Arial", 14), text_color="black").place(relx=0.4, rely=0.55)

                        y += spacing
                        i += 1


          def admin_pending_payments_screen(self):
                self.render_table_screen("Pending Payments")
                self.load_pending_payments_data()

          def load_pending_payments_data(self): 
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("payment_id", "buyer_id", "amount", "payment_method", "payment_status", "payment_date")

                self.tree.heading("payment_id", text="Payment ID", anchor="center")
                self.tree.heading("buyer_id", text="Buyer ID", anchor="center")
                self.tree.heading("amount", text="Amount", anchor="center")
                self.tree.heading("payment_method", text="Method", anchor="center")
                self.tree.heading("payment_status", text="Status", anchor="center")
                self.tree.heading("payment_date", text="Date", anchor="center")

                self.tree.column("payment_id", anchor="center", width=100)
                self.tree.column("buyer_id", anchor="center", width=100)
                self.tree.column("amount", anchor="center", width=120)
                self.tree.column("payment_method", anchor="center", width=100)
                self.tree.column("payment_status", anchor="center", width=100)
                self.tree.column("payment_date", anchor="center", width=180)

                
                self.app.db.cursor.execute("""
                        SELECT payment_id, buyer_id, amount, payment_method, payment_status, payment_date
                        FROM payments 
                        WHERE payment_status = 'pending'
                """)
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          
          def admin_pending_pickups_screen(self):
                self.render_table_screen("Pending Pickups")
                self.load_pending_pickups_data()

          def load_pending_pickups_data(self): 
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("pickup_id", "product_id", "seller_id", "pickup_date", "pickup_address", "status")

                self.tree.heading("pickup_id", text="Pickup ID", anchor="center")
                self.tree.heading("product_id", text="Product ID", anchor="center")
                self.tree.heading("seller_id", text="Seller ID", anchor="center")
                self.tree.heading("pickup_date", text="Pickup Date", anchor="center")
                self.tree.heading("pickup_address", text="Pickup Address", anchor="center")
                self.tree.heading("status", text="Status", anchor="center")

                self.tree.column("pickup_id", anchor="center", width=100)
                self.tree.column("product_id", anchor="center", width=100)
                self.tree.column("seller_id", anchor="center", width=100)
                self.tree.column("pickup_date", anchor="center", width=180)
                self.tree.column("pickup_address", anchor="center", width=250)
                self.tree.column("status", anchor="center", width=100)

                self.app.db.cursor.execute("""
                        SELECT pickup_id, product_id, seller_id, pickup_date, pickup_address, status 
                        FROM pickup 
                        WHERE status = 'Scheduled'
                """)
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          
          def admin_pending_deliveries_screen(self):
                self.render_table_screen("Pending Deliveries")
                self.load_pending_deliveries_data()

          def load_pending_deliveries_data(self): 
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("delivery_id", "buyer_id", "product_id", "delivery_address", "delivery_status")

                self.tree.heading("delivery_id", text="Delivery ID", anchor="center")
                self.tree.heading("buyer_id", text="Buyer ID", anchor="center")
                self.tree.heading("product_id", text="Product ID", anchor="center")
                self.tree.heading("delivery_address", text="Address", anchor="center")
                self.tree.heading("delivery_status", text="Status", anchor="center")

                self.tree.column("delivery_id", anchor="center", width=100)
                self.tree.column("buyer_id", anchor="center", width=100)
                self.tree.column("product_id", anchor="center", width=100)
                self.tree.column("delivery_address", anchor="center", width=250)
                self.tree.column("delivery_status", anchor="center", width=120)


                self.app.db.cursor.execute("""
                        SELECT order_id, buyer_id, payment_id, delivery_address, status 
                        FROM orders 
                        WHERE   status = 'Pending'
                """)
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          
          def admin_reports_screen(self):
                self.render_table_screen("Reports")
                self.load_reports_data()

          def load_reports_data(self):
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("report_id", "buyer_id", "seller_id", "report_type", "description", "evidence_path", "report_date")

                self.tree.heading("report_id", text="Report ID", anchor="center")
                self.tree.heading("buyer_id", text="Buyer ID", anchor="center")
                self.tree.heading("seller_id", text="Seller ID", anchor="center")
                self.tree.heading("report_type", text="Type", anchor="center")
                self.tree.heading("description", text="Description", anchor="center")
                self.tree.heading("evidence_path", text="Evidence", anchor="center")
                self.tree.heading("report_date", text="Date", anchor="center")

                self.tree.column("report_id", anchor="center", width=100)
                self.tree.column("buyer_id", anchor="center", width=100)
                self.tree.column("seller_id", anchor="center", width=100)
                self.tree.column("report_type", anchor="center", width=120)
                self.tree.column("description", anchor="center", width=300)
                self.tree.column("evidence_path", anchor="center", width=200)
                self.tree.column("report_date", anchor="center", width=180)

                self.app.db.cursor.execute("SELECT report_id, buyer_id, seller_id, report_type, description, evidence_path, report_date FROM report")
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          
          def admin_feedback_screen(self):
                self.render_table_screen("Feedbacks")
                self.load_feedback_data()
                
          def load_feedback_data(self):
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("feedback_id", "buyer_id", "seller_id", "rate", "review", "created_at")

                self.tree.heading("feedback_id", text="Feedback ID", anchor="center")
                self.tree.heading("buyer_id", text="Buyer ID", anchor="center")
                self.tree.heading("seller_id", text="Seller ID", anchor="center")
                self.tree.heading("rate", text="Rating", anchor="center")
                self.tree.heading("review", text="Review", anchor="center")
                self.tree.heading("created_at", text="Date", anchor="center")

                self.tree.column("feedback_id", anchor="center", width=100)
                self.tree.column("buyer_id", anchor="center", width=100)
                self.tree.column("seller_id", anchor="center", width=100)
                self.tree.column("rate", anchor="center", width=80)
                self.tree.column("review", anchor="center", width=300)
                self.tree.column("created_at", anchor="center", width=180)

                self.app.db.cursor.execute("SELECT feedback_id, buyer_id, seller_id, rate, review, created_at FROM feedback")
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          def admin_products_for_repair_screen(self):
                self.render_table_screen("Products for Repair")
                self.load_products_for_repair()

          def load_products_for_repair(self): 
                if not hasattr(self, "tree"):
                        return

                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = ("recycle_id", "product_id", "product_name", "recycle_date", "status")

                self.tree.heading("recycle_id", text="Recycle ID", anchor="center")
                self.tree.heading("product_id", text="Product ID", anchor="center")
                self.tree.heading("product_name", text="Product Name", anchor="center")
                self.tree.heading("recycle_date", text="Recycle Date", anchor="center")
                self.tree.heading("status", text="Status", anchor="center")

                self.tree.column("recycle_id", anchor="center", width=100)
                self.tree.column("product_id", anchor="center", width=100)
                self.tree.column("product_name", anchor="center", width=150)
                self.tree.column("recycle_date", anchor="center", width=180)
                self.tree.column("status", anchor="center", width=120)

                self.app.db.cursor.execute("""
                        SELECT 
                        r.recycle_id, 
                        r.product_id, 
                        p.product_type AS product_name, 
                        r.recycle_date, 
                        r.status 
                        FROM recycling r
                        JOIN product p ON r.product_id = p.product_id
                        WHERE r.status = 'Pending'
                """)
                rows = self.app.db.cursor.fetchall()
                for row in rows:
                        self.tree.insert("", "end", values=row)

          def render_table_screen(self, title, btn1_func=None, btn2_func=None):
                self.app.clear_content()

                frame = ctk.CTkFrame(self.app.content_frame, fg_color="#E5E7EB", corner_radius=15)
                frame.pack(padx=20, pady=20, fill="both", expand=True)

                if btn1_func and btn2_func:
                        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
                        button_frame.pack(pady=10)

                        ctk.CTkButton(button_frame, text="Show Buyers", command=btn1_func).pack(side="left", padx=10)
                        ctk.CTkButton(button_frame, text="Show Sellers", command=btn2_func).pack(side="left", padx=10)

                tree_frame = ctk.CTkFrame(frame, fg_color="transparent")
                tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

                vsb = ttk.Scrollbar(tree_frame, orient="vertical")
                vsb.pack(side="right", fill="y")

                self.tree = ttk.Treeview(tree_frame, show="headings", yscrollcommand=vsb.set)
                vsb.config(command=self.tree.yview)

                style = ttk.Style()
                style.configure("Treeview", font=("Arial", 14), rowheight=30)
                style.configure("Treeview.Heading", font=("Arial", 15, "bold"))

                self.tree.pack(fill="both", expand=True)


          def notifications(self):
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

          def send_nego_message(self, seller_id):
                text = self.msg_entry.get().strip()
                if text:
                        self.app.fm.add_negotiation_message(seller_id, "Admin", text)
                        self.add_nego_message("Admin", text)
                        self.msg_entry.delete(0, "end")


          def add_nego_message(self, sender, msg):
                color = "blue" if sender == "Admin" else "green"
                ctk.CTkLabel(
                        self.nego_frame, 
                        text=f"{sender}: {msg}", 
                        text_color=color, 
                        font=("Arial", 16),
                        anchor="w"
                ).pack(anchor="w" if sender == "Admin" else "e", padx=10, pady=5)