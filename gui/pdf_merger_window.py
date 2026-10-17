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
    window.grab_set()

    # Menyimpan daftar path file PDF
    filepaths = []

  
    def choose_file():
        files = filedialog.askopenfilenames(
            title="Pilih File PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for f in files:
            if f not in filepaths:
                filepaths.append(f)
                listbox_files.insert(tk.END, os.path.basename(f))

    def delete_list():
        filepaths.clear()
        listbox_files.delete(0, tk.END)
        label_thumbnail.configure(image="", text="Tidak ada\npreview")

    def delete_selected():
        selection = listbox_files.curselection()
        if selection:
            idx = selection[0]
            listbox_files.delete(idx)
            filepaths.pop(idx)
            label_thumbnail.configure(image="", text="Tidak ada\npreview")

    def move_up():
        selection = listbox_files.curselection()
        if not selection: return
        idx = selection[0]
        if idx > 0:
            filepaths[idx-1], filepaths[idx] = filepaths[idx], filepaths[idx-1]
            teks = listbox_files.get(idx)
            listbox_files.delete(idx)
            listbox_files.insert(idx-1, teks)
            listbox_files.selection_set(idx-1)

    def move_down():
        selection = listbox_files.curselection()
        if not selection: return
        idx = selection[0]
        if idx < len(filepaths) - 1:
            filepaths[idx+1], filepaths[idx] = filepaths[idx], filepaths[idx+1]
            teks = listbox_files.get(idx)
            listbox_files.delete(idx)
            listbox_files.insert(idx+1, teks)
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
            label_thumbnail.configure(image="", text="Gagal memuat\npreview")

    def enlarge_preview():
        selection = listbox_files.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih file dari daftar terlebih dahulu!")
            return
            
        filepath = filepaths[selection[0]]
        try:
            doc = pymupdf.open(filepath)
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150) 
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            img.thumbnail((700, 800), Image.Resampling.LANCZOS)
            
            # Create new window for large preview
            preview_window = ctk.CTkToplevel(window)
            preview_window.title(f"Preview: {os.path.basename(filepath)}")
            
            ctk_img_large = ctk.CTkImage(light_image=img, size=(img.width, img.height))
            lbl_large = ctk.CTkLabel(preview_window, image=ctk_img_large, text="")
            lbl_large.pack(padx=20, pady=20)
            
            doc.close()
            
            preview_window.transient(window)
            preview_window.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbesar preview:\n{str(e)}")

    def execute_merger():
        if len(filepaths) < 2:
            messagebox.showwarning("Peringatan", "Pilih minimal 2 file PDF untuk digabungkan!")
            return

        file_output = filedialog.asksaveasfilename(
            title="Simpan PDF Sebagai",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="hasil_gabungan.pdf"
        )

        if file_output:
            sukses, pesan = pdf_merger_process(filepaths, file_output)
            if sukses:
                messagebox.showinfo("Sukses", pesan)
                delete_list()
                window.destroy()
            else:
                messagebox.showerror("Error", f"Terjadi kesalahan:\n{pesan}")


    # ================= UI ELEMENTS =================
    
    label_judul = ctk.CTkLabel(window, text="Gabungkan File PDF", font=ctk.CTkFont(size=20, weight="bold"))
    label_judul.pack(pady=(15, 5))

    label_info = ctk.CTkLabel(window, text="Klik file untuk preview. Gunakan tombol untuk mengatur urutan.", text_color="gray")
    label_info.pack()

    frame_konten = ctk.CTkFrame(window, fg_color="transparent")
    frame_konten.pack(padx=20, pady=10, fill="both", expand=True)

    # --- List file ---
    frame_kiri = ctk.CTkFrame(frame_konten)
    frame_kiri.pack(side="left", fill="both", expand=True, padx=(0, 10))

    listbox_files = tk.Listbox(frame_kiri, selectmode=tk.SINGLE, bg="#2B2B2B", fg="white", 
                               selectbackground="#1F538D", font=("Arial", 11), borderwidth=0, highlightthickness=1)
    listbox_files.pack(padx=10, pady=10, fill="both", expand=True)
    listbox_files.bind("<<ListboxSelect>>", show_thumbnail)

    frame_kontrol = ctk.CTkFrame(frame_kiri, fg_color="transparent")
    frame_kontrol.pack(pady=(0, 10))

    ctk.CTkButton(frame_kontrol, text="⬆ Naik", width=60, command=move_up).pack(side="left", padx=5)
    ctk.CTkButton(frame_kontrol, text="⬇ Turun", width=60, command=move_down).pack(side="left", padx=5)
    ctk.CTkButton(frame_kontrol, text="❌ Hapus", width=60, fg_color="#C8504B", hover_color="#8E3533", command=delete_selected).pack(side="left", padx=5)

    # --- Thumbnail ---
    frame_kanan = ctk.CTkFrame(frame_konten, width=200)
    frame_kanan.pack(side="right", fill="y")
    frame_kanan.pack_propagate(False)

    label_thumb_title = ctk.CTkLabel(frame_kanan, text="Preview Halaman", font=ctk.CTkFont(weight="bold"))
    label_thumb_title.pack(pady=(10, 5))

    label_thumbnail = ctk.CTkLabel(frame_kanan, text="Tidak ada\npreview", width=180, height=240, fg_color="#333333", corner_radius=8)
    label_thumbnail.pack(padx=10, pady=5)
    
    # Enlarge preview
    btn_enlarge = ctk.CTkButton(frame_kanan, text="🔍 Perbesar", width=150, command=enlarge_preview, fg_color="#4A4D50", hover_color="#333538")
    btn_enlarge.pack(pady=(5, 10))

    # ================= Control panel =================
    frame_btn = ctk.CTkFrame(window, fg_color="transparent")
    frame_btn.pack(padx=20, pady=(0, 20), fill="x")

    btn_pilih = ctk.CTkButton(frame_btn, text="Pilih File", command=choose_file, width=130)
    btn_pilih.pack(side="left", padx=5)

    btn_clear = ctk.CTkButton(frame_btn, text="Hapus Semua", command=delete_list, width=130, 
                              fg_color="#C8504B", hover_color="#8E3533")
    btn_clear.pack(side="left", padx=5)

    btn_gabung = ctk.CTkButton(frame_btn, text="Gabungkan!", command=execute_merger, width=130, 
                               fg_color="#28A745", hover_color="#218838")
    btn_gabung.pack(side="right", padx=5)