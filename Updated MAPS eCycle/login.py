import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import re

class Login:
          def __init__(self, app):
                    self.app = app
                    self.main_frame = self.app.main_frame

          def check_l_details(self):
                    l_name = self.username_entry.get().strip().lower()
                    l_pass = self.password_entry.get().strip()
                    l_email = self.l_email_entry.get().strip().lower()
                    l_type = self.user_type_entry.get().strip()
                    

                    if not l_name or not l_pass or not l_email or not l_type:
                              messagebox.showerror("ERROR", "All Fields Are Required!!!")

                    elif not re.match(r"^[a-zA-Z]+(?: [a-zA-Z]+)*$", l_name):  
                              messagebox.showerror("Invalid Name", "Provide a valid name (letters only)")

                    elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", l_email):  
                              messagebox.showerror("Invalid Email", "Provide a valid email ID")

                    elif not re.match(r"^[a-zA-Z]+$", l_type):  
                              messagebox.showerror("Wrong Type", "Provide a valid type (letters only)")

                    else:                  
                              role = l_type.lower()
                              user_data = self.app.db.check_user(role, l_name, l_pass, l_email)

                              if user_data == "S":
                                        messagebox.showinfo("Success", "Successfully Logged IN")
                                        self.app.p_mail = l_email
                                        self.app.p_name = l_name

                                        if role == "buyer":
                                                  self.app.be.buyer_shop_screen()
                                                  
                                        elif role == "seller":
                                                  self.app.se.seller_screen()
                              else:
                                        messagebox.showerror("Login Failed", "Invalid Username, Email, or Password!")



          def form_l(self):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    self.types = ["Buyer", "Seller"]

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                    self.frame = ctk.CTkFrame(self.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                    self.frame.place(relx=0.5, rely=0.5, anchor="center")


                    title_label = ctk.CTkLabel(self.frame, text="LOGIN", font=("Impact", 40, "bold"), text_color="black")
                    title_label.place(relx=0.5, rely=0.1, anchor="center")

                    self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your username", width=280)
                    self.username_entry.place(relx=0.5, rely=0.2, anchor="center")

                    self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your password", width=280, show="*")
                    self.password_entry.place(relx=0.5, rely=0.3, anchor="center")

                    self.l_email_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your email", width=280)
                    self.l_email_entry.place(relx=0.5, rely=0.4, anchor="center")

                    self.user_type_entry = ctk.CTkOptionMenu(self.frame, values = self.types, width=280)
                    self.user_type_entry.place(relx=0.5, rely=0.5, anchor="center")

                    login_button = ctk.CTkButton(self.frame, text="LOGIN", width=200, fg_color="black", text_color="white", hover_color="gray", border_width=2, command=self.check_l_details)
                    login_button.place(relx=0.5, rely=0.6, anchor="center")

                    reset_button = ctk.CTkButton(self.frame, text="RESET PASSWORD", width=200, fg_color="gray", text_color="black", hover_color="darkgray", border_width=2, command=self.reset_password)
                    reset_button.place(relx=0.5, rely=0.7, anchor="center")

                    not_registered_label = ctk.CTkLabel(self.frame, text="Not Registered Yet?", font=("Arial", 14), text_color="black")
                    not_registered_label.place(relx=0.5, rely=0.85, anchor="center")

                    register_button = ctk.CTkLabel(self.frame, text="Register", font=("Arial", 14, "underline"),text_color="blue", cursor="hand2")
                    register_button.place(relx=0.5, rely=0.9, anchor="center")

                    back_button = ctk.CTkLabel(self.frame, text="Back", font=("Arial", 14, "underline"), text_color="blue", cursor="hand2")
                    back_button.place(relx=0.9, rely=0.95, anchor="center")

                    register_button.bind("<Button-1>", lambda e: self.app.rol.role_user())
                    back_button.bind("<Button-1>", lambda e: self.app.rol.role_screen())

          def change_password(self):
                    c_name = self.user_name_entry.get().strip().lower()
                    o_pass = self.old_password_entry.get().strip()
                    n_pass = self.new_password_entry.get().strip()
                    c_email = self.re_email_entry.get().strip().lower()
                    u_type = self.user_type_entry.get().strip().lower()

                    if not c_name or not o_pass or not n_pass:
                              messagebox.showerror("ERROR","All Fields Are Required!!!")

                    elif not re.match(r".{6,}$", n_pass):
                              messagebox.showerror("Password","Minimum Characters Are Required!!!")

                    elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", c_email):
                              messagebox.showerror("Invalid Email", "Provide a valid email ID")

                    elif o_pass == n_pass:
                              messagebox.showerror("Same Passwords", "Both The Passwords Are Same!!!")

                    else:
                              messagebox.showinfo("Success", "Successfully Logged IN")
                              

                              '''if u_type == "buyer":
                                        role = "buyer"
                                        self.db.check_pass(role, n_pass, c_name, c_email, o_pass)

                              elif u_type == "seller":
                                        role = "seller"
                                        self.db.check_pass(role, n_pass, c_name, c_email, o_pass)
'''
            

          def reset_password(self):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.07, anchor="center")

                    self.frame = ctk.CTkFrame(self.main_frame, height=600, width=500, fg_color="#A8F1FE", corner_radius=20)
                    self.frame.place(relx=0.5, rely=0.5, anchor="center")

                    title_label = ctk.CTkLabel(self.frame, text="RESET PASSWORD", font=("Impact", 40, "bold"), text_color="black")
                    title_label.place(relx=0.5, rely=0.1, anchor="center")

                    self.user_name_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Username", width=280)
                    self.user_name_entry.place(relx=0.5, rely=0.2, anchor="center")

                    self.re_email_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your email", width=280)
                    self.re_email_entry.place(relx=0.5, rely=0.3, anchor="center")

                    self.old_password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your old password", width=280, show="*")
                    self.old_password_entry.place(relx=0.5, rely=0.4, anchor="center")

                    self.new_password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your new password", width=280, show="*")
                    self.new_password_entry.place(relx=0.5, rely=0.5, anchor="center")

                    self.user_type_entry = ctk.CTkOptionMenu(self.frame, values = self.types, width=280)
                    self.user_type_entry.place(relx=0.5, rely=0.6, anchor="center")

                    self.confirm_button = ctk.CTkButton(self.frame, text="CONFIRM PASSWORD", width=200, fg_color="gray", text_color="black", hover_color="darkgray", border_width=2, command=self.change_password)
                    self.confirm_button.place(relx=0.5, rely=0.75, anchor="center")

                    self.back_label = ctk.CTkLabel(self.frame, text="Back To Login", font=("Arial", 14 , "underline"), text_color="blue")
                    self.back_label.place(relx=0.5, rely=0.9, anchor="center")
                    
                    self.back_label.bind("<Button-1>", lambda e: self.form_l())
                    

