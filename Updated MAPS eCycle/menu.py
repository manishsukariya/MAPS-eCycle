import customtkinter as ctk

class Menu:
    def __init__(self, app):
        self.app = app
        self.menu_width = 250
        self.current_x = -self.menu_width
        self.menu_bar = False
        self.menu_frame = None
        self.menu_list = None


    def create_menu_frame(self):
        if self.menu_frame is None or not self.menu_frame.winfo_exists():
            self.menu_frame = ctk.CTkFrame(self.app.main_frame, width=self.menu_width, border_color="Black", fg_color="#0F172A", corner_radius=0)    #0EA5E9


    def menu_flag(self, items=None, type=None):
        self.create_menu_frame()
        if not self.menu_bar:
            if items and type:
                self.menu_list = items
                self.type = type
            self.menu_frame.place(x=self.current_x, y=0, relheight=1)
            self.exp_menu()
        else:
            self.col_menu()

    def menu_action(self, n, type):
        if type == "seller":
            self.seller_menu_action(n)
        elif type == "buyer":
            self.buyer_menu_action(n)
        elif type == "inspector":
            self.inspector_menu_action(n)
        elif type == "recycler":
            self.recycler_menu_action(n)
        elif type == "delivery":
            self.delivery_menu_action(n)
        else:
            self.admin_menu_action(n)


    def seller_menu_action(self, n):
        if n == "Dashboard":
            self.better_anim(self.app.se.seller_screen)
        elif n == "Sell":
            self.better_anim(self.app.se.seller_sell_screen)
        elif n == "Status":
            self.better_anim(self.app.se.seller_status_screen)
        elif n == "History":
            self.better_anim(self.app.se.seller_history_screen)
        elif n == "Negociations":
            self.better_anim(self.app.se.seller_nego_screen)
        elif n == "Direct B to S":
            self.better_anim(self.app.se.seller_b_to_s_screen)
        elif n == "Feedback":
            self.better_anim(self.app.se.seller_feedback_screen)
        elif n == "Report":
            self.better_anim(self.app.se.seller_report_screen)

        
    def buyer_menu_action(self, n):
        if n == "Shop":
            self.better_anim(self.app.be.buyer_shop_screen)
        elif n == "Status":
            self.better_anim(self.app.be.buyer_status_screen)
        elif n == "History":
            self.better_anim(self.app.be.buyer_history_screen)
        elif n == "Direct S to B":
            self.better_anim(self.app.be.buyer_s_to_b_screen)
        elif n == "Cart":
            self.better_anim(self.app.be.buyer_cart_screen)
        elif n == "Payment":
            self.better_anim(self.app.be.buyer_pay_screen)
        elif n == "Wishlist":
            self.better_anim(self.app.be.buyer_wishlist_screen)
        elif n == "Feedback":
            self.better_anim(self.app.be.buyer_fb_screen)
        elif n == "Report":
            self.better_anim(self.app.be.buyer_report_screen)

    def admin_menu_action(self, n):
        if n =="Dashboard":
            self.better_anim(self.app.ad.admin_screen)
        elif n == "Users":
            self.better_anim(self.app.ad.admin_users_screen)
        elif n == "Inventory":
            self.better_anim(self.app.ad.admin_inventory_screen)
        elif n == "All Inspection":
            self.better_anim(self.app.ad.admin_all_inspection_screen)
        elif n == "Pending Payments":
            self.better_anim(self.app.ad.admin_pending_payments_screen)
        elif n == "Pending Pickups":
            self.better_anim(self.app.ad.admin_pending_pickups_screen)
        elif n == "Pending Deliveries":
            self.better_anim(self.app.ad.admin_pending_deliveries_screen)
        elif n == "Negotiation":
            self.better_anim(self.app.ad.admin_negotiation_screen)
        elif n == "Feedbacks":
            self.better_anim(self.app.ad.admin_feedback_screen)
        elif n == "Reports":
            self.better_anim(self.app.ad.admin_reports_screen)
        elif n == "Products For Repair":
            self.better_anim(self.app.ad.admin_products_for_repair_screen)

    def inspector_menu_action(self, n):
        if n == "Inspections":
            self.better_anim(self.app.ins.inspection_screen)

    def recycler_menu_action(self, n):
        if n == "recycling":
            self.better_anim(self.app.re.recycler_screen)

    def delivery_menu_action(self, n):
        if n == "Deliveries":
            self.better_anim(self.app.de.delivery_screen)
        elif n == "Pick Ups":
            self.better_anim(self.app.de.pickup_screen)
        elif n == "Buyer to Seller":
            self.better_anim(self.app.de.direct_delivery_screen)


    def update_menu(self, list_m):
        self.check_menu_frame()
        self.clear_menu_frame()

        ctk.CTkLabel(self.menu_frame, text="MENU", font=("Arial", 40, "bold"), text_color="#E2E8F0").place(relx=0.3, rely=0.05, anchor="center")
        ctk.CTkFrame(self.menu_frame, fg_color="#2563EB", height=2).place(relx=0.495, rely=0.09, relwidth=1, anchor="center")
        ctk.CTkFrame(self.menu_frame, fg_color="#2563EB", width=4).place(relx=1.0, rely=0.5, relheight=1, anchor="center")
        
        close_btn = ctk.CTkButton(self.menu_frame, text="X", width=30, height=30,
                                fg_color="#EF4444", text_color="white",
                                hover_color="#DC2626",
                                command=lambda: self.menu_flag())
        close_btn.place(x=200, y=10)

        for i, name in enumerate(list_m, start=1):
            self.btn = ctk.CTkButton(self.menu_frame, text=name, width=200, height=40,
                                fg_color="#0F172A", text_color="#F0F9FF", anchor="w",
                                hover_color="#2563EB", command=lambda n=name: self.menu_action(n, self.type))
            self.btn.place(x=10, y=60 + (i * 50))


    def exp_menu(self):
        self.app.mg.send_to_back(self.menu_frame)
        if self.current_x < 0:
            self.current_x += 10
            self.menu_frame.place(x=self.current_x, y=0)
            self.app.after(5, self.exp_menu)
        else:
            self.current_x = 0
            self.menu_bar = True
            if self.menu_list:
                self.update_menu(self.menu_list)
            self.menu_frame.lift()

    def col_menu(self):
        if self.current_x > -self.menu_width:
            self.current_x -= 10
            self.menu_frame.place(x=self.current_x, y=0)
            self.app.after(5, self.col_menu)
        else:
            self.current_x = -self.menu_width
            self.menu_bar = False
            self.menu_frame.place_forget()
            self.clear_menu_frame()
            self.app.mg.bring_to_front()
            
    def check_menu_before_action(self, event=None):
        if not self.menu_bar:
            return
        widget = event.widget
        while widget:
            if widget == self.menu_frame:
                return
            try:
                widget = widget.master
            except AttributeError:
                break
        self.menu_flag()
        return "break"
    
    def better_anim(self, callback):
        self.app.clear_content()
        self.target_callback = callback
        self.close_menu_with_callback()

    def close_menu_with_callback(self):
        if self.current_x > -self.menu_width:
            self.current_x -= 10
            self.menu_frame.place(x=self.current_x, y=0)
            self.app.after(5, self.close_menu_with_callback)
        else:
            self.current_x = -self.menu_width
            self.menu_bar = False
            self.menu_frame.place_forget()
            self.clear_menu_frame()
            self.app.mg.bring_to_front()
            if hasattr(self, "target_callback") and self.target_callback:
                cb = self.target_callback
                self.target_callback = None
                self.app.after(10, cb)


    def check_menu_frame(self):
        try:
            self.menu_frame.winfo_children()
        except:
            self.menu_frame = self.create_menu_frame()

    def clear_menu_frame(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()