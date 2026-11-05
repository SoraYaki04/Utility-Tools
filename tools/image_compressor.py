import os
from PIL import Image

def compress_image_process(input_path, output_path, compression_level="Medium"):

    try:
        if compression_level == "Extreme (Smallest Size)":
            quality_val = 30
        elif compression_level == "Medium":
            quality_val = 60
        else:
            quality_val = 85

        img = Image.open(input_path)
        
        # Convert RGBA/P to RGB if saving as JPG/JPEG to prevent errors
        if img.mode in ("RGBA", "P") and output_path.lower().endswith((".jpg", ".jpeg")):
            img = img.convert("RGB")
            
        # Save image with quality reduction and standard optimization
        img.save(output_path, quality=quality_val, optimize=True)
        
        # Calculate file sizes in Kilobytes (KB)
        original_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        saved_size = original_size - new_size
        
        message = (f"Compression successful!\n"
                   f"Original size: {original_size:.2f} KB\n"
                   f"New size: {new_size:.2f} KB\n"
                   f"Saved: {saved_size:.2f} KB")
        return True, message
        
    except Exception as e:
        return False, f"Failed to compress image: {e}"