import customtkinter as ctk
from PIL import Image
import tkinter as tk
from filemanager import *
from registration import *
from inspector import *
from recycler import *
from delivery import *
from database import *
from messages import *
from invoice import *
from login import *
from admin import *
from seller import *
from buyer import *
from role import *
from menu import *
from map import *

class Main(ctk.CTk):
        def __init__(self):
                super().__init__()
                self.geometry("1000x600")
                #self.resizable(True, True)
                self.title("MAPS eCycle")
                self.main_frame = ctk.CTkFrame(self, fg_color="#D8F7FF")
                self.main_frame.pack(fill="both", expand=True)
                self.head_frame = None
                self.content_frame = None
                self.all_files()
                self.bind_all("<Button-1>", self.me.check_menu_before_action, add="+")
                self.splash_screen()
                self.p_mail = None
                
        def all_files(self):
                self.fm = FileManager(os.getcwd())
                self.reg = Registration(self)
                self.ins = Inspector(self)
                self.rec = Recycler(self)
                self.de = Delivery(self)
                self.db = Database(self)
                self.mg = Messages(self)
                self.inv = InvoicePDF(self)
                self.log = Login(self)
                self.ad = Admin(self)
                self.se = Seller(self)
                self.be = Buyer(self)
                self.me = Menu(self)
                self.rol = Role(self)
                self.mp = Map(self)
              
        def splash_screen(self):
                self.remove_head_content()

                img_logo = ctk.CTkImage(light_image=Image.open("images/logo1.png"), size=(120, 120))
                ctk.CTkLabel(self.main_frame, image=img_logo, text="").place(relx=0.5, rely=0.25, anchor="center")
        
                ctk.CTkLabel(self.main_frame, text="Please Wait...", font=("Arial", 20, "italic"), text_color="navyblue").place(relx=0.5, rely=0.45, anchor="center")

                progress = ctk.CTkProgressBar(self.main_frame, width=300, mode="determinate", fg_color="gray", progress_color="limegreen")
                progress.place(relx=0.5, rely=0.5, anchor="center")
                progress.set(0)

                self.animate_loading(progress, 0)

        def animate_loading(self, progress, value):
                if value <= 100:
                        progress.set(value / 100)
                        self.after(30, self.animate_loading, progress, value + 1)
                else:
                        self.after(30, self.rol.role_screen)


        def create_head_frame(self, types):
                if not self.head_frame:
                        self.head_frame = ctk.CTkFrame(self.main_frame, height=90, corner_radius=0, fg_color="#0F172A")
                        self.head_frame.place(relx=0.5, rely=0, relwidth=1, anchor="n")

                        ctk.CTkFrame(self.head_frame, fg_color="white", height=2).place(relx=0.5, rely=0.99, relwidth=1, anchor="center")

                        self.menub = ctk.CTkButton(self.head_frame, text="☰", font=("Italic", 40, "bold"), height=50, width=50,
                                                text_color="#E2E8F0", fg_color="#0F172A", hover_color="#0F172A",
                                                bg_color="transparent", corner_radius=10,
                                                command=lambda: self.me.menu_flag())
                        self.menub.place(relx=0.03, rely=0.5, anchor="center")

                        img_logo = ctk.CTkImage(light_image=Image.open("images/logo2.png"), size=(80, 80))
                        ctk.CTkLabel(self.head_frame, image=img_logo, text="").place(relx=0.3, rely=0.5, anchor="center")
                        

                        ctk.CTkLabel(self.head_frame, text="M A P S   e C y c l e", text_color="#E2E8F0",
                                font=("Impact", 40, "bold"), bg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

                        
                        img_pro = ctk.CTkImage(light_image=Image.open("images/person.png"), size=(80, 80))
                        self.logout = ctk.CTkLabel(self.head_frame, image=img_pro, text="")
                        self.logout.place(relx=0.9, rely=0.5, anchor="center")
                        self.logout.bind("<Button-1>", lambda event: self.logout_profile(types))

                        
        def create_content_frame(self):
                if not self.content_frame:
                        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#E4E7EB")  #D8F7FF
                        self.content_frame.place(x=310, y=100, relwidth=0.79, relheight=0.86)

                
        def show_registration(self, role):
                self.reg.form_r(role)

        def head_content_create(self, type):
                self.create_head_frame(type)
                self.create_content_frame()

        def logout_profile(self, t):
                if t == "seller":
                        self.se.seller_profile()
                elif t == "buyer":
                        self.be.buyer_profile()
                else:
                        self.clear_content()

                        ctk.CTkLabel(self.content_frame, text="LOGOUT", text_color="black", font=("Arial", 40, "bold")).place(relx=0.5, rely=0.1, anchor="center")

                        ctk.CTkLabel(self.content_frame, text="Confirm to LOGOUT", text_color="red", font=("Arial", 40, "bold")).place(relx=0.5, rely=0.4, anchor="center")
                        
                        self.logout = ctk.CTkButton(self.content_frame, text="LOGOUT", fg_color="#EF4444", hover_color="#F87171",
                                                        text_color="#FFFFFF", font=("Poppins", 15),
                                                        height=50, width=150, corner_radius=10, command=self.rol.role_screen)
                        self.logout.place(relx=0.5, rely=0.55, anchor="center")

        def clear_frame(self):
              for widget in self.main_frame.winfo_children():
                        if widget not in (self.head_frame, self.me.menu_frame, self.content_frame, self.mg.msg_frame):
                                widget.destroy()  

        def clear_content(self):
                for widget in self.content_frame.winfo_children():
                        widget.destroy()

        def remove_head_content(self):
                if self.head_frame:
                        self.head_frame.destroy()
                        self.head_frame = None

                if  self.content_frame:
                        self.content_frame.destroy()
                        self.content_frame = None

                if self.mg.msg_frame:
                        self.mg.msg_frame.destroy()
                        self.mg.msg_frame = None        


if __name__ == "__main__":
        app = Main()
        app.mainloop() 