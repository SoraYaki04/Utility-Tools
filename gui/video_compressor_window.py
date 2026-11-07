import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from tools.video_compressor import compress_video_process

def open_video_compressor_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Video Compressor")
    window.geometry("450x520") 
    window.resizable(False, False)
    window.grab_set()

    filepath = ctk.StringVar()
    cancel_flag = [False]

    def choose_video():
        path = filedialog.askopenfilename(
            title="Pilih Video",
            filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov")]
        )
        if path:
            filepath.set(path)
            label_status.configure(text=f"Terpilih: {os.path.basename(path)}", text_color="#2ecc71")

    def check_cancel():
        return cancel_flag[0]

    def cancel_resize():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Membatalkan...")

    def update_progress_ui(percent_float, percent_str):
        progress_bar.set(percent_float)
        label_progress.configure(text=f"Status: Memproses... {percent_str}")

    def execute_process():
        if not filepath.get():
            messagebox.showwarning("Peringatan", "Pilih video terlebih dahulu!", parent=window)
            return
            
        original_path = filepath.get()
        file_name_no_ext, _ = os.path.splitext(os.path.basename(original_path))
        
        target_comp = combo_compress.get()
        level_label = target_comp.split(" ")[0].lower() 
            
        save_path = filedialog.asksaveasfilename(
            title="Simpan Video Sebagai",
            initialfile=f"{file_name_no_ext}_{level_label}",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        
        if save_path:
            cancel_flag[0] = False
            btn_execute.configure(state="disabled", text="⏳ Sedang Memproses...")
            btn_cancel.configure(state="normal", text="✖ Batalkan")
            btn_cancel.pack(pady=(0, 20), padx=40, fill="x") 
            
            progress_bar.set(0)
            label_progress.configure(text="Status: Memulai penyandian video...")
            
            def on_success(pesan):
                label_progress.configure(text="Status: Selesai!")
                progress_bar.set(1.0)
                messagebox.showinfo("Sukses", pesan, parent=window)
 
                window.destroy()

            def on_error(pesan):
                label_progress.configure(text=f"Status: {pesan}")
                if "dibatalkan" not in pesan.lower():
                    messagebox.showerror("Error", pesan, parent=window)
                btn_execute.configure(state="normal", text="🗜️ 2. Mulai Kompresi")
                btn_cancel.pack_forget()

            def process_thread():
                success, pesan = compress_video_process(
                    original_path, save_path, level=target_comp,
                    progress_callback=update_progress_ui,
                    cancel_callback=check_cancel
                )
                
                if success:
                    window.after(0, lambda: on_success(pesan))
                else:
                    window.after(0, lambda: on_error(pesan))

            threading.Thread(target=process_thread, daemon=True).start()

    # ================= UI ELEMENTS =================
    ctk.CTkLabel(window, text="Video Compressor", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    ctk.CTkButton(frame_konten, text="📁 1. Pilih Video Asli", 
                  fg_color="#7f8c8d", hover_color="#95a5a6",
                  height=40, font=ctk.CTkFont(weight="bold"), 
                  command=choose_video).pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_konten, text="Belum ada video terpilih", text_color="gray")
    label_status.pack(pady=(0, 15))


    frame_comp = ctk.CTkFrame(frame_konten, fg_color="transparent")
    frame_comp.pack(pady=(5, 10))
    
    ctk.CTkLabel(frame_comp, text="Level Kompresi:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
    compressions = ["Balanced (720p)", "Small (480p)", "Smallest (360p)"]
    combo_compress = ctk.CTkComboBox(frame_comp, values=compressions, state="readonly", width=180)
    combo_compress.set("Balanced (720p)")
    combo_compress.pack(side="left", padx=5)

    warning_text = (
        "Catatan: Semakin kecil file yang dihasilkan, semakin\n"
        "rendah resolusi visual akhirnya. Proses ini mungkin\n"
        "memakan waktu tergantung performa CPU Anda."
    )
    label_warning = ctk.CTkLabel(frame_konten, text=warning_text, text_color="#e67e22", 
                                 font=ctk.CTkFont(size=11, slant="italic"))
    label_warning.pack(pady=(0, 15))


    label_progress = ctk.CTkLabel(frame_konten, text="Status: Menunggu instruksi...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(5, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_konten, width=400, height=12, progress_color="#2ecc71")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))
    
    btn_execute = ctk.CTkButton(frame_konten, text="🗜️ 2. Mulai Kompresi", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=execute_process)
    btn_execute.pack(pady=(5, 15), padx=40, fill="x")
    
    btn_cancel = ctk.CTkButton(window, text="✖ Batalkan", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_resize)