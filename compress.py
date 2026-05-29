import os
import sys
from PIL import Image

def compress_image(input_path, output_path, max_size_kb=90):
    max_size_bytes = max_size_kb * 1024
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return False
        
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if it's RGBA/P
            if img.mode in ("RGBA", "P"):
                # Create a white background
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    bg.paste(img, mask=img.split()[3])
                else:
                    bg.paste(img)
                img = bg
            else:
                img = img.convert("RGB")
            
            # Start compressing
            quality = 85
            # Resize if dimensions are excessively large to save space
            width, height = img.size
            if width > 1200 or height > 1200:
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                print(f"Resized image from {width}x{height} to {img.width}x{img.height}")
            
            # Binary search or decrement quality until size < 90KB
            while quality > 10:
                img.save(output_path, "JPEG", quality=quality, optimize=True)
                size = os.path.getsize(output_path)
                if size <= max_size_bytes:
                    print(f"Compressed {os.path.basename(input_path)} -> {os.path.basename(output_path)}: {size/1024:.2f} KB (quality={quality})")
                    return True
                quality -= 5
                
            # If still larger, downscale dimensions further
            scale = 0.8
            while scale > 0.1:
                w, h = int(img.width * scale), int(img.height * scale)
                resized_img = img.resize((w, h), Image.Resampling.LANCZOS)
                quality = 70
                while quality > 10:
                    resized_img.save(output_path, "JPEG", quality=quality, optimize=True)
                    size = os.path.getsize(output_path)
                    if size <= max_size_bytes:
                        print(f"Resized & Compressed {os.path.basename(input_path)} -> {os.path.basename(output_path)}: {size/1024:.2f} KB (scale={scale}, quality={quality})")
                        return True
                    quality -= 5
                scale -= 0.1
                
            print(f"Warning: Could not compress {input_path} under {max_size_kb} KB.")
            return False
            
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compress.py <input_path> <output_path>")
        sys.exit(1)
    compress_image(sys.argv[1], sys.argv[2])
