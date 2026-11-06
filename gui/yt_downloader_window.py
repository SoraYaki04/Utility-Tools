import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from tools.yt_downloader import download_yt_process

def open_yt_downloader_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("YouTube Downloader")
    window.geometry("500x550") 
    window.resizable(False, False)
    window.grab_set()
    
    cancel_flag = [False]

    def update_quality_options(*args):
        if format_var.get() == "MP4 (Video)":
            label_quality.configure(text="Resolusi Video:")
            combo_quality.configure(values=["1080p", "720p", "480p", "360p"])
            quality_var.set("720p")
        else:
            label_quality.configure(text="Bitrate Audio:")
            combo_quality.configure(values=["320kbps", "256kbps", "192kbps", "128kbps"])
            quality_var.set("192kbps")

    def check_cancel():
        return cancel_flag[0]

    def cancel_download():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Membatalkan...")

    # Progess bar
    def update_progress_ui(percent_float, percent_str, speed_str, downloaded_mb, total_mb):
        progress_bar.set(percent_float)
        teks_status = f"Status: {percent_str} | {speed_str}\nProgress: {downloaded_mb:.2f} MB / {total_mb:.2f} MB"
        label_progress.configure(text=teks_status)
            

    def execute_download():
        url = entry_url.get().strip()
        if not url:
            messagebox.showwarning("Peringatan", "Masukkan URL YouTube terlebih dahulu!", parent=window)
            return
            
        output_dir = filedialog.askdirectory(title="Pilih Folder Penyimpanan")
        if not output_dir:
            return

        file_type = format_var.get()
        quality = quality_var.get()


        cancel_flag[0] = False
        btn_download.configure(state="disabled", text="⏳ Mengunduh...")
        btn_cancel.configure(state="normal", text="✖ Batalkan")
        btn_cancel.pack(pady=(0, 20), padx=30, fill="x")
        
        progress_bar.set(0)
        label_progress.configure(text="Status: Memulai koneksi...")

        def download_thread():
            success, message = download_yt_process(url, output_dir, file_type, quality, progress_callback=update_progress_ui, cancel_callback=check_cancel)
            
            if success:
                label_progress.configure(text="Status: Selesai!")
                progress_bar.set(1.0)
                messagebox.showinfo("Sukses", message, parent=window)
                entry_url.delete(0, 'end')
            else:
                label_progress.configure(text="Status: Gagal")
                messagebox.showerror("Error", message, parent=window)
                
            btn_download.configure(state="normal", text="⬇️ Mulai Download")
            btn_cancel.pack_forget() 

        threading.Thread(target=download_thread, daemon=True).start()


    # ================= UI ELEMENTS =================
    
    ctk.CTkLabel(window, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    # Input URL
    ctk.CTkLabel(frame_konten, text="URL Video YouTube:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
    entry_url = ctk.CTkEntry(frame_konten, placeholder_text="https://www.youtube.com/watch?v=...", width=400, height=40)
    entry_url.pack(padx=20, pady=(0, 15))

    ctk.CTkLabel(frame_konten, text="Pilih Format:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(5, 5))
    format_var = ctk.StringVar(value="MP4 (Video)")
    format_var.trace_add("write", update_quality_options)
    
    frame_radio = ctk.CTkFrame(frame_konten, fg_color="transparent")
    frame_radio.pack(fill="x", padx=20, pady=(0, 15))
    
    ctk.CTkRadioButton(frame_radio, text="MP4 (Video)", variable=format_var, value="MP4 (Video)").pack(side="left", padx=(0, 20))
    ctk.CTkRadioButton(frame_radio, text="MP3 (Audio Saja)", variable=format_var, value="MP3 (Audio Saja)").pack(side="left")

    label_quality = ctk.CTkLabel(frame_konten, text="Resolusi Video:", font=ctk.CTkFont(weight="bold"))
    label_quality.pack(anchor="w", padx=20, pady=(5, 5))
    
    quality_var = ctk.StringVar(value="720p")
    combo_quality = ctk.CTkComboBox(frame_konten, values=["1080p", "720p", "480p", "360p"], variable=quality_var, state="readonly", width=400)
    combo_quality.pack(padx=20, pady=(0, 20))

    # PROGESS BAR
    label_progress = ctk.CTkLabel(frame_konten, text="Status: Menunggu instruksi...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(10, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_konten, width=400, height=12, progress_color="#2ecc71")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))

    btn_download = ctk.CTkButton(window, text="⬇️ Mulai Download", 
                                 height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                 fg_color="#c0392b", hover_color="#e74c3c",
                                 command=execute_download)
    btn_download.pack(pady=(10, 20), padx=30, fill="x")
    
    btn_cancel = ctk.CTkButton(window, text="✖ Batalkan", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color="#7f8c8d", hover_color="#95a5a6",
                                command=cancel_download)