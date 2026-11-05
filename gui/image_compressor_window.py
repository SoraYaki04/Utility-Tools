import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from tools.image_compressor import compress_image_process

def open_image_compressor_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Image Compressor")
    window.geometry("450x380")
    window.resizable(False, False)
    window.grab_set()

    filepath = ctk.StringVar()

    def choose_image():
        path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")]
        )
        if path:
            filepath.set(path)
            label_status.configure(text=f"Terpilih: {os.path.basename(path)}", text_color="#2ecc71")

    def compress_image():
        if not filepath.get():
            messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu!", parent=window)
            return
            
        original_path = filepath.get()
        file_name_no_ext, original_ext = os.path.splitext(os.path.basename(original_path))
            
        save_path = filedialog.asksaveasfilename(
            title="Simpan Gambar Sebagai",
            initialfile=f"{file_name_no_ext}_compressed",
            defaultextension=original_ext,
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("WEBP", "*.webp")]
        )
        
        if save_path:
            level_selected = combo_level.get()
            success, pesan = compress_image_process(original_path, save_path, compression_level=level_selected)
            
            if success:
                messagebox.showinfo("Sukses", pesan, parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", pesan, parent=window)

    # ================= UI ELEMENTS =================
    ctk.CTkLabel(window, text="Kompresi Gambar", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    ctk.CTkButton(frame_konten, text="📁 1. Pilih Gambar Asli", 
                  fg_color="#7f8c8d", hover_color="#95a5a6",
                  height=40, font=ctk.CTkFont(weight="bold"), 
                  command=choose_image).pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_konten, text="Belum ada gambar terpilih", text_color="gray")
    label_status.pack(pady=(0, 15))
    
    # Dropdown level
    frame_level = ctk.CTkFrame(frame_konten, fg_color="transparent")
    frame_level.pack(pady=(0, 15))
    
    ctk.CTkLabel(frame_level, text="Kualitas:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
    
    combo_level = ctk.CTkComboBox(frame_level, values=["High (Best Quality)", "Medium", "Extreme (Smallest Size)"], state="readonly", width=180)
    combo_level.set("Medium")
    combo_level.pack(side="left", padx=5)
    
    ctk.CTkButton(frame_konten, text="🗜️ 2. Kompres & Simpan", 
                  height=45, font=ctk.CTkFont(size=14, weight="bold"),
                  command=compress_image).pack(pady=(5, 20), padx=40, fill="x")