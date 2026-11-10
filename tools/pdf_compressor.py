import pymupdf
import os

def compress_pdf_process(input_path, output_path, level="Medium"):
    try:
        if level == "Fast":
            doc = pymupdf.open(input_path)
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            
        else:
            target_dpi = 144 if level == "Medium" else 72
            
            original_doc = pymupdf.open(input_path)
            compressed_doc = pymupdf.open() 
            
            for page in original_doc:
                pix = page.get_pixmap(dpi=target_dpi)
                new_page = compressed_doc.new_page(width=page.rect.width, height=page.rect.height)
                new_page.insert_image(page.rect, stream=pix.tobytes("jpeg"))
                
            compressed_doc.save(output_path, garbage=4, deflate=True)
            original_doc.close()
            compressed_doc.close()
            
        original_size = os.path.getsize(input_path) / 1024 
        new_size = os.path.getsize(output_path) / 1024
        
        if original_size > 0:
            percent_saved = ((original_size - new_size) / original_size) * 100
        else:
            percent_saved = 0
        
        message = (f"{level} Compression successful!\n"
                   f"Original size: {original_size:.2f} KB\n"
                   f"New size: {new_size:.2f} KB\n"
                   f"Saved: {percent_saved:.1f}%")
                   
        return True, message
        
    except Exception as e:
        return False, f"Compression failed: {e}"