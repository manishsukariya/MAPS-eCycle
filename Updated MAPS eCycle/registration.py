import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import re

class Registration:
          def __init__(self, app):
                    self.app = app
                    self.frame = app.main_frame

          def check_r_details(self):
                    r_name = self.name_entry.get().strip().lower()
                    r_phone = self.phone_entry.get().strip()
                    r_email = self.r_email_entry.get().strip().lower()
                    r_addr = self.address_entry.get().strip().lower()
                    r_pass = self.password_entry.get().strip()
                    r_repass = self.re_password_entry.get().strip()
                    
                    

                    if not r_name or not r_phone or not r_email or not r_addr or not r_pass or not r_repass:
                              messagebox.showerror("ERROR","All Fields Are Required!!!")

                    elif not re.match(r"^[a-zA-Z\s]+$", r_name):
                              messagebox.showerror("Valid Name", "Provide Valid Name")

                    elif not re.match(r"^[9876]\d{9}$", r_phone):
                              messagebox.showerror("Valid Number", "Provide Valid Phone No.")

                    elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", r_email):
                              messagebox.showerror("Valid Email", "Provide EmailID")

                    elif r_pass != r_repass:
                              messagebox.showerror("Password","Password Does Not Match")

                    elif not re.match(r".{6,}$", r_pass):
                              messagebox.showerror("Password","Minimum Characters Are Required!!!")

                    else:
                              if self.role == "buyer":
                                        role = "buyer"
                                        new_user1 = self.app.db.new_user(role, r_name, r_phone, r_email, r_addr, r_pass)

                                        if new_user1 == "S":
                                                  messagebox.showinfo("Success", "Registration Successful")
                                                  self.app.p_mail = r_email
                                                  self.app.p_name = r_name

                                                  self.app.be.buyer_shop_screen()

                                        else:
                                                  messagebox.showerror("Error", "Phone or Email used once!!!")

                              
                              elif self.role == "seller":
                                        role = "seller"
                                        new_user2 = self.app.db.new_user(role, r_name, r_phone, r_email, r_addr, r_pass)

                                        if new_user2 == "S":
                                                  messagebox.showinfo("success", "Registered !!!")
                                                  self.app.p_mail = r_email
                                                  self.app.p_name = r_name
                                                  
                                                  self.app.se.seller_screen()

                                        else:
                                                  messagebox.showerror("Error", "Registration Failed")


                              else:
                                        messagebox.showerror("ERROR","Invalid Role!!!")


    


          def form_r(self, role):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    self.role = role

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                    self.form_frame = ctk.CTkFrame(self.frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                    self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

                    role_label = ctk.CTkLabel(self.form_frame, text=f"REGISTER AS {role.upper()}", font=("Impact", 40, "bold"), text_color="black")
                    role_label.place(relx=0.5, rely=0.1, anchor="center")

                    self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter your name", width=280)
                    self.name_entry.place(relx=0.5, rely=0.23, anchor="center")

                    self.phone_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter phone number", width=280)
                    self.phone_entry.place(relx=0.5, rely=0.32, anchor="center")

                    self.r_email_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter email", width=280)
                    self.r_email_entry.place(relx=0.5, rely=0.41, anchor="center")

                    self.address_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter address", width=280)
                    self.address_entry.place(relx=0.5, rely=0.50, anchor="center")

                    self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Create password", width=280, show="*")
                    self.password_entry.place(relx=0.5, rely=0.59, anchor="center")

                    self.re_password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Re-enter password", width=280, show="*")
                    self.re_password_entry.place(relx=0.5, rely=0.68, anchor="center")

                    submit_button = ctk.CTkButton(self.form_frame, text="SUBMIT", width=200, fg_color="black", text_color="white", border_width=2, border_color="grey", command=self.check_r_details)
                    submit_button.place(relx=0.5, rely=0.8, anchor="center")

                    already_registered_label = ctk.CTkLabel(self.form_frame, text="Already Registered?", font=("Arial", 14), text_color="black")
                    already_registered_label.place(relx=0.5, rely=0.9, anchor="center")

                    login_button = ctk.CTkLabel(self.form_frame, text="Login", font=("Arial", 14, "underline"), text_color="blue", cursor="hand2")
                    login_button.place(relx=0.5, rely=0.95, anchor="center")

                    back_button = ctk.CTkLabel(self.form_frame, text="Back", font=("Arial", 14, "underline"), text_color="blue", cursor="hand2")
                    back_button.place(relx=0.9, rely=0.95, anchor="center")

                    login_button.bind("<Button-1>", lambda e: self.app.log.form_l())
                    back_button.bind("<Button-1>", lambda e: self.app.rol.role_screen())
