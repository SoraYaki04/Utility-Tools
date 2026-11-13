import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from tools.yt_downloader import download_yt_process

def open_yt_downloader_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("YouTube Downloader")
    window.geometry("500x580")
    window.resizable(False, False)
    window.transient(parent)
    
    cancel_flag = [False]

    def update_quality_options(*args):
        if var_format.get() in ["MP4 (H.264)", "MP4 (AV1)"]:
            label_quality.configure(text="Video Resolution:")
            combo_quality.configure(values=["1080p", "720p", "480p", "360p"])
            if var_quality.get() not in ["1080p", "720p", "480p", "360p"]:
                var_quality.set("720p")
        else:
            label_quality.configure(text="Audio Bitrate:")
            combo_quality.configure(values=["320kbps", "256kbps", "192kbps", "128kbps"])
            var_quality.set("192kbps")

    def check_cancel():
        return cancel_flag[0]

    def cancel_process():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Cancelling...")

    def update_progress_ui(percent_float, percent_str, speed_str, downloaded_mb, total_mb, eta_str):
        status_text = f"Status: {percent_str} | {speed_str} | ETA: {eta_str}\nProgress: {downloaded_mb:.2f} MB / {total_mb:.2f} MB"
        window.after(0, lambda: progress_bar.set(percent_float))
        window.after(0, lambda: label_progress.configure(text=status_text))

    def execute_download():
        url = entry_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL first!", parent=window)
            return
            
        output_dir = filedialog.askdirectory(title="Select Destination Folder")
        if not output_dir:
            return
        
        file_type = var_format.get()
        quality = var_quality.get()

        cancel_flag[0] = False
        btn_download.configure(state="disabled", text="⏳ Downloading...")
        btn_cancel.configure(state="normal", text="✖ Cancel")
        btn_cancel.pack(pady=(0, 20), padx=30, fill="x")
        
        progress_bar.set(0)
        label_progress.configure(text="Status: Starting connection...")

        def on_success(message):
            label_progress.configure(text="Status: Completed!")
            progress_bar.set(1.0)
            messagebox.showinfo("Success", message, parent=window)
            entry_url.delete(0, 'end')
            btn_download.configure(state="normal", text="⬇️ Start Download")
            btn_cancel.pack_forget()

        def on_error(message):
            label_progress.configure(text=f"Status: {message}")
            if "cancel" not in message.lower():
                messagebox.showerror("Error", message, parent=window)
            btn_download.configure(state="normal", text="⬇️ Start Download")
            btn_cancel.pack_forget()

        def download_thread():
            success, message = download_yt_process(
                url, output_dir, file_type, quality,
                progress_callback=update_progress_ui,
                cancel_callback=check_cancel
            )
            
            if success:
                window.after(0, lambda: on_success(message))
            else:
                window.after(0, lambda: on_error(message))

        threading.Thread(target=download_thread, daemon=True).start()


    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(20, 10))
    
    frame_content = ctk.CTkFrame(window, corner_radius=15)
    frame_content.pack(pady=10, padx=30, fill="both", expand=True)

    # Input URL
    label_url = ctk.CTkLabel(frame_content, text="YouTube Video URL:", font=ctk.CTkFont(weight="bold"))
    label_url.pack(anchor="w", padx=20, pady=(20, 5))
    
    entry_url = ctk.CTkEntry(frame_content, placeholder_text="https://www.youtube.com/watch?v=...", width=400, height=40)
    entry_url.pack(padx=20, pady=(0, 15))

    # Format Selection
    label_format = ctk.CTkLabel(frame_content, text="Select Format:", font=ctk.CTkFont(weight="bold"))
    label_format.pack(anchor="w", padx=20, pady=(5, 5))
    
    var_format = ctk.StringVar(value="MP4 (H.264)")
    var_format.trace_add("write", update_quality_options)
    
    frame_radio = ctk.CTkFrame(frame_content, fg_color="transparent")
    frame_radio.pack(fill="x", padx=20, pady=(0, 15))
    
    radio_h264 = ctk.CTkRadioButton(frame_radio, text="MP4 (Standart)", variable=var_format, value="MP4 (H.264)")
    radio_h264.pack(side="left", padx=(0, 15))
    
    radio_av1 = ctk.CTkRadioButton(frame_radio, text="MP4 (AV1)", variable=var_format, value="MP4 (AV1)")
    radio_av1.pack(side="left", padx=(0, 15))
    
    radio_mp3 = ctk.CTkRadioButton(frame_radio, text="MP3 (Audio)", variable=var_format, value="MP3 (Audio)")
    radio_mp3.pack(side="left")

    # Resolution/Quality Selection
    label_quality = ctk.CTkLabel(frame_content, text="Video Resolution:", font=ctk.CTkFont(weight="bold"))
    label_quality.pack(anchor="w", padx=20, pady=(5, 5))
    
    var_quality = ctk.StringVar(value="720p")
    combo_quality = ctk.CTkComboBox(frame_content, values=["1080p", "720p", "480p", "360p"], variable=var_quality, state="readonly", width=400)
    combo_quality.pack(padx=20, pady=(0, 20))

    # Progress Bar Area
    label_progress = ctk.CTkLabel(frame_content, text="Status: Waiting for instructions...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(10, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_content, width=400, height=12, progress_color="#2ecc71")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))

    # Execute Button
    btn_download = ctk.CTkButton(window, text="⬇️ Start Download", 
                                 height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                 fg_color="#c0392b", hover_color="#e74c3c",
                                 command=execute_download)
    btn_download.pack(pady=(10, 20), padx=30, fill="x")
    
    # Cancel Button
    btn_cancel = ctk.CTkButton(window, text="✖ Cancel", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_process)

    return window