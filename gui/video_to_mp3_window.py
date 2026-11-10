import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from tools.video_to_mp3 import convert_media_to_mp3

def open_video_to_mp3_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("MP4 to MP3 Converter")
    window.geometry("500x500") 
    window.resizable(False, False)
    window.transient(parent)

    var_filepath = ctk.StringVar()
    cancel_flag = [False]

    def check_cancel():
        return cancel_flag[0]

    def cancel_process():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Cancelling...")

    def update_progress_ui(percent_float, percent_str):
        progress_bar.set(percent_float)
        label_progress.configure(text=f"Status: Converting... {percent_str}")

    def choose_file():
        path = filedialog.askopenfilename(
            title="Select Video/Audio",
            filetypes=[("Media Files", "*.mp4;*.m4a;*.mkv;*.avi;*.mov")]
        )
        if path:
            var_filepath.set(path)
            label_status.configure(text=f"Selected: {os.path.basename(path)}")

    def execute_conversion():
        original_path = var_filepath.get()
        if not original_path:
            messagebox.showwarning("Warning", "Please select a media file first!", parent=window)
            return
            
        file_name, _ = os.path.splitext(os.path.basename(original_path))
        bitrate = var_quality.get().replace("kbps", "k")
            
        save_path = filedialog.asksaveasfilename(
            title="Save MP3 As",
            initialfile=f"{file_name} [{bitrate}]",
            defaultextension=".mp3",
            filetypes=[("MP3 Audio", "*.mp3")]
        )
        
        if not save_path:
            return

        cancel_flag[0] = False
        btn_execute.configure(state="disabled", text="⏳ Converting...")
        btn_cancel.configure(state="normal", text="✖ Cancel")
        btn_cancel.pack(pady=(0, 20), padx=30, fill="x") 
        
        progress_bar.set(0)
        label_progress.configure(text="Status: Starting FFmpeg conversion...")

        def on_success(message):
            label_progress.configure(text="Status: Completed!")
            progress_bar.set(1.0)
            messagebox.showinfo("Success", message, parent=window)
            
            var_filepath.set("")
            label_status.configure(text="No file selected")
            btn_execute.configure(state="normal", text="🗜️ Start Conversion")
            btn_cancel.pack_forget()

        def on_error(message):
            label_progress.configure(text=f"Status: {message}")
            if "cancel" not in message.lower():
                messagebox.showerror("Error", message, parent=window)
            btn_execute.configure(state="normal", text="🗜️ Start Conversion")
            btn_cancel.pack_forget()

        def convert_thread():
            success, message = convert_media_to_mp3(
                original_path, save_path, bitrate,
                progress_callback=update_progress_ui,
                cancel_callback=check_cancel
            )
            
            if success:
                window.after(0, lambda: on_success(message))
            else:
                window.after(0, lambda: on_error(message))

        threading.Thread(target=convert_thread, daemon=True).start()


    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="Video to MP3 Converter", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(20, 10))
    
    frame_content = ctk.CTkFrame(window, corner_radius=15)
    frame_content.pack(pady=10, padx=30, fill="both", expand=True)

    btn_select = ctk.CTkButton(frame_content, text="📁 Select Video / Media", 
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               height=40, font=ctk.CTkFont(weight="bold"), 
                               command=choose_file)
    btn_select.pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_content, text="No file selected", text_color="gray")
    label_status.pack(pady=(0, 15))

    label_quality = ctk.CTkLabel(frame_content, text="Audio Quality (Bitrate):", font=ctk.CTkFont(weight="bold"))
    label_quality.pack(anchor="w", padx=20, pady=(5, 5))
    
    var_quality = ctk.StringVar(value="320kbps")
    combo_quality = ctk.CTkComboBox(frame_content, values=["320kbps", "256kbps", "192kbps", "128kbps"], variable=var_quality, state="readonly", width=400)
    combo_quality.pack(padx=20, pady=(0, 15))

    # Progress Bar
    label_progress = ctk.CTkLabel(frame_content, text="Status: Waiting for instructions...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(10, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_content, width=400, height=12, progress_color="#3498db")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))

    btn_execute = ctk.CTkButton(window, text="🗜️ Start Conversion", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=execute_conversion)
    btn_execute.pack(pady=(10, 10), padx=30, fill="x")

    btn_cancel = ctk.CTkButton(window, text="✖ Cancel", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_process)
    
    return window