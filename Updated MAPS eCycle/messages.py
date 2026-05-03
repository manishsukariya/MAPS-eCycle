import tkinter as tk
import customtkinter as ctk

class Messages:
    def __init__(self, app):
        self.app = app
        self.text_ids = []
        self.positions = []
        self.scroll_speed = 3
        self.scroll_active = False
        self.msg_frame = None
        self.canvas = None
        self.is_scroll = None
        self.line_height = 50

    def create_msg_frame(self, msgs):
        self.stop_scroll()
        if self.msg_frame:
            self.msg_frame.destroy()

        self.msg_frame = ctk.CTkFrame(self.app.main_frame, width=280, fg_color="#E4E7EB", corner_radius=10)
        self.msg_frame.place(relx=0.01, y=100, relheight=0.86)

        ctk.CTkLabel(self.msg_frame, text="Notifications", font=("Arial", 24, "bold"), text_color="black", ).place(relx=0.3, rely=0.05, anchor="center")

        self.canvas = tk.Canvas(self.msg_frame, width=320, bg="#E4E7EB", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.53, relheight=0.9, anchor="center")

        self.msgs = msgs
        self.show_messages()

    def show_messages(self):
        if not self.canvas:
            return

        self.canvas.delete("all")
        self.text_ids.clear()
        self.positions.clear()

        y = 40
        for msg in self.msgs:
            text_id = self.canvas.create_text(140, y, text=msg, font=("Arial", 16), fill="#FF0000", width=260, justify="center")
            self.text_ids.append(text_id)
            self.positions.append(y)
            y += self.line_height

        self.scroll_active = True
        self.animate_scroll()

    def animate_scroll(self):
        if not self.canvas or not self.canvas.winfo_exists():
            return

        
        x_space = 40

        for i in range(len(self.positions)):
            self.positions[i] -= self.scroll_speed
            if self.positions[i] < -20:
                self.positions[i] = max(self.positions) + self.line_height + x_space
                
            self.canvas.coords(self.text_ids[i], 160, self.positions[i])

        self.is_scroll = self.app.after(30, self.animate_scroll)

    def stop_scroll(self):
        self.scroll_active = False
        if self.is_scroll:
                  self.app.after_cancel(self.is_scroll)
                  self.is_scroll = None

    def send_to_back(self, menu_frame):
          if self.msg_frame and self.msg_frame.winfo_exists() and menu_frame and menu_frame.winfo_exists():
                    self.msg_frame.lower(menu_frame)


    def bring_to_front(self):
          if self.msg_frame and self.msg_frame.winfo_exists():
                    self.msg_frame.lift()
