import customtkinter as ctk
from gui.image_converter_window import open_image_converter_window
from gui.image_compressor_window import open_image_compressor_window

from gui.pdf_merger_window import open_pdf_merger_window
from gui.pdf_compressor_window import open_pdf_compressor_window

from gui.yt_downloader_window import open_yt_downloader_window
from gui.video_to_mp3_window import open_video_to_mp3_window
from gui.video_compressor_window import open_video_compressor_window

def run_app():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Utility Tools")
    
    root.geometry("850x550") 
    root.resizable(True, True)
    
    # PREVENT DUPLICATE WINDOW
    active_windows = {}
    def open_unique_window(window_key, open_function):
        win = active_windows.get(window_key)
        if win is not None:
            try:
                if win.winfo_exists():
                    win.deiconify()
                    win.lift()
                    win.focus_force()
                    return
            except Exception:
                pass
            active_windows.pop(window_key, None)

        before = set(root.winfo_children())
        result = open_function(root)

        if result is None:
            new_windows = [w for w in root.winfo_children()
                        if w not in before and isinstance(w, ctk.CTkToplevel)]
            result = new_windows[-1] if new_windows else None

        active_windows[window_key] = result

        if result is not None:
            result.bind(
                "<Destroy>",
                lambda e, k=window_key, w=result:
                    active_windows.pop(k, None) if e.widget is w else None
            )
        
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
                                 command=lambda: open_unique_window("image_conv", open_image_converter_window))
    btn_img_conv.pack(fill="x", padx=15, pady=5)

    btn_img_comp = ctk.CTkButton(card_image, text="Image Compressor", height=40, font=ctk.CTkFont(weight="bold"), 
                                 command=lambda: open_unique_window("image_comp", open_image_compressor_window))
    btn_img_comp.pack(fill="x", padx=15, pady=5)


    # PDF TOOLS
    card_pdf = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_pdf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    card_pdf.grid_propagate(False)
    
    ctk.CTkLabel(card_pdf, text="📄 PDF", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_pdf_merger = ctk.CTkButton(card_pdf, text="PDF Merger", height=40, font=ctk.CTkFont(weight="bold"), 
                                   command=lambda: open_unique_window("pdf_merger", open_pdf_merger_window))
    btn_pdf_merger.pack(fill="x", padx=15, pady=5)

    btn_pdf_comp = ctk.CTkButton(card_pdf, text="PDF Compressor", height=40, font=ctk.CTkFont(weight="bold"), 
                                 command=lambda: open_unique_window("pdf_comp", open_pdf_compressor_window))
    btn_pdf_comp.pack(fill="x", padx=15, pady=5)



    # TOOLS IN BOTTOM ONLY IN RELEASE VERSION
    
    
    
    # DOWNLOADER TOOLS
    card_dl = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_dl.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    card_dl.grid_propagate(False)
    
    ctk.CTkLabel(card_dl, text="🌐 Downloader", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_yt_dl = ctk.CTkButton(card_dl, text="YT Downloader", height=40, font=ctk.CTkFont(weight="bold"), 
                              fg_color="#c0392b", hover_color="#e74c3c", 
                              command=lambda: open_unique_window("yt_dl", open_yt_downloader_window))
    btn_yt_dl.pack(fill="x", padx=15, pady=5)

    
    # VIDEO TOOLS
    card_video = ctk.CTkFrame(main_frame, corner_radius=15, width=240)
    card_video.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    card_video.grid_propagate(False)
    
    ctk.CTkLabel(card_video, text="🎬 Video", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
    
    btn_video_mp3 = ctk.CTkButton(card_video, text="Video to MP3", height=40, font=ctk.CTkFont(weight="bold"),
                                  command=lambda: open_unique_window("video_mp3", open_video_to_mp3_window))
    btn_video_mp3.pack(fill="x", padx=15, pady=5)
    
    btn_video_compressor = ctk.CTkButton(card_video, text="Video Compressor", height=40, font=ctk.CTkFont(weight="bold"),
                                     command=lambda: open_unique_window("video_comp", open_video_compressor_window))
    btn_video_compressor.pack(fill="x", padx=15, pady=5)

    root.mainloop()