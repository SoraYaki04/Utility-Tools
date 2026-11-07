import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from tools.video_to_mp3 import convert_media_to_mp3

def open_video_to_mp3_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("MP4 to MP3 Converter Pro")
    window.geometry("500x500") 
    window.resizable(False, False)
    window.grab_set()

    filepath = ctk.StringVar()
    cancel_flag = [False]

    def check_cancel():
        return cancel_flag[0]

    def cancel_conversion():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Membatalkan...")

    def update_progress_ui(percent_float, percent_str):
        progress_bar.set(percent_float)
        label_progress.configure(text=f"Status: Mengonversi... {percent_str}")

    def choose_file():
        path = filedialog.askopenfilename(
            title="Pilih Video/Audio",
            filetypes=[("Media Files", "*.mp4;*.m4a;*.mkv;*.avi;*.mov")]
        )
        if path:
            filepath.set(path)
            label_status.configure(text=f"Terpilih: {os.path.basename(path)}")

    def execute_conversion():
        original_path = filepath.get()
        if not original_path:
            messagebox.showwarning("Peringatan", "Pilih file media terlebih dahulu!", parent=window)
            return
            
        file_name, _ = os.path.splitext(os.path.basename(original_path))
        bitrate = quality_var.get().replace("kbps", "k")
            
        save_path = filedialog.asksaveasfilename(
            title="Simpan MP3 Sebagai",
            initialfile=f"{file_name} [{bitrate}]",
            defaultextension=".mp3",
            filetypes=[("MP3 Audio", "*.mp3")]
        )
        
        if not save_path:
            return


        cancel_flag[0] = False
        btn_convert.configure(state="disabled", text="⏳ Mengonversi...")
        btn_cancel.configure(state="normal", text="✖ Batalkan")
        btn_cancel.pack(pady=(0, 20), padx=30, fill="x") 
        
        progress_bar.set(0)
        label_progress.configure(text="Status: Memulai konversi FFmpeg...")

        def convert_thread():
            success, message = convert_media_to_mp3(
                original_path, save_path, bitrate,
                progress_callback=update_progress_ui,
                cancel_callback=check_cancel
            )
            
            if success:
                label_progress.configure(text="Status: Selesai!")
                progress_bar.set(1.0)
                messagebox.showinfo("Sukses", message, parent=window)
                filepath.set("")
                label_status.configure(text="Belum ada file terpilih")
            else:
                label_progress.configure(text=f"Status: {message}")
                if "dibatalkan" not in message.lower():
                    messagebox.showerror("Error", message, parent=window)
                
            btn_convert.configure(state="normal", text="🗜️ Mulai Konversi")
            btn_cancel.pack_forget()

        threading.Thread(target=convert_thread, daemon=True).start()


    # UI ELEMENTS
    ctk.CTkLabel(window, text="Video to MP3 Converter", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    ctk.CTkButton(frame_konten, text="📁 Pilih Video / Media", 
                  fg_color="#7f8c8d", hover_color="#95a5a6",
                  height=40, font=ctk.CTkFont(weight="bold"), 
                  command=choose_file).pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_konten, text="Belum ada file terpilih", text_color="gray")
    label_status.pack(pady=(0, 15))

    ctk.CTkLabel(frame_konten, text="Kualitas Audio (Bitrate):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(5, 5))
    quality_var = ctk.StringVar(value="320kbps")
    combo_quality = ctk.CTkComboBox(frame_konten, values=["320kbps", "256kbps", "192kbps", "128kbps"], variable=quality_var, state="readonly", width=400)
    combo_quality.pack(padx=20, pady=(0, 15))

    # Progress Bar
    label_progress = ctk.CTkLabel(frame_konten, text="Status: Menunggu instruksi...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(10, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_konten, width=400, height=12, progress_color="#3498db")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))

    btn_convert = ctk.CTkButton(window, text="🗜️ Mulai Konversi", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=execute_conversion)
    btn_convert.pack(pady=(10, 10), padx=30, fill="x")

    btn_cancel = ctk.CTkButton(window, text="✖ Batalkan", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_conversion)