import customtkinter as ctk
from gui.image_window import open_image_window
from gui.pdf_merger_window import open_pdf_merger_window
from gui.pdf_compressor_window import open_pdf_compressor_window
from gui.image_compressor_window import open_image_compressor_window
from gui.yt_downloader_window import open_yt_downloader_window

def run_app():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Utility Tools")
    
    root.geometry("850x550") 
    root.resizable(True, True)
        
    # HEADER
    label_judul = ctk.CTkLabel(root, text="🛠️ Utility Tools", font=ctk.CTkFont(size=26, weight="bold"))
    label_judul.pack(pady=(20, 5))
    
    label_sub = ctk.CTkLabel(root, text="Pilih kategori alat yang ingin Anda gunakan:", text_color="gray")
    label_sub.pack(pady=(0, 15))
    
    # CONTAINER
    main_frame = ctk.CTkScrollableFrame(root, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # IMAGE TOOLS
    card_image = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_image.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    card_image.grid_propagate(False)
    
    ctk.CTkLabel(card_image, text="🎨 Image", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_img_conv = ctk.CTkButton(card_image, text="Image Converter", height=40, font=ctk.CTkFont(weight="bold"),
                                 command=lambda: open_image_window(root))
    btn_img_conv.pack(fill="x", padx=15, pady=5)

    btn_img_comp = ctk.CTkButton(card_image, text="Image Compressor", height=40, font=ctk.CTkFont(weight="bold"), 
                                command=lambda: open_image_compressor_window(root)) 
    btn_img_comp.pack(fill="x", padx=15, pady=5)


    # PDF TOOLS
    card_pdf = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_pdf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    card_pdf.grid_propagate(False)
    
    ctk.CTkLabel(card_pdf, text="📄 PDF", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_pdf_merger = ctk.CTkButton(card_pdf, text="PDF Merger", height=40, font=ctk.CTkFont(weight="bold"),
                                   command=lambda: open_pdf_merger_window(root))
    btn_pdf_merger.pack(fill="x", padx=15, pady=5)

    btn_pdf_comp = ctk.CTkButton(card_pdf, text="PDF Compressor", height=40, font=ctk.CTkFont(weight="bold"),
                                 command=lambda: open_pdf_compressor_window(root))
    btn_pdf_comp.pack(fill="x", padx=15, pady=5)

    # only in release version
    # DOWNLOADER TOOLS
    card_dl = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_dl.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    card_dl.grid_propagate(False)
    
    ctk.CTkLabel(card_dl, text="🌐 Downloader", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_yt_dl = ctk.CTkButton(card_dl, text="YT Downloader", height=45, font=ctk.CTkFont(weight="bold"),
                            fg_color="#c0392b", hover_color="#e74c3c",
                            command=lambda: open_yt_downloader_window(root))
    btn_yt_dl.pack(fill="x", padx=20, pady=5)

    btn_ig_dl = ctk.CTkButton(card_dl, text="IG Downloader", height=40, font=ctk.CTkFont(weight="bold"),
                              fg_color="#5C6E7F", hover_color="#4C5B69")
    btn_ig_dl.pack(fill="x", padx=15, pady=5)

    root.mainloop()