from pypdf import PdfWriter
import os

def pdf_merger_process(file_list, file_output):
    merger = PdfWriter()
    try:
        original_size = 0
        
        for pdf in file_list:
            merger.append(pdf)
            original_size += os.path.getsize(pdf) / 1024 
            
        merger.write(file_output)
        
        new_size = os.path.getsize(file_output) / 1024
        
        message = (f"Merge successful!\n"
                   f"Original size: {original_size:.2f} KB\n"
                   f"New size: {new_size:.2f} KB")
        
        return True, message
        
    except Exception as e:
        return False, f"Failed to merge PDF: {e}"
    finally:
        merger.close()