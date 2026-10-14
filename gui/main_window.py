import customtkinter as ctk
from tkinter import messagebox
from gui.image_window import open_image_window

def open_pdf_merger():
    messagebox.showinfo("Info", "Fitur PDF akan segera hadir!")

def run_app():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Utility Tools")
    root.geometry("400x350")
    root.resizable(False, False)
        
        
    # ================= UI ELEMENTS =================
    
    label_judul = ctk.CTkLabel(root, text="🛠️ Utility Tools", font=ctk.CTkFont(size=24, weight="bold"))
    label_judul.pack(pady=(30, 10))
    
    label_sub = ctk.CTkLabel(root, text="Pilih alat yang ingin Anda gunakan:", text_color="gray")
    label_sub.pack(pady=(0, 20))
    
    frame_tombol = ctk.CTkFrame(root, fg_color="transparent")
    frame_tombol.pack(pady=10, padx=40, fill="both", expand=True)
    
    # Button
    btn_img = ctk.CTkButton(frame_tombol, text="🎨 Image Converter", height=45,
                            font=ctk.CTkFont(size=14, weight="bold"),
                            command=lambda: open_image_window(root))
    btn_img.pack(pady=10, fill="x")
    
    btn_pdf = ctk.CTkButton(frame_tombol, text="📄 PDF Merger (Segera)", height=45, 
                            font=ctk.CTkFont(size=14, weight="bold"),
                            fg_color="gray", command=open_pdf_merger)
                            
    btn_pdf.pack(pady=10, fill="x")
    
    root.mainloop()