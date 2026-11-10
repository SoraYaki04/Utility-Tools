import customtkinter as ctk
from tkinter import filedialog, messagebox
import os 
from PIL import Image
from tools.image_converter import convert_image_process

def open_image_converter_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Image Converter")
    window.geometry("500x550")
    window.resizable(False, False)
    window.transient(parent)

    filepaths = [] 

    def update_display_list():
        for widget in frame_list.winfo_children():
            widget.destroy()
            
        if not filepaths:
            ctk.CTkLabel(frame_list, text="No images have been added yet.", text_color="gray").pack(pady=20)
            label_status.configure(text="Total: 0 image")
            return

        label_status.configure(text=f"Total: {len(filepaths)} image")

        for path in filepaths:
            frame_row = ctk.CTkFrame(frame_list, fg_color="transparent")
            frame_row.pack(fill="x", pady=5, padx=5)
            
            # Thumbnail 
            try:
                with Image.open(path) as img:
                    img_small = img.copy()
                    img_small.thumbnail((80, 80))
                img_ctk = ctk.CTkImage(light_image=img_small, dark_image=img_small, size=(40, 40))
                ctk.CTkLabel(frame_row, image=img_ctk, text="").pack(side="left", padx=(0, 10))
            except Exception:
                pass
            
            file_name = os.path.basename(path)
            if len(file_name) > 25:
                file_name = file_name[:22] + "..."
                
            ctk.CTkLabel(frame_row, text=file_name, font=ctk.CTkFont(weight="bold")).pack(side="left")
            
            btn_delete = ctk.CTkButton(frame_row, text="❌", width=30, height=30,
                                      fg_color="#e74c3c", hover_color="#c0392b",
                                      command=lambda p=path: delete_image(p))
            btn_delete.pack(side="right")

    def delete_image(delete_path):
        if delete_path in filepaths:
            filepaths.remove(delete_path)
            update_display_list()

    def choose_images():
        paths = filedialog.askopenfilenames(
            title="Select Additional Images",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.jfif;*.bmp;*.webp;*.tiff;*.ico")]
        )
        if paths:
            # Validate duplicate file input
            for p in paths:
                if p not in filepaths:
                    filepaths.append(p)
            update_display_list()

    def convert_images():
        if not filepaths:
            messagebox.showwarning("Warning", "Add an image first!", parent=window)
            return
            
        output_dir = filedialog.askdirectory(title="Select Storage Folder")
        if not output_dir:
            return 
            
        target_format = format_var.get()
        success_count = 0
        
        # Bulk convert
        for path in filepaths:
            file_name_no_ext, _ = os.path.splitext(os.path.basename(path))
            new_filename = f"{file_name_no_ext}{target_format}"
            save_path = os.path.join(output_dir, new_filename)
            
            success, _ = convert_image_process(path, save_path)
            if success:
                success_count += 1
                
        messagebox.showinfo("Done", f"Successfully converted {success_count} from {len(filepaths)} images!", parent=window)
        
        filepaths.clear()
        update_display_list()


    # ================= UI ELEMENTS =================
    ctk.CTkLabel(window, text="Image Converter", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

    # Img bulk container
    frame_list = ctk.CTkScrollableFrame(window, corner_radius=10, height=220)
    frame_list.pack(pady=5, padx=20, fill="both", expand=True)


    # Control panel
    frame_control = ctk.CTkFrame(window, fg_color="transparent")
    frame_control.pack(pady=10, padx=20, fill="x")
    
    ctk.CTkButton(frame_control, text="➕ Add Image", 
                  fg_color="#3498db", hover_color="#2980b9",
                  height=35, font=ctk.CTkFont(weight="bold"), 
                  command=choose_images).pack(side="left", padx=5, expand=True, fill="x")

    label_status = ctk.CTkLabel(frame_control, text="Total: 0 image", font=ctk.CTkFont(weight="bold"))
    label_status.pack(side="right", padx=10)


    # Execute panel
    frame_execute = ctk.CTkFrame(window, corner_radius=10)
    frame_execute.pack(pady=(0, 20), padx=20, fill="x")
    
    ctk.CTkLabel(frame_execute, text="Convert to format:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15, pady=15)
    
    format_var = ctk.StringVar(value=".png")
    ctk.CTkComboBox(frame_execute, values=[".png", ".jpg", ".webp", ".jfif", ".ico", ".bmp"], 
                    variable=format_var, state="readonly", width=90).pack(side="left", padx=5)

    ctk.CTkButton(frame_execute, text="💾 Convert All", 
                  fg_color="#2ecc71", hover_color="#27ae60",
                  height=40, font=ctk.CTkFont(weight="bold"),
                  command=convert_images).pack(side="right", padx=15, pady=15)
    
    update_display_list()
    
    return window