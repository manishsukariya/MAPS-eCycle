import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json


class Recycler:
          def __init__(self, app):
                  self.app = app


          def valid_recycler(self):
                    rec_code = self.recycler_pass_entry.get().strip()

                    valid_rec = ["a"]
                    if rec_code in valid_rec:
                              messagebox.showinfo("Success", "Successfully Logged In!")

                              self.recycler_screen()
          
                    else:
                              messagebox.showerror("Invalid", "Invalid Admin Code!")

          def recycler_login(self):
                self.app.remove_head_content()
                self.app.clear_frame()

                img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                ctk.CTkLabel(self.app.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                self.frame = ctk.CTkFrame(self.app.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                self.frame.place(relx=0.5, rely=0.5, anchor="center")

                admin_label = ctk.CTkLabel(self.frame, text="Recyclers", font=("Impact", 50), width=200, text_color="black")
                admin_label.place(relx=0.5, rely=0.1, anchor="center")

                admin_login_label = ctk.CTkLabel(self.frame, text="Login", font=("Impact", 50), width=380, text_color="black")
                admin_login_label.place(relx=0.5, rely=0.2, anchor="center")

                self.recycler_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Name", width=380)
                self.recycler_entry.place(relx=0.5, rely=0.4, anchor="center")

                self.recycler_pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Recycler login password", width=380)
                self.recycler_pass_entry.place(relx=0.5, rely=0.5, anchor="center")

                login_button = ctk.CTkButton(self.frame, text="LOGIN", width=200, fg_color="black", text_color="white", border_width=2, border_color="grey", command=self.valid_recycler)
                login_button.place(relx=0.5, rely=0.7, anchor="center")

                back_l = ctk.CTkLabel(self.frame, text="Back", font=("Arial", 14), text_color="blue")
                back_l.place(relx=0.5, rely=0.8, anchor="center")

                back_l.bind("<Button-1>", lambda e: self.app.rol.role_screen())
                    

          def recycler_screen(self):
                  self.app.clear_frame()
                  if self.app.content_frame:
                              self.app.clear_content()
                  self.app.head_content_create("recycler")

                  ctk.CTkLabel(self.app.content_frame, text="Dashboard", font=("Impact", 60), text_color="Black").place(relx=0.5, rely=0.08, anchor="center")

                  self.list_m = ["recyclings"]
                  self.app.me.menu_flag(self.list_m, "recycler")

                  heading = ctk.CTkLabel(self.app.content_frame, text="Recycling", font=("Arial", 24, "bold"))
                  heading.place(relx=0.5, rely=0.05, anchor="center")

                  query = """
                        SELECT r.recycle_id, p.product_type, r.recycle_date, r.status
                        FROM recycling r
                        JOIN product p ON r.product_id = p.product_id
                        ORDER BY r.recycle_date DESC
                  """
                  self.app.db.cursor.execute(query)
                  records = self.app.db.cursor.fetchall()

                  y = 0.15
                  for record in records:
                        recycle_id, product_name, recycle_date, status = record

                        product_label = ctk.CTkLabel(self.app.content_frame, text=f"{product_name} | ID: {recycle_id}", font=("Arial", 16))
                        product_label.place(relx=0.1, rely=y)

                        date_label = ctk.CTkLabel(self.app.content_frame, text=f"Recycled On: {recycle_date.strftime('%Y-%m-%d %H:%M:%S')}", font=("Arial", 14))
                        date_label.place(relx=0.1, rely=y + 0.05)

                        status_label = ctk.CTkLabel(self.app.content_frame, text=f"Status: {status}", font=("Arial", 14), text_color="green" if status == "Completed" else "orange" if status == "In Process" else "red")
                        status_label.place(relx=0.1, rely=y + 0.1)

                        y += 0.18  # spacing between entries


                  self.rec_notify()

          def recycler_screen(self):
                  self.app.clear_frame()
                  if self.app.content_frame:
                              self.app.clear_content()
                  self.app.head_content_create("recycler")

                  ctk.CTkLabel(self.app.content_frame, text="Recyclings", font=("Impact", 60), text_color="Black").place(relx=0.5, rely=0.08, anchor="center")

                  self.list_m = ["recyclings"]
                  self.app.me.menu_flag(self.list_m, "recycler")
                  self.column_widths = [100, 270, 200, 150]
                  self.headers = ["RECYCLE ID", "PRODUCT", "RECYCLE DATE", "STATUS"]

                  self.FONT_TITLE = ("Helvetica", 18, "bold")
                  self.FONT_HEADER = ("Helvetica", 11, "bold")
                  self.FONT_ROW = ("Helvetica", 11)
                  self.BADGE_FONT = ("Helvetica", 10, "bold")

                  self.STATUS_COLORS = {
                        "Pending": "#FFB300",
                        "In Process": "#33B5E5",
                        "Completed": "#00C851"
                  }

                  table = ctk.CTkFrame(self.app.content_frame, corner_radius=15, fg_color="#f2f2f2")
                  table.place(relx=0.03, rely=0.13, relwidth=0.75, relheight=0.7)

                  # Header row
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

                  # Fetch and show recycling records
                  query = """
                        SELECT r.recycle_id, p.product_type, r.recycle_date, r.status
                        FROM recycling r
                        JOIN product p ON r.product_id = p.product_id
                  """
                  self.app.db.cursor.execute(query)
                  rows = self.app.db.cursor.fetchall()

                  for recycle_id, product_name, recycle_date, status in rows:
                        row_frame = ctk.CTkFrame(table, fg_color="transparent")
                        row_frame.pack(fill="x", pady=4)

                        ctk.CTkLabel(row_frame, text=recycle_id, font=self.FONT_ROW,
                                    width=self.column_widths[0], anchor="w", text_color="black").pack(side="left", padx=(12, 0))
                        ctk.CTkLabel(row_frame, text=product_name, font=self.FONT_ROW,
                                    width=self.column_widths[1], anchor="w", text_color="black").pack(side="left")
                        ctk.CTkLabel(row_frame, text=str(recycle_date), font=self.FONT_ROW,
                                    width=self.column_widths[2], anchor="w", text_color="black").pack(side="left")

                        status_menu = ctk.CTkOptionMenu(
                              row_frame,
                              values=["Pending", "In Process", "Completed"],
                              command=lambda s, m=None, rid=recycle_id: self.update_recycle_status(m, s, rid),
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
                        status_menu._command = lambda s, m=status_menu, rid=recycle_id: self.update_recycle_status(m, s, rid)

                  self.rec_notify()

          def update_recycle_status(self, menu_widget, new_status, recycle_id):
                  query = "UPDATE recycling SET status = %s WHERE recycle_id = %s"
                  self.app.db.cursor.execute(query, (new_status, recycle_id))
                  self.app.db.db.commit()

                  # Change color of menu
                  menu_widget.configure(
                        fg_color=self.STATUS_COLORS[new_status],
                        button_color=self.STATUS_COLORS[new_status]
                  )

                  
                  if new_status == "Completed":
                        try:
                              
                              self.app.db.cursor.execute("SELECT product_id FROM recycling WHERE recycle_id = %s", (recycle_id,))
                              result = self.app.db.cursor.fetchone()
                              print("pid")
                              if not result:
                                    return
                              product_id = result[0]

                             
                              self.app.db.cursor.execute("""
                              SELECT product_type, brand, price, quantity, image_paths
                              FROM product
                              WHERE product_id = %s
                              """, (product_id,))
                              prod = self.app.db.cursor.fetchone()
                              print("pd")
                              if not prod:
                                    return

                              product_type, brand, price, quantity, image_json = prod
                              image_paths = json.loads(image_json) if image_json else []
                              first_image = image_paths[0] if image_paths else ""

                              
                              self.app.db.cursor.execute("""
                              SELECT inventory_id, stock FROM inventory WHERE type = %s
                              """, (product_type, ))
                              inv = self.app.db.cursor.fetchone()
                              print(inv)

                              if inv:
                              
                                    inventory_id, stock = inv
                                    new_stock = stock + quantity
                                    self.app.db.cursor.execute("UPDATE inventory SET stock = %s WHERE inventory_id = %s", (new_stock, inventory_id))
                                    print("up")
                              else:
                              
                                    self.app.db.cursor.execute("""
                                          INSERT INTO inventory (name, type, price_per_unit, stock, image_path)
                                          VALUES (%s, %s, %s, %s, %s)
                                    """, (product_type, product_type.lower(), price, quantity, first_image))
                                    print("last")

                              self.app.db.db.commit()

                        except Exception as e:
                              self.app.db.db.rollback()
                              messagebox.showerror("Inventory Error", f"Failed to update inventory: {e}")


          def rec_notify(self):
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
