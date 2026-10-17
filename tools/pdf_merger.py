from pypdf import PdfWriter

def pdf_merger_process(file_list, file_output):
    """Menggabungkan daftar file PDF menjadi satu file output."""
    merger = PdfWriter()
    try:
        for pdf in file_list:
            merger.append(pdf)
        merger.write(file_output)
        return True, "File PDF berhasil digabungkan!"
    except Exception as e:
        return False, str(e)
    finally:
        merger.close()