import customtkinter as ctk
from PIL import Image

class Role:
          def __init__(self, app):
                    self.app = app
                    self.main_frame = self.app.main_frame
                    

          def role_screen(self):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.1, anchor="center")

                    ctk.CTkLabel(self.main_frame, text="Register as Type", font=("Impact", 50), text_color="Black").place(relx=0.5, rely=0.2, anchor="center")
                    ctk.CTkLabel(self.main_frame, text="Choose Operator or User", font=("Arial", 30, "italic"), text_color="Black").place(relx=0.5, rely=0.3, anchor="center")


                    self.op_btn1 = ctk.CTkButton(self.main_frame, text="👨🏻‍💻 OPERATOR", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.role_operator)
                    self.op_btn1.place(relx=0.40, rely=0.5, anchor="center")

                    self.op_btn2 = ctk.CTkButton(self.main_frame, text="🙋🏻 USER", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.role_user)
                    self.op_btn2.place(relx=0.60, rely=0.5, anchor="center")

          def role_user(self):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.1, anchor="center")

                    ctk.CTkLabel(self.main_frame, text="Register as User", font=("Impact", 50), text_color="Black").place(relx=0.5, rely=0.2, anchor="center")
                    ctk.CTkLabel(self.main_frame, text="Choose Buyer or Seller", font=("Arial", 30, "italic"), text_color="Black").place(relx=0.5, rely=0.3, anchor="center")

                    self.op_btn3 = ctk.CTkButton(self.main_frame, text="🛒 BUYER", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = lambda : self.app.show_registration("buyer"))
                    self.op_btn3.place(relx=0.40, rely=0.5, anchor="center")

                    self.op_btn4 = ctk.CTkButton(self.main_frame, text="💰 SELLER", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = lambda : self.app.show_registration("seller"))
                    self.op_btn4.place(relx=0.60, rely=0.5, anchor="center")

          def role_operator(self):
                    self.app.remove_head_content()
                    self.app.clear_frame()

                    img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(80, 80))
                    ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.1, anchor="center")

                    ctk.CTkLabel(self.main_frame, text="Register as Operator", font=("Impact", 50), text_color="Black").place(relx=0.5, rely=0.2, anchor="center")
                    ctk.CTkLabel(self.main_frame, text="Choose Your Type", font=("Arial", 30, "italic"), text_color="Black").place(relx=0.5, rely=0.3, anchor="center")

                    self.op_btn5 = ctk.CTkButton(self.main_frame, text="🧑🏻‍💼 ADMIN", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.app.ad.admin_login)
                    self.op_btn5.place(relx=0.4, rely=0.4, anchor="center")

                    self.op_btn6 = ctk.CTkButton(self.main_frame, text="🕵🏻 INSPECTOR", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.app.ins.inspect_login)
                    self.op_btn6.place(relx=0.6, rely=0.4, anchor="center")

                    self.op_btn7 = ctk.CTkButton(self.main_frame, text="🧑🏻‍🔧 RECYCLER", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.app.rec.recycler_login)
                    self.op_btn7.place(relx=0.4, rely=0.6, anchor="center")

                    self.op_btn8 = ctk.CTkButton(self.main_frame, text="🚚 DELIVERY", text_color="Black", height=50, width=150, fg_color="White", border_width=1, border_color="Black", hover_color="#F5FCFF", command = self.app.de.delivery_login)
                    self.op_btn8.place(relx=0.6, rely=0.6, anchor="center")

