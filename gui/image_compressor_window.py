import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from tools.image_compressor import compress_image_process

def open_image_compressor_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Image Compressor")
    window.geometry("450x380")
    window.resizable(False, False)
    window.transient(parent)

    filepath = ctk.StringVar()

    def choose_image():
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")]
        )
        if path:
            filepath.set(path)
            label_status.configure(text=f"Selected: {os.path.basename(path)}", text_color="#2ecc71")

    def compress_image():
        if not filepath.get():
            messagebox.showwarning("Warning", "Add an image first!", parent=window)
            return
            
        original_path = filepath.get()
        file_name_no_ext, original_ext = os.path.splitext(os.path.basename(original_path))
            
        save_path = filedialog.asksaveasfilename(
            title="Save Image As",
            initialfile=f"{file_name_no_ext}_compressed",
            defaultextension=original_ext,
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("WEBP", "*.webp")]
        )
        
        if save_path:
            level_selected = combo_level.get()
            success, pesan = compress_image_process(original_path, save_path, compression_level=level_selected)
            
            if success:
                messagebox.showinfo("Success", pesan, parent=window)
            else:
                messagebox.showerror("Error", pesan, parent=window)


    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="Image Compressor", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(20, 10))
    
    frame_content = ctk.CTkFrame(window, corner_radius=15)
    frame_content.pack(pady=10, padx=30, fill="both", expand=True)

    btn_select = ctk.CTkButton(frame_content, text="📁 1. Select Original Image", 
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               height=40, font=ctk.CTkFont(weight="bold"), 
                               command=choose_image)
    btn_select.pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_content, text="No image selected", text_color="gray")
    label_status.pack(pady=(0, 15))
    
    # Dropdown level
    frame_level = ctk.CTkFrame(frame_content, fg_color="transparent")
    frame_level.pack(pady=(0, 15))
    
    label_quality = ctk.CTkLabel(frame_level, text="Quality:", font=ctk.CTkFont(weight="bold"))
    label_quality.pack(side="left", padx=5)
    
    combo_level = ctk.CTkComboBox(frame_level, values=["High (Best Quality)", "Medium", "Extreme (Smallest Size)"], state="readonly", width=180)
    combo_level.set("Medium")
    combo_level.pack(side="left", padx=5)
    
    btn_execute = ctk.CTkButton(frame_content, text="🗜️ 2. Compress & Save", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=compress_image)
    btn_execute.pack(pady=(5, 20), padx=40, fill="x")
    
    return window