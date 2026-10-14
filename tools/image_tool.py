from PIL import Image

def convert_image_process(original_filepath, new_filepath):
    try:
        img = Image.open(original_filepath)
        
        # Validate for transparant bg
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
            
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))
            
            img = Image.alpha_composite(background, img)
            
            img = img.convert('RGB')
            
        elif new_filepath.lower().endswith(('.jpg', '.jpeg', '.jfif')) and img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.save(new_filepath)
        return True, "Gambar berhasil dikonversi!"
    except Exception as e:
        return False, f"Gagal mengonversi: {e}"