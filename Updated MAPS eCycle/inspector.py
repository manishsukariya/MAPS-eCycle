import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json
import os


class Inspector:
          def __init__(self, app):
                  self.app = app


          def valid_inspect(self):
                    inspect_code = self.inspect_pass_entry.get().strip()

                    valid_ins = ["a"]
                    if inspect_code in valid_ins:
                              messagebox.showinfo("Success", "Successfully Logged In!")

                              self.inspection_screen()
          
                    else:
                              messagebox.showerror("Invalid", "Invalid Admin Code!")

          def inspect_login(self):
                self.app.remove_head_content()
                self.app.clear_frame()

                img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                ctk.CTkLabel(self.app.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                self.frame = ctk.CTkFrame(self.app.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                self.frame.place(relx=0.5, rely=0.5, anchor="center")

                admin_label = ctk.CTkLabel(self.frame, text="Inspectors", font=("Impact", 50), width=200, text_color="black")
                admin_label.place(relx=0.5, rely=0.1, anchor="center")

                admin_login_label = ctk.CTkLabel(self.frame, text="Login", font=("Impact", 50), width=380, text_color="black")
                admin_login_label.place(relx=0.5, rely=0.2, anchor="center")

                self.inspect_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Name", width=380)
                self.inspect_entry.place(relx=0.5, rely=0.4, anchor="center")

                self.inspect_pass_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Inspector login password", width=380)
                self.inspect_pass_entry.place(relx=0.5, rely=0.5, anchor="center")

                login_button = ctk.CTkButton(self.frame, text="LOGIN", width=200, fg_color="black", text_color="white", border_width=2, border_color="grey", command=self.valid_inspect)
                login_button.place(relx=0.5, rely=0.7, anchor="center")

                back_l = ctk.CTkLabel(self.frame, text="Back", font=("Arial", 14), text_color="blue")
                back_l.place(relx=0.5, rely=0.8, anchor="center")

                back_l.bind("<Button-1>", lambda e: self.app.rol.role_screen())


          def inspection_screen(self):
                    self.app.clear_frame()
                    if self.app.content_frame:
                              self.app.clear_content()
                    self.app.head_content_create("operator")


                    self.list_m = [
                               "Inspections"
                    ]

                    self.app.me.menu_flag(self.list_m, "inspector")

                    ctk.CTkLabel(self.app.content_frame, text="Inspections", font=("Impact", 60), text_color="Black").place(relx=0.5, rely=0.08, anchor="center")

                    self.reqs_frame = ctk.CTkScrollableFrame(self.app.content_frame, fg_color="#E4E7EB")
                    self.reqs_frame.place(relx=0.5, rely=0.55, relheight=0.8, relwidth=0.9, anchor="center")


                    query = "select * from product where status='pending'"
                    self.app.db.cursor.execute(query)
                    requests = self.app.db.cursor.fetchall()
                    
                    for i, product in enumerate(requests):
                            row=i
                            col=0

                            product_id, seller_id, product_type, brand, model, condition, price, quantity, pickup_location, image_paths, status, upload_date = product

                            req_frame = ctk.CTkFrame(self.reqs_frame, fg_color="white", height=150, width=900)
                            req_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

                            imgs_path = json.loads(image_paths)[0] if image_paths else "default.png"
                            img = ctk.CTkImage(light_image=Image.open(imgs_path), size=(100, 100))
                            ctk.CTkLabel(req_frame, image=img, text="").place(relx=0.1, rely=0.5, anchor="center")


                            ctk.CTkLabel(req_frame, text=f"{brand} {model}", font=("Impact", 24), text_color="black").place(relx=0.2, rely=0.08)
                            ctk.CTkLabel(req_frame, text=f"Type: {product_type}", font=("Arial", 16), text_color="black").place(relx=0.25, rely=0.3)
                            ctk.CTkLabel(req_frame, text=f"Condition: {condition}", font=("Arial", 16), text_color="black").place(relx=0.25, rely=0.5)
                            ctk.CTkLabel(req_frame, text=f"Price: ₹{price}", font=("Arial", 16), text_color="green").place(relx=0.25, rely=0.7)

                            view_btn = ctk.CTkButton(req_frame, text="View Details", command=lambda p=product: self.inspection_view(p))
                            view_btn.place(relx=0.85, rely=0.5, anchor="center")




                    self.insp_notify()

          def inspection_view(self, product):
                        self.app.clear_content()

                        product_id, seller_id, product_type, brand, model, condition, price, quantity, pickup_location, image_paths, status, upload_date = product

                        ctk.CTkLabel(self.app.content_frame, text=f"Inspect {product_type}", font=("Impact", 45), text_color="black").place(relx=0.5, rely=0.1, anchor="center")
                    
                        imgs = json.loads(image_paths) if image_paths else []
                        thumb_path = imgs[0] if imgs else "assets/no_image.png"
                        thumb_img = ctk.CTkImage(light_image=Image.open(thumb_path), size=(180, 180))
                        ctk.CTkLabel(self.app.content_frame, image=thumb_img, text="").place(relx=0.25, rely=0.3, anchor="center")

                        y_offset = 0.6
                        for path in imgs:
                              name = os.path.basename(path)
                              def open_preview(p=path):
                                    img_win = ctk.CTkToplevel(self.app)
                                    img = ctk.CTkImage(light_image=Image.open(p), size=(400, 400))
                                    ctk.CTkLabel(img_win, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")
                              ctk.CTkButton(self.app.content_frame, text=name, width=160, command=open_preview).place(relx=0.23, rely=y_offset, anchor="center")
                              y_offset += 0.07

                        details = (
                        f"Type: {product_type}\n"
                        f"Brand: {brand}\n"
                        f"Model: {model}\n"
                        f"Seller Price: ₹{price}\n"
                        f"Qty: {quantity}\n"
                        f"Seller Condition: {condition}\n"
                        f"Pickup: {pickup_location}"
                        )
                        ctk.CTkLabel(self.app.content_frame, text=details, font=("Arial", 20), text_color="black", justify="left", wraplength=400).place(relx=0.6, rely=0.3, anchor="center")

                        ctk.CTkLabel(self.app.content_frame, text="Suggest Price", font=("Arial", 20), text_color="black").place(relx=0.5, rely=0.55, anchor="center")
                        price_entry = ctk.CTkEntry(self.app.content_frame, placeholder_text="Enter a Suggested Price", width=180)
                        price_entry.place(relx=0.5, rely=0.59, anchor="center")

                        ctk.CTkLabel(self.app.content_frame, text="Select Condition", font=("Arial", 20), text_color="black").place(relx=0.5, rely=0.65, anchor="center")
                        cond_box = ctk.CTkComboBox(self.app.content_frame, values=["Poor", "Moderate", "Good"], width=180)
                        cond_box.place(relx=0.5, rely=0.69, anchor="center")

                        def approve():
                              sug_price = price_entry.get()
                              cond = cond_box.get()
                              if not sug_price or not cond:
                                    return messagebox.showerror("Required", "Provide Suggestions!!!")
                              self.app.fm.save_inspection_data(product_id, sug_price, cond)
                              self.app.db.cursor.execute(
                                    "UPDATE product SET status='approved' WHERE product_id=%s", (product_id,)
                              )
                              self.app.db.db.commit()
                              self.app.db.cursor.nextset()
                              self.app.db.cursor.execute("INSERT INTO pickup (product_id, seller_id, pickup_address, pickup_date, status) VALUES (%s, %s, %s, now(), 'Scheduled')", (product_id, seller_id, pickup_location))
                              self.app.db.db.commit()
                              self.inspection_screen()

                        def reject():
                                    self.app.db.cursor.execute(
                                          "UPDATE product SET status='rejected' WHERE product_id=%s", (product_id,)
                                    )

                                    self.app.db.db.commit()
                                    print(product_id, seller_id, pickup_location)
                                    
                                    
                                    print("done")

                                    self.inspection_screen()

                        ctk.CTkButton(self.app.content_frame, text="Approve", fg_color="green", command=approve).place(relx=0.4, rely=0.85)
                        ctk.CTkButton(self.app.content_frame, text="Reject", fg_color="red", command=reject).place(relx=0.6, rely=0.85)


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

