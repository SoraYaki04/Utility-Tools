import customtkinter as ctk
from tkinter import filedialog, messagebox
import os 
from tools.pdf_compressor import compress_pdf_process

def open_pdf_compressor_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("PDF Compressor")
    window.geometry("450x380") 
    window.resizable(False, False)
    window.grab_set()

    filepath = ctk.StringVar()

    def choose_file():
        path = filedialog.askopenfilename(
            title="Pilih File PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            filepath.set(path)
            label_status.configure(text=f"Terpilih: {os.path.basename(path)}", text_color="#2ecc71")

    def compress_file():
        if not filepath.get():
            messagebox.showwarning("Peringatan", "Pilih file PDF terlebih dahulu!", parent=window)
            return
            
        original_path = filepath.get()
        file_name, _ = os.path.splitext(os.path.basename(original_path))
            
        save_path = filedialog.asksaveasfilename(
            title="Simpan PDF Sebagai",
            initialfile=f"{file_name}_compressed",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if save_path:

            level_dipilih = combo_level.get()
            success, pesan = compress_pdf_process(original_path, save_path, level=level_dipilih)
            
            if success:
                messagebox.showinfo("Sukses", pesan, parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", pesan, parent=window)

    # ================= UI ELEMENTS =================
    ctk.CTkLabel(window, text="Kompresi PDF", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
    
    frame_konten = ctk.CTkFrame(window, corner_radius=15)
    frame_konten.pack(pady=10, padx=30, fill="both", expand=True)

    ctk.CTkButton(frame_konten, text="📁 1. Pilih File PDF", 
                  fg_color="#7f8c8d", hover_color="#95a5a6",
                  height=40, font=ctk.CTkFont(weight="bold"), 
                  command=choose_file).pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_konten, text="Belum ada file terpilih", text_color="gray")
    label_status.pack(pady=(0, 15))
    
    # Dropdown level
    frame_level = ctk.CTkFrame(frame_konten, fg_color="transparent")
    frame_level.pack(pady=(0, 15))
    
    ctk.CTkLabel(frame_level, text="Level Kompresi:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
    
    combo_level = ctk.CTkComboBox(frame_level, values=["Fast", "Medium", "Ekstrem"], state="readonly", width=140)
    combo_level.set("Medium") # default
    combo_level.pack(side="left", padx=5)
    
    
    ctk.CTkButton(frame_konten, text="🗜️ 2. Kompres & Simpan", 
                  height=45, font=ctk.CTkFont(size=14, weight="bold"),
                  command=compress_file).pack(pady=(5, 20), padx=40, fill="x")