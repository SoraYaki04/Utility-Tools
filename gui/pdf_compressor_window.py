import customtkinter as ctk
from tkinter import filedialog, messagebox
import os 
from tools.pdf_compressor import compress_pdf_process

def open_pdf_compressor_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("PDF Compressor")
    window.geometry("450x380") 
    window.resizable(False, False)
    window.transient(parent)

    var_filepath = ctk.StringVar()

    def choose_file():
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            var_filepath.set(file_path)
            label_status.configure(text=f"Selected: {os.path.basename(file_path)}", text_color="#2ecc71")

    def compress_file():
        if not var_filepath.get():
            messagebox.showwarning("Warning", "Please select a PDF file first!", parent=window)
            return
            
        original_path = var_filepath.get()
        file_name, _ = os.path.splitext(os.path.basename(original_path))
            
        save_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            initialfile=f"{file_name}_compressed",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if save_path:
            selected_level = combo_level.get()
            success, message = compress_pdf_process(original_path, save_path, level=selected_level)
            
            if success:
                messagebox.showinfo("Success", message, parent=window)
            else:
                messagebox.showerror("Error", message, parent=window)


    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="Compress PDF", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(20, 10))
    
    frame_content = ctk.CTkFrame(window, corner_radius=15)
    frame_content.pack(pady=10, padx=30, fill="both", expand=True)

    btn_select = ctk.CTkButton(frame_content, text="📁 1. Select PDF File", 
                               fg_color="#7f8c8d", hover_color="#95a5a6",
                               height=40, font=ctk.CTkFont(weight="bold"), 
                               command=choose_file)
    btn_select.pack(pady=(20, 5), padx=40, fill="x")
    
    label_status = ctk.CTkLabel(frame_content, text="No file selected", text_color="gray")
    label_status.pack(pady=(0, 15))
    
    # Dropdown level
    frame_level = ctk.CTkFrame(frame_content, fg_color="transparent")
    frame_level.pack(pady=(0, 15))
    
    label_level = ctk.CTkLabel(frame_level, text="Compression Level:", font=ctk.CTkFont(weight="bold"))
    label_level.pack(side="left", padx=5)
    
    combo_level = ctk.CTkComboBox(frame_level, values=["Fast", "Medium", "Extreme"], state="readonly", width=140)
    combo_level.set("Medium") # default
    combo_level.pack(side="left", padx=5)
    
    btn_execute = ctk.CTkButton(frame_content, text="🗜️ 2. Compress & Save", 
                                height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                command=compress_file)
    btn_execute.pack(pady=(5, 20), padx=40, fill="x")
    
    return window