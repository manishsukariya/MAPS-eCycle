import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import shutil
import json

class Seller:
          def __init__(self, app):
                    self.app = app
                    self.anyy = None
                    self.small_frame = {}

                    self.uploaded_images = []

                    self.UPLOAD_DIR = "uploads"
                    os.makedirs(self.UPLOAD_DIR, exist_ok=True)

                    self.rating = 0
                    self.star_buttons = []


          def seller_screen(self):
                    self.app.clear_frame()
                    if self.app.content_frame:
                              self.app.clear_content()

                    self.app.head_content_create("seller")

                    ctk.CTkLabel(self.app.content_frame, text="Dashboard", font=("Impact", 60), text_color="Black").place(relx=0.5, rely=0.08, anchor="center")


                    menu_list = ["Dashboard", "Sell", "Status", "Direct B to S", "Negociations", "History", "Feedback", "Report"]

                    self.app.me.menu_flag(menu_list, "seller")

                    dash_items1 = ["Sell", "Seller to Buyer", "Negotiations"]
                    dash_items2 = ["Status", "History", "Report"]

                    self.dash_items = (dash_items1, dash_items2)

                    for j in range(1, 3):
                              self.small_frame[j] = ctk.CTkFrame(self.app.content_frame, fg_color="white", corner_radius=20)
                              self.small_frame[j].place(relx=0.5, rely=0.33 * j + 0.05, relheight=0.27, relwidth=0.8, anchor="center")

                              for i, name in enumerate(self.dash_items[j-1], 1):
                                        btn = ctk.CTkButton(
                                        self.small_frame[j],
                                        text=name,
                                        font=("Impact", 26),
                                        text_color="#1E3A8A",     
                                        corner_radius=20,
                                        fg_color="#E0E7FF",      
                                        hover_color="#93C5FD",
                                        border_width=0.2,
                                        border_color="Black", 
                                        command=lambda n = name: self.dash_btn_check(n)   
                                        )
                                        btn.place(relx=(0.33 * i) - 0.165, rely=0.5, relheight=0.75, relwidth=0.25, anchor="center")
                                        if i == 3:
                                                  break
                                        
                              self.app.db.cursor.execute("SELECT seller_id FROM seller WHERE email=%s", (self.app.p_mail,))
                              self.seller_id = self.app.db.cursor.fetchone()[0]

                    
                    self.seller_notify()

          def dash_btn_check(self, n):
                  if n == "Sell":
                          self.seller_sell_screen()
                  elif n == "Seller to Buyer":
                          self.seller_b_to_s_screen()
                  elif n == "Negotiations":
                          self.seller_nego_screen()
                  elif n == "Status":
                          self.seller_status_screen()
                  elif n == "History":
                          self.seller_history_screen()
                  elif n == "Report":
                          self.seller_report_screen()                    

          def seller_sell_screen(self):
                    self.app.clear_content()
                    self.app.update_idletasks()


                    ctk.CTkLabel(self.app.content_frame, text="Sell Product", text_color="black", font=("Impact", 50)).place(relx=0.5, rely=0.05, anchor="center")


                    self.sell_frame = ctk.CTkFrame(self.app.content_frame, fg_color="white", corner_radius=20)
                    self.sell_frame.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.35, anchor="center")

                    self.scroll_frame = ctk.CTkScrollableFrame(self.sell_frame, fg_color="#ffffff", corner_radius=20)
                    self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

                    row = 0

                    title = ctk.CTkLabel(self.scroll_frame, text="Submit E-waste for Valuation",
                                        font=("Arial", 22, "bold"), text_color="#155724", anchor="center")
                    title.grid(row=row, column=0, pady=(10, 15), sticky="ew")

                    row += 1
                    self.add_label("Product Type", row)

                    row += 1
                    self.product_type = ctk.CTkComboBox(self.scroll_frame,
                                                            values=["Mobile", "Laptop", "Tablet", "Other"],
                                                            font=("Arial", 14), corner_radius=10,
                                                            command=self.handle_product_type)
                    self.product_type.set("Select Product Type")
                    self.product_type.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1
                    self.other_row = row
                    self.other_entry = ctk.CTkEntry(self.scroll_frame, font=("Arial", 14),
                                                            placeholder_text="Enter product type", corner_radius=10)
                    self.other_entry.grid(row=self.other_row, column=0, pady=5, sticky="ew")
                    self.other_entry.grid_remove()

                    row += 1
                    self.add_label("Brand", row)

                    row += 1
                    self.brand_entry = ctk.CTkEntry(self.scroll_frame, font=("Arial", 14),
                                                            placeholder_text="Enter Brand", corner_radius=10)
                    self.brand_entry.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1
                    self.add_label("Model", row)

                    row += 1
                    self.model_entry = ctk.CTkEntry(self.scroll_frame, font=("Arial", 14),
                                                            placeholder_text="Enter Model", corner_radius=10)
                    self.model_entry.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1
                    self.add_label("Condition", row)

                    row += 1
                    self.condition_box = ctk.CTkComboBox(self.scroll_frame,
                                                            values=["Poor", "Moderate", "Good"],
                                                            font=("Arial", 14), corner_radius=10)
                    self.condition_box.set("Select Condition")
                    self.condition_box.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1

                    ctk.CTkLabel(self.scroll_frame, text="Price", font=("Arial", 14, "bold"), text_color="#1b1b1b") \
                    .grid(row=row, column=0, pady=(10, 0), sticky="w")
                    row += 1
                    self.price_entry = ctk.CTkEntry(self.scroll_frame, font=("Arial", 14),
                                                  placeholder_text="Enter Price", corner_radius=10)
                    self.price_entry.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1
                    ctk.CTkLabel(self.scroll_frame, text="Quantity", font=("Arial", 14, "bold"), text_color="#1b1b1b") \
                    .grid(row=row, column=0, pady=(10, 0), sticky="w")
                    row += 1
                    self.qty_entry = ctk.CTkEntry(self.scroll_frame, font=("Arial", 14),
                                                  placeholder_text="Enter Quantity", corner_radius=10)
                    self.qty_entry.grid(row=row, column=0, pady=5, sticky="ew")

                    row += 1
                    self.add_label("Pickup Location", row)

                    row += 1
                    self.pickup_btn = ctk.CTkButton(self.scroll_frame, text="Select Location on Map",
                                                  font=("Arial", 14), corner_radius=10,
                                                  fg_color="#28a745", hover_color="#218838",
                                                  command=self.get_location)
                    self.pickup_btn.grid(row=row, column=0, pady=10, sticky="ew")

                    row += 1
                    self.location_label = ctk.CTkLabel(self.scroll_frame, text="No location selected",
                                                  font=("Arial", 12), text_color="gray", wraplength=300)
                    self.location_label.grid(row=row, column=0, pady=5, sticky="w")

                    self.location_label.configure(text=f"Selected: {self.app.mp.address}")


                    row += 1
                    self.add_label("Product Images", row)

                    row += 1
                    self.upload_btn = ctk.CTkButton(self.scroll_frame, text="⬆ Upload Images",
                                                  command=self.upload_images, font=("Arial", 14), corner_radius=10,
                                                  fg_color="#28a745", hover_color="#218838")
                    self.upload_btn.grid(row=row, column=0, pady=5, sticky="w")

                    row += 1
                    self.image_label = ctk.CTkLabel(self.scroll_frame, text="No images selected.",
                                                            font=("Arial", 12), text_color="gray")
                    self.image_label.grid(row=row, column=0, pady=5, sticky="w")

                    row += 1
                    self.note = ctk.CTkLabel(self.scroll_frame, text="Max 5 images, up to 10MB each.",
                                        font=("Arial", 12), text_color="gray")
                    self.note.grid(row=row, column=0, pady=(0, 10), sticky="w")

                    row += 1
                    self.submit_btn = ctk.CTkButton(self.scroll_frame, text="Valuation",
                                                  command=self.submit_form, font=("Arial", 16, "bold"),
                                                  height=45, corner_radius=12,
                                                  fg_color="#007bff", hover_color="#005dc1")
                    self.submit_btn.grid(row=row, column=0, pady=(10, 20), sticky="ew")

                    row += 1
                    self.success_box = ctk.CTkLabel(self.scroll_frame, text="",
                                                            font=("Arial", 13), text_color="#004085",
                                                            fg_color="#d1ecf1", corner_radius=10)
                    self.success_box.grid(row=row, column=0, pady=(5, 10), sticky="ew")
                    self.success_box.grid_remove()


                    self.back_btn = ctk.CTkButton(self.app.content_frame, text="Back", fg_color="#0F172A", border_color="white", font=("Arial", 26, "bold"), command= self.seller_screen)
                    self.back_btn.place(relx=0.5, rely=0.95, anchor="center")

                    

          def seller_status_screen(self):
                self.app.clear_content()


                ctk.CTkLabel(
                              self.app.content_frame, 
                              text="Status", 
                              text_color="black", 
                              font=("Impact", 50)
                    ).place(relx=0.5, rely=0.1, anchor="center")

                self.st_frame = ctk.CTkFrame(self.app.content_frame, height=60, fg_color="White")
                self.st_frame.place(relx=0.5, rely=0.25, relwidth=0.8, anchor="center")

                ctk.CTkLabel(self.st_frame, text="Product_Type", text_color="black", font=("Arial", 30)).place(relx=0.1, rely=0.5, anchor="center")
                ctk.CTkLabel(self.st_frame, text="Brand", text_color="black", font=("Arial", 30)).place(relx=0.3, rely=0.5, anchor="center")
                ctk.CTkLabel(self.st_frame, text="Price", text_color="black", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")
                ctk.CTkLabel(self.st_frame, text="Quantity", text_color="black", font=("Arial", 30)).place(relx=0.7, rely=0.5, anchor="center")
                ctk.CTkLabel(self.st_frame, text="Status", text_color="black", font=("Arial", 30)).place(relx=0.9, rely=0.5, anchor="center")

                query = "select product_type, brand, price, quantity, status from product where seller_id = %s"
                self.app.db.cursor.execute(query, (self.seller_id, ))
                result = self.app.db.cursor.fetchall()

                if not result:
                        ctk.CTkLabel(
                        self.st_frame,
                        text="No products found!",
                        text_color="red",
                        font=("Arial", 22, "bold")
                        ).pack(pady=20)
                        return

                
                for i, row in enumerate(result, start=0):
                        sts_frame = ctk.CTkFrame(self.app.content_frame, fg_color="white", height=60, corner_radius=10)
                        sts_frame.place(relx=0.5, rely=0.35 + ((i * 10)/100), relwidth=0.8, anchor="center")

                        for i, value in enumerate(row):
                                if i == 4:
                                        status_color = "gray"
                                        status_text = row[4].capitalize()

                                        if row[4] == "pending":
                                                status_color = "#FFD700"
                                        elif row[4] == "approved":
                                                status_color = "#32CD32"
                                        else:
                                                status_color = "#FF4C4C"

                                        status_frame = ctk.CTkFrame(
                                        sts_frame,
                                        width=120,
                                        height=40,
                                        fg_color=status_color,
                                        corner_radius=8
                                        )
                                        status_frame.place(relx=0.1 + (i * 0.2), rely=0.5, anchor="center")

                                        status_label = ctk.CTkLabel(
                                        status_frame,
                                        text=status_text,
                                        font=("Arial", 20, "bold"),
                                        text_color="white"
                                        )
                                        status_label.place(relx=0.5, rely=0.5, anchor="center")

                                else:
                                        lal = ctk.CTkLabel(
                                        sts_frame,
                                        text=str(value),
                                        font=("Arial", 30),
                                        text_color="black"
                                        )
                                        lal.place(relx=0.1 + (i * 0.2), rely=0.5, anchor="center")


          def seller_nego_screen(self):
                    self.app.clear_content()

                    ctk.CTkLabel(
                              self.app.content_frame, 
                              text="Negotiations", 
                              text_color="black", 
                              font=("Impact", 50)
                    ).place(relx=0.5, rely=0.05, anchor="center")

                    self.nego_frame = ctk.CTkScrollableFrame(
                              self.app.content_frame, 
                              fg_color="#ffffff", 
                              corner_radius=20
                    )
                    self.nego_frame.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.5, anchor="center")

                    self.nego_head = ctk.CTkFrame(
                              self.app.content_frame, 
                              height=60, 
                              corner_radius=0, 
                              fg_color="#A8F1FE"
                    )
                    self.nego_head.place(relx=0.5, rely=0.18, relwidth=0.5, anchor="center")

                    ctk.CTkLabel(
                              self.nego_head, 
                              text="Admin", 
                              text_color="blue", 
                              font=("Arial", 20, "bold")
                    ).place(relx=0.5, rely=0.5, anchor="center")

                    messages = self.app.fm.get_negotiations(self.seller_id)

                    if messages:
                           for msg in messages:
                                  sender = "You" if msg["sender"] == "seller" else "Admin"
                                  self.add_nego_message(sender, msg["message"])
                    else:
                                self.add_nego_message("Admin", "No messages yet.")


                    self.msg_entry = ctk.CTkEntry(
                              self.app.content_frame, 
                              placeholder_text="Type your message...", 
                              font=("Arial", 16),
                              width=420,
                              corner_radius=10
                    )
                    self.msg_entry.place(relx=0.44, rely=0.83, anchor="center")

                    self.send_btn = ctk.CTkButton(
                              self.app.content_frame, 
                              text="Send", 
                              fg_color="#007bff", 
                              hover_color="#005dc1", 
                              command=self.send_nego_message
                    )
                    self.send_btn.place(relx=0.68, rely=0.83, anchor="center")

          def seller_b_to_s_screen(self):
                    self.app.clear_content()

                    self.seller_sell_screen()

                    self.upload_btn.configure(command=self.upload_single_image)
                    self.note.configure(text="Select One Photo of Your Product")

                    self.submit_btn.configure(command = self.submit_form_buyer)


          def seller_history_screen(self):
                self.app.clear_content()

                ctk.CTkLabel(
                        self.app.content_frame,
                        text="Product History",
                        text_color="black",
                        font=("Impact", 50)
                ).place(relx=0.5, rely=0.05, anchor="center")

                frame = ctk.CTkFrame(self.app.content_frame, fg_color="white", corner_radius=15)
                frame.place(relx=0.5, rely=0.55, relheight=0.7, relwidth=0.9, anchor="center")

                columns = ("Product Type", "Brand", "Model", "Price", "Quantity", "Status")

                style = ttk.Style()
                style.configure("Treeview.Heading", font=("Arial", 14, "bold"), foreground="black")
                style.configure("Treeview", font=("Arial", 12), rowheight=30, background="white", fieldbackground="white")

                tree = ttk.Treeview(frame, columns=columns, show="headings")
                tree.pack(fill="both", expand=True)

                for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=120, anchor="center")

                self.app.db.cursor.execute(
                        "SELECT product_type, brand, model, price, quantity, status "
                        "FROM product WHERE seller_id = %s ORDER BY upload_date DESC",
                        (self.seller_id,)
                )
                products = self.app.db.cursor.fetchall()

                for row in products:
                        tree.insert("", "end", values=row)

          def seller_feedback_screen(self):
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


          def seller_report_screen(self):
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

          def send_nego_message(self):
                text = self.msg_entry.get().strip()
                if text:
                        self.app.fm.add_negotiation_message(self.seller_id, "seller", text)
                        self.add_nego_message("Seller", text)
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



          def seller_profile(self):
                if self.anyy:
                        self.anyy.destroy()
                        self.anyy = None
                    
                  
                mail = self.app.p_mail

                query = f"select seller_id, name, phone_no, email, address from seller where email=%s"

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

                self.app.bind("<Button-1>", self.check_click_outside_profile, add="+")

                back_btn = ctk.CTkLabel(self.pro_frame, text="Back", text_color="blue", fg_color="transparent", font=("Arial", 15))
                back_btn.place(relx=0.5, rely=0.95, anchor="center")
                back_btn.bind("<Button-1>", lambda e: self.remove_profile())

                self.pro_frame.bind("<Button-1>", lambda e: "break")

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

                self.app.unbind("<Button-1>")


          def seller_notify(self):
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
                    
                    if not self.app.mg.msg_frame:
                            self.app.mg.create_msg_frame(qwerty)


          def submit_fb(self):
                    mail = self.app.p_mail
                    rate = self.rating
                    review = self.fb_text.get("1.0", "end-1c").lower()
                    try:
                              self.app.db.cursor.execute("select seller_id from seller where email = %s", (mail, ))
                              seller_id = self.app.db.cursor.fetchone()[0]
                              print(seller_id)

                              query = "insert into feedback (seller_id, rate, review) values (%s, %s, %s)"
                              self.app.db.cursor.execute(query, (seller_id, rate, review))
                              self.app.db.db.commit()
                              print("done")
                              return self.after_fb()

                    except Exception as e:
                              return f"Database Error: {e}"
                    
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

                    self.app.db.cursor.execute(f"select seller_id from seller where email = %s", (self.app.p_mail, ))
                    id = self.app.db.cursor.fetchone()

                    what = self.app.db.submit_report_all("seller", id[0], r_type, desc, files_path)

                    if what == "S":
                            self.app.clear_content()

                            ctk.CTkLabel(self.app.content_frame, text=f"Report Submitted, \n Thank You For Reporting...!!", text_color="Black", font=("Impact", 30)).place(relx=0.5, rely=0.5, anchor="center")

                    else:
                            self.seller_report_screen()


          def get_location(self):
                    self.app.mp.get_map(self.set_pickup_address)

          def set_pickup_address(self, address):
                    self.pickup_location = address
                    self.location_label.configure(text=f"Address: {address}")

          def add_label(self, text, row):
                    label = ctk.CTkLabel(self.scroll_frame, text=text,
                                        font=("Arial", 14, "bold"), anchor="w", text_color="#1b1b1b")
                    label.grid(row=row, column=0, pady=(10, 0), sticky="w")

          def handle_product_type(self, choice):
                    if choice == "Other":
                              self.other_entry.grid()
                    else:
                              self.other_entry.grid_remove()

          def upload_single_image(self):
                file = filedialog.askopenfilename(
                        title="Select an Image",
                        filetypes=[("Images", "*.jpg *.jpeg *.png")]
                )

                if not file:
                        return

                file_name = os.path.basename(file)
                dest_folder = "uploads/s_to_b"
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, file_name)

                if not os.path.exists(dest_path):
                        shutil.copy(file, dest_path)

                self.uploaded_images = [file]
                self.image_label.configure(text=file_name)

                self.image_path = dest_path


          def upload_images(self):
                files = filedialog.askopenfilenames(
                        title="Select up to 5 Images",
                        filetypes=[("Images", "*.jpg *.jpeg *.png")],
                        multiple=True
                )

                if not files:
                        return

                if not hasattr(self, "uploaded_images"):
                        self.uploaded_images = []

                for file_path in files:
                        if len(self.uploaded_images) >= 5:
                                break

                        file_name = os.path.basename(file_path)
                        dest_folder = "uploads/recycling"
                        os.makedirs(dest_folder, exist_ok=True)

                        dest_path = os.path.join(dest_folder, file_name)

                        if not os.path.exists(dest_path):
                                shutil.copy(file_path, dest_path)

                        if dest_path not in self.uploaded_images:
                                self.uploaded_images.append(dest_path)

                if len(self.uploaded_images) > 5:
                        messagebox.showwarning("Limit Exceeded", "You can upload up to 5 images only.")
                        self.uploaded_images = self.uploaded_images[:5]

                names = ", ".join([os.path.basename(f) for f in self.uploaded_images])
                self.image_label.configure(text=names if names else "No images selected.")

                self.image_paths_json = json.dumps(self.uploaded_images)



          def submit_form(self):
                        type = self.other_entry.get().strip() if self.product_type.get() == "Other" else self.product_type.get()
                        brand = self.brand_entry.get().strip()
                        model = self.model_entry.get().strip()
                        condition = self.condition_box.get()
                        price = self.price_entry.get().strip()
                        qty = self.qty_entry.get().strip()
                        pickup = getattr(self, "pickup_location", None)

                        if not type or not brand or not model or not price or not qty or condition == "Select Condition" or not pickup:
                                messagebox.showerror("Missing Info", "Please fill all required fields and select pickup location.")
                                return

                        for img in self.uploaded_images:
                              dest = os.path.join(self.UPLOAD_DIR, os.path.basename(img))
                              if not os.path.exists(dest):
                                        shutil.copy(img, dest)

                        img_json = json.dumps(self.uploaded_images)

                        self.success_box.configure(text="Your product details have been submitted.\nWe will contact you soon.")
                        self.success_box.grid()

                        self.app.db.cursor.execute("select seller_id from seller where email=%s", (self.app.p_mail, ))
                        id  = self.app.db.cursor.fetchone()[0]
                        print(id)

                        wh = self.app.db.submit_product(id, type, brand, model, condition, price, qty, pickup, img_json)

                        if wh == "S":
                                self.success_box.configure(text="Product submitted successfully!")
                                self.success_box.grid()
                        else:
                                messagebox.showerror("Error", wh)

          def submit_form_buyer(self):
                product_type = self.other_entry.get().strip() if self.product_type.get() == "Other" else self.product_type.get()
                brand = self.brand_entry.get().strip()
                model = self.model_entry.get().strip()
                condition = self.condition_box.get()
                price = self.price_entry.get().strip()
                qty = self.qty_entry.get().strip()
                location = self.location_label.cget("text").replace("Address: ", "")

                if not product_type or not brand or not model or not price or not qty or condition == "Select Condition":
                        messagebox.showerror("Missing Info", "Please fill all required fields.")
                        return

                try:
                        seller_price = float(price)
                        buyer_price = round(seller_price * 1.10, 2)  # +10% profit
                except ValueError:
                        messagebox.showerror("Invalid Price", "Please enter a valid price.")
                        return

                image_paths = []
                for img in self.uploaded_images:
                        dest = os.path.join(self.UPLOAD_DIR, os.path.basename(img))
                        if not os.path.exists(dest):
                                shutil.copy(img, dest)
                        image_paths.append(dest)

                self.app.db.cursor.execute("SELECT seller_id FROM seller WHERE email=%s", (self.app.p_mail,))
                seller_id = self.app.db.cursor.fetchone()[0]

                self.app.db.cursor.execute(
                        "INSERT INTO direct_sale (seller_id, product_type, brand, model, `condition`, seller_price, buyer_price, quantity, pickup_location, image_paths) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (seller_id, product_type, brand, model, condition, seller_price, buyer_price, qty, location, json.dumps(image_paths))
                )
                self.app.db.db.commit()

                self.success_box.configure(text=f"Product listed for buyer. Buyer price: ₹{buyer_price}")
                self.success_box.grid()



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
