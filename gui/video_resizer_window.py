import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from tools.video_resizer import resize_video_process

def open_video_resizer_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Video Resizer")
    window.geometry("450x540") 
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

    def execute_resize():
        if not filepath.get():
            messagebox.showwarning("Peringatan", "Pilih video terlebih dahulu!", parent=window)
            return
            
        original_path = filepath.get()
        file_name_no_ext, original_ext = os.path.splitext(os.path.basename(original_path))
        
        target_res = combo_resolution.get()
        res_label = target_res.split(" ")[1].replace("(", "").replace(")", "")
            
        save_path = filedialog.asksaveasfilename(
            title="Simpan Video Sebagai",
            initialfile=f"{file_name_no_ext}_{res_label}",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        
        if save_path:

            cancel_flag[0] = False
            btn_execute.configure(state="disabled", text="⏳ Memproses Video...")
            btn_cancel.configure(state="normal", text="✖ Batalkan")
            btn_cancel.pack(pady=(0, 20), padx=40, fill="x") 
            
            progress_bar.set(0)
            label_progress.configure(text="Status: Memulai FFmpeg...")
            
            def process_thread():
                success, pesan = resize_video_process(
                    original_path, save_path, target_res,
                    progress_callback=update_progress_ui,
                    cancel_callback=check_cancel
                )
                
                if success:
                    label_progress.configure(text="Status: Selesai!")
                    progress_bar.set(1.0)
                    messagebox.showinfo("Sukses", pesan, parent=window)
                    window.destroy()
                else:
                    label_progress.configure(text=f"Status: {pesan}")
                    if "dibatalkan" not in pesan.lower():
                        messagebox.showerror("Error", pesan, parent=window)
                    

                btn_execute.configure(state="normal", text="🗜️ 2. Ubah Resolusi & Simpan")
                btn_cancel.pack_forget()

            threading.Thread(target=process_thread, daemon=True).start()


    # ================= UI ELEMENTS =================
    ctk.CTkLabel(window, text="Video Resizer", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    ctk.CTkButton(frame_konten, text="📁 1. Pilih Video", 
                  fg_color="#7f8c8d", hover_color="#95a5a6",
                  height=40, font=ctk.CTkFont(weight="bold"), 
                  command=choose_video).pack(pady=(25, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_konten, text="Belum ada video terpilih", text_color="gray")
    label_status.pack(pady=(0, 10))
    

    frame_res = ctk.CTkFrame(frame_konten, fg_color="transparent")
    frame_res.pack(pady=(10, 5))
    
    ctk.CTkLabel(frame_res, text="Resolusi Target:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
    
    resolutions = [
        "1920x1080 (1080p)",
        "1280x720 (720p)",
        "854x480 (480p)",
        "640x360 (360p)"
    ]
    combo_resolution = ctk.CTkComboBox(frame_res, values=resolutions, state="readonly", width=160)
    combo_resolution.set("1280x720 (720p)")
    combo_resolution.pack(side="left", padx=5)

    warning_text = (
        "Catatan: Memilih resolusi yang lebih tinggi dari video\n"
        "asli tidak akan meningkatkan kualitas gambar,\n"
        "melainkan hanya akan memperbesar ukuran file."
    )
    label_warning = ctk.CTkLabel(frame_konten, text=warning_text, text_color="#e67e22", 
                                 font=ctk.CTkFont(size=11, slant="italic"))
    label_warning.pack(pady=(0, 15))


    label_progress = ctk.CTkLabel(frame_konten, text="Status: Menunggu instruksi...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(5, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_konten, width=400, height=12, progress_color="#2ecc71")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))
    
    btn_execute = ctk.CTkButton(frame_konten, text="🗜️ 2. Ubah Resolusi & Simpan", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=execute_resize)
    btn_execute.pack(pady=(5, 15), padx=40, fill="x")


    btn_cancel = ctk.CTkButton(window, text="✖ Batalkan", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_resize)