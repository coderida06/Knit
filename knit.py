import customtkinter as ctk
from datetime import datetime
import winsound
from PIL import Image
from knot3 import show_knot3
from knot4 import show_knot4
from knot5 import show_knot5
import subprocess
import sys


ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("1160x580")
app.configure(fg_color="#efcfe3")
app.title("knit")

app.after(100, lambda: app.wm_state("zoomed"))

PINK_COLOR = "#e27396"

def oppage():
    for widget in app.winfo_children():
        widget.destroy()

    
    # Left Side Flow
    ctk.CTkLabel(app, text="୨୧", font=("Arial", 32, "bold"), text_color=PINK_COLOR).place(x=80, y=80)
    ctk.CTkLabel(app, text="🧶", font=("Arial", 26), text_color=PINK_COLOR).place(x=180, y=160)
    ctk.CTkLabel(app, text="❀", font=("Arial", 28, "bold"), text_color=PINK_COLOR).place(x=100, y=280)
    ctk.CTkLabel(app, text="✦", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=220, y=380)
    ctk.CTkLabel(app, text="୨୧", font=("Arial", 32, "bold"), text_color=PINK_COLOR).place(x=120, y=490)

    # Right Side Flow
    ctk.CTkLabel(app, text="✦", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=1060, y=90)
    ctk.CTkLabel(app, text="୨୧", font=("Arial", 30, "bold"), text_color=PINK_COLOR).place(x=960, y=180)
    ctk.CTkLabel(app, text="🧶", font=("Arial", 28), text_color=PINK_COLOR).place(x=1040, y=290)
    ctk.CTkLabel(app, text="❀", font=("Arial", 26, "bold"), text_color=PINK_COLOR).place(x=930, y=410)
    ctk.CTkLabel(app, text="୨୧", font=("Arial", 32, "bold"), text_color=PINK_COLOR).place(x=1020, y=510)

    # Center Accents near selection buttons
    ctk.CTkLabel(app, text="✿", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=390, y=125)
    ctk.CTkLabel(app, text="✿", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=870, y=305)
    ctk.CTkLabel(app, text="✿", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=390, y=495)


    knot3 = ctk.CTkButton(
        app,
        text="🧶🧶🧶",                  
        width=400,                    
        height=80,                    
        corner_radius=40,             
        font=ctk.CTkFont(family="Arial Rounded MT Bold", size=32, weight="bold"), 
        fg_color="#8df1c6",          
        hover_color="#bef7df",        
        text_color="#e27396",         
        border_width=4,
        border_color="#bef7df",
        command=lambda: show_knot3(app, oppage)
    )
    knot3.place(x=450, y=100)
    
        
    k3 = ctk.CTkLabel(
        app,
        text="3 Knots",
        font=("times", 25),
        text_color="#985789"
    )
    k3.place(x=610, y=190)
    

    knot4 = ctk.CTkButton(
        app,
        text="🧶🧶🧶🧶",                  
        width=400,                    
        height=80,                    
        corner_radius=40,             
        font=ctk.CTkFont(family="Arial Rounded MT Bold", size=32, weight="bold"), 
        fg_color="#d9c5f5",          
        hover_color="#e4d6f8",        
        text_color="#ea9ab2",         
        border_width=4,
        border_color="#e4d6f8",
        command=lambda: show_knot4(app, oppage)
    )
    knot4.place(x=450, y=280)
    
            
    k4 = ctk.CTkLabel(
        app,
        text="4 Knots",
        font=("Times", 25),
        text_color="#985789"
    )
    k4.place(x=610, y=370)
    

    knot5 = ctk.CTkButton(
        app,
        text="🧶🧶🧶🧶🧶",                  
        width=400,                    
        height=80,                    
        corner_radius=40,             
        font=ctk.CTkFont(family="Arial Rounded MT Bold", size=32, weight="bold"), 
        fg_color="#b2e2eb",          
        hover_color="#e0f4f7",        
        text_color="#e27396",         
        border_width=4,
        border_color="#e0f4f7",
        command=lambda: show_knot5(app, oppage)
    )
    knot5.place(x=450, y=470)
    
            
    k5 = ctk.CTkLabel(
        app,
        text="5 Knots",
        font=("Times", 25),
        text_color="#985789"
    )
    k5.place(x=610, y=560)


# --- Main Menu Pink Scattered Decor ---

# Left Side Floating Pattern
ctk.CTkLabel(app, text="୨୧", font=("Arial", 34, "bold"), text_color=PINK_COLOR).place(x=80, y=50)
ctk.CTkLabel(app, text="✦", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=180, y=110)
ctk.CTkLabel(app, text="🧶", font=("Arial", 28), text_color=PINK_COLOR).place(x=120, y=210)
ctk.CTkLabel(app, text="❀", font=("Arial", 24, "bold"), text_color=PINK_COLOR).place(x=250, y=260)
ctk.CTkLabel(app, text="୨୧", font=("Arial", 30, "bold"), text_color=PINK_COLOR).place(x=90, y=360)
ctk.CTkLabel(app, text="✿", font=("Arial", 26, "bold"), text_color=PINK_COLOR).place(x=200, y=460)
ctk.CTkLabel(app, text="✦", font=("Arial", 24, "bold"), text_color=PINK_COLOR).place(x=60, y=520)

# Right Side Floating Pattern
ctk.CTkLabel(app, text="✦", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=1080, y=60)
ctk.CTkLabel(app, text="୨୧", font=("Arial", 32, "bold"), text_color=PINK_COLOR).place(x=980, y=120)
ctk.CTkLabel(app, text="❀", font=("Arial", 26, "bold"), text_color=PINK_COLOR).place(x=1060, y=240)
ctk.CTkLabel(app, text="🧶", font=("Arial", 30), text_color=PINK_COLOR).place(x=900, y=290)
ctk.CTkLabel(app, text="✿", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=1020, y=390)
ctk.CTkLabel(app, text="୨୧", font=("Arial", 36, "bold"), text_color=PINK_COLOR).place(x=930, y=490)
ctk.CTkLabel(app, text="✦", font=("Arial", 20, "bold"), text_color=PINK_COLOR).place(x=1080, y=530)

# Frame Around the Main Logo & Play Button
ctk.CTkLabel(app, text="୨୧", font=("Arial", 28, "bold"), text_color=PINK_COLOR).place(x=340, y=80)
ctk.CTkLabel(app, text="✿", font=("Arial", 20, "bold"), text_color=PINK_COLOR).place(x=910, y=80)
ctk.CTkLabel(app, text="🧶", font=("Arial", 24), text_color=PINK_COLOR).place(x=330, y=330)
ctk.CTkLabel(app, text="✦", font=("Arial", 22, "bold"), text_color=PINK_COLOR).place(x=920, y=330)

# Play Button Framing
ctk.CTkLabel(app, text="୨୧", font=("Arial", 28, "bold"), text_color=PINK_COLOR).place(x=490, y=420)
ctk.CTkLabel(app, text="୨୧", font=("Arial", 28, "bold"), text_color=PINK_COLOR).place(x=750, y=420)
ctk.CTkLabel(app, text="✦", font=("Arial", 18, "bold"), text_color=PINK_COLOR).place(x=630, y=495)


logo = ctk.CTkImage(
    light_image=Image.open("knitlogo.png"),
    dark_image=Image.open("knitlogo.png"),
    size=(500, 500)
)

logo_label = ctk.CTkLabel(
    app,
    image=logo,
    text=""
)

logo_label.place(x=395, y=50)

playbutton = ctk.CTkButton(
    app,
    text="Play",                  
    width=180,                    
    height=80,                    
    corner_radius=40,             
    font=ctk.CTkFont(family="Arial Rounded MT Bold", size=32, weight="bold"), 
    fg_color="#e27396",          
    hover_color="#ea9ab2",        
    text_color="#ffffff",         
    border_width=4,
    border_color="#f7b2bd",
    command=oppage
)

playbutton.place(x=550, y=400)

app.mainloop()
