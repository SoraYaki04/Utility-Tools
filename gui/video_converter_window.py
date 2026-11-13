import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from tools.video_converter import convert_video_process

def open_video_converter_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Video Converter")
    window.geometry("450x520")
    window.resizable(False, False)
    window.transient(parent)

    var_filepath = ctk.StringVar()
    cancel_flag = [False]

    def choose_video():
        path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.webm;*.flv")]
        )
        if path:
            var_filepath.set(path)
            label_status.configure(text=f"Selected: {os.path.basename(path)}", text_color="#2ecc71")

    def check_cancel():
        return cancel_flag[0]

    def cancel_conversion():
        cancel_flag[0] = True
        btn_cancel.configure(state="disabled", text="Cancelling...")

    def update_progress_ui(percent_float, percent_str):
        window.after(0, lambda: progress_bar.set(percent_float))
        window.after(0, lambda: label_progress.configure(text=f"Status: Converting... {percent_str}"))

    def execute_conversion():
        if not var_filepath.get():
            messagebox.showwarning("Warning", "Please select a video first!", parent=window)
            return
            
        original_path = var_filepath.get()
        file_name_no_ext, _ = os.path.splitext(os.path.basename(original_path))
        target_format = var_format.get()
        
        save_path = filedialog.asksaveasfilename(
            title="Save Video As",
            initialfile=file_name_no_ext,
            defaultextension=target_format,
            filetypes=[(f"{target_format.upper().replace('.', '')} Video", f"*{target_format}")]
        )
        
        if save_path:
            cancel_flag[0] = False
            btn_execute.configure(state="disabled", text="⏳ Converting...")
            btn_cancel.configure(state="normal", text="✖ Cancel")
            btn_cancel.pack(pady=(0, 20), padx=30, fill="x")
            
            progress_bar.set(0)
            label_progress.configure(text="Status: Starting FFmpeg...")
            
            def on_success(message):
                label_progress.configure(text="Status: Completed!")
                progress_bar.set(1.0)
                messagebox.showinfo("Success", message, parent=window)
                window.destroy()

            def on_error(message):
                label_progress.configure(text=f"Status: {message}")
                if "cancelled" not in message.lower():
                    messagebox.showerror("Error", message, parent=window)
                btn_execute.configure(state="normal", text="🔄 2. Convert & Save")
                btn_cancel.pack_forget()

            def process_thread():
                success, message = convert_video_process(
                    original_path, save_path,
                    progress_callback=update_progress_ui,
                    cancel_callback=check_cancel
                )
                
                if success:
                    window.after(0, lambda: on_success(message))
                else:
                    window.after(0, lambda: on_error(message))

            threading.Thread(target=process_thread, daemon=True).start()


    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="Video Converter", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(20, 10))
    
    frame_content = ctk.CTkFrame(window, corner_radius=15)
    frame_content.pack(pady=10, padx=30, fill="both", expand=True)

    btn_select = ctk.CTkButton(frame_content, text="📁 1. Select Video", 
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               height=40, font=ctk.CTkFont(weight="bold"), 
                               command=choose_video)
    btn_select.pack(pady=(25, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_content, text="No video selected", text_color="gray")
    label_status.pack(pady=(0, 15))
    
    
    frame_format = ctk.CTkFrame(frame_content, fg_color="transparent")
    frame_format.pack(pady=(5, 15))
    
    label_format = ctk.CTkLabel(frame_format, text="Convert to:", font=ctk.CTkFont(weight="bold"))
    label_format.pack(side="left", padx=5)
    
    var_format = ctk.StringVar(value=".mp4")
    combo_format = ctk.CTkComboBox(frame_format, values=[".mp4", ".mkv", ".avi", ".mov", ".webm"], 
                                   variable=var_format, state="readonly", width=120)
    combo_format.pack(side="left", padx=5)


    label_progress = ctk.CTkLabel(frame_content, text="Status: Waiting for instruction...", text_color="gray", font=ctk.CTkFont(size=12))
    label_progress.pack(anchor="w", padx=20, pady=(10, 0))
    
    progress_bar = ctk.CTkProgressBar(frame_content, width=400, height=12, progress_color="#2ecc71")
    progress_bar.set(0)
    progress_bar.pack(padx=20, pady=(5, 20))
    
    btn_execute = ctk.CTkButton(frame_content, text="🔄 2. Convert & Save", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=execute_conversion)
    btn_execute.pack(pady=(5, 20), padx=40, fill="x")

    btn_cancel = ctk.CTkButton(window, text="✖ Cancel", 
                               height=45, font=ctk.CTkFont(size=14, weight="bold"),
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               command=cancel_conversion)

    return window