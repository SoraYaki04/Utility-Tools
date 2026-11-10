import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pymupdf
import os
from tools.pdf_merger import pdf_merger_process

def open_pdf_merger_window(parent):
    window = ctk.CTkToplevel(parent)
    window.title("📄 PDF Merger")
    window.geometry("650x550")
    window.resizable(False, False)
    window.transient(parent)

    filepaths = []

    def choose_file():
        files = filedialog.askopenfilenames(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for f in files:
            if f not in filepaths:
                filepaths.append(f)
                listbox_files.insert(tk.END, os.path.basename(f))

    def delete_list():
        filepaths.clear()
        listbox_files.delete(0, tk.END)
        label_thumbnail.configure(image="", text="No\npreview")

    def delete_selected():
        selection = listbox_files.curselection()
        if selection:
            idx = selection[0]
            listbox_files.delete(idx)
            filepaths.pop(idx)
            label_thumbnail.configure(image="", text="No\npreview")

    def move_up():
        selection = listbox_files.curselection()
        if not selection: return
        idx = selection[0]
        if idx > 0:
            filepaths[idx-1], filepaths[idx] = filepaths[idx], filepaths[idx-1]
            text_val = listbox_files.get(idx)
            listbox_files.delete(idx)
            listbox_files.insert(idx-1, text_val)
            listbox_files.selection_set(idx-1)

    def move_down():
        selection = listbox_files.curselection()
        if not selection: return
        idx = selection[0]
        if idx < len(filepaths) - 1:
            filepaths[idx+1], filepaths[idx] = filepaths[idx], filepaths[idx+1]
            text_val = listbox_files.get(idx)
            listbox_files.delete(idx)
            listbox_files.insert(idx+1, text_val)
            listbox_files.selection_set(idx+1)

    def show_thumbnail(event):
        selection = listbox_files.curselection()
        if not selection: return
        
        filepath = filepaths[selection[0]]
        try:
            doc = pymupdf.open(filepath)
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=72)
            
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ctk_img = ctk.CTkImage(light_image=img, size=(180, 240))
            
            label_thumbnail.configure(image=ctk_img, text="")
            doc.close()
        except Exception as e:
            label_thumbnail.configure(image="", text="Failed to load\npreview")

    def enlarge_preview():
        selection = listbox_files.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a file from the list first!")
            return
            
        filepath = filepaths[selection[0]]
        try:
            doc = pymupdf.open(filepath)
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150) 
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            img.thumbnail((700, 800), Image.Resampling.LANCZOS)
            
            preview_window = ctk.CTkToplevel(window)
            preview_window.title(f"Preview: {os.path.basename(filepath)}")
            
            ctk_img_large = ctk.CTkImage(light_image=img, size=(img.width, img.height))
            lbl_large = ctk.CTkLabel(preview_window, image=ctk_img_large, text="")
            lbl_large.pack(padx=20, pady=20)
            
            doc.close()
            
            preview_window.transient(window)
            preview_window.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enlarge preview:\n{str(e)}")

    def execute_merger():
        if len(filepaths) < 2:
            messagebox.showwarning("Warning", "Select at least 2 PDF files to merge!")
            return

        file_output = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="merged_output.pdf"
        )

        if file_output:
            success, message = pdf_merger_process(filepaths, file_output)
            if success:
                messagebox.showinfo("Success", message)
                delete_list()
                window.destroy()
            else:
                messagebox.showerror("Error", f"An error occurred:\n{message}")
                

    # ================= UI ELEMENTS =================
    label_title = ctk.CTkLabel(window, text="Merge PDF Files", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=(15, 5))

    label_info = ctk.CTkLabel(window, text="Click a file to preview. Use buttons to reorder.", text_color="gray")
    label_info.pack()

    frame_content = ctk.CTkFrame(window, fg_color="transparent")
    frame_content.pack(padx=20, pady=10, fill="both", expand=True)

    # --- Left Panel (File List) ---
    frame_left = ctk.CTkFrame(frame_content)
    frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    listbox_files = tk.Listbox(frame_left, selectmode=tk.SINGLE, bg="#2B2B2B", fg="white", 
                               selectbackground="#1F538D", font=("Arial", 11), borderwidth=0, highlightthickness=1)
    listbox_files.pack(padx=10, pady=10, fill="both", expand=True)
    listbox_files.bind("<<ListboxSelect>>", show_thumbnail)

    frame_controls = ctk.CTkFrame(frame_left, fg_color="transparent")
    frame_controls.pack(pady=(0, 10))

    btn_up = ctk.CTkButton(frame_controls, text="⬆ Up", width=60, command=move_up)
    btn_up.pack(side="left", padx=5)
    
    btn_down = ctk.CTkButton(frame_controls, text="⬇ Down", width=60, command=move_down)
    btn_down.pack(side="left", padx=5)
    
    btn_remove = ctk.CTkButton(frame_controls, text="❌ Remove", width=60, fg_color="#C8504B", hover_color="#8E3533", command=delete_selected)
    btn_remove.pack(side="left", padx=5)

    # --- Right Panel (Thumbnail) ---
    frame_right = ctk.CTkFrame(frame_content, width=200)
    frame_right.pack(side="right", fill="y")
    frame_right.pack_propagate(False)

    label_thumb_title = ctk.CTkLabel(frame_right, text="Page Preview", font=ctk.CTkFont(weight="bold"))
    label_thumb_title.pack(pady=(10, 5))

    label_thumbnail = ctk.CTkLabel(frame_right, text="No\npreview", width=180, height=240, fg_color="#333333", corner_radius=8)
    label_thumbnail.pack(padx=10, pady=5)
    
    btn_enlarge = ctk.CTkButton(frame_right, text="🔍 Enlarge", width=150, command=enlarge_preview, fg_color="#4A4D50", hover_color="#333538")
    btn_enlarge.pack(pady=(5, 10))

    # ================= Control panel =================
    frame_btn_bottom = ctk.CTkFrame(window, fg_color="transparent")
    frame_btn_bottom.pack(padx=20, pady=(0, 20), fill="x")

    btn_select = ctk.CTkButton(frame_btn_bottom, text="Select File", command=choose_file, width=130)
    btn_select.pack(side="left", padx=5)

    btn_clear = ctk.CTkButton(frame_btn_bottom, text="Clear All", command=delete_list, width=130, 
                              fg_color="#C8504B", hover_color="#8E3533")
    btn_clear.pack(side="left", padx=5)

    btn_merge = ctk.CTkButton(frame_btn_bottom, text="Merge!", command=execute_merger, width=130, 
                               fg_color="#28A745", hover_color="#218838")
    btn_merge.pack(side="right", padx=5)
    
    return window