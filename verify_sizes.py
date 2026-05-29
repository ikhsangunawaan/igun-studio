import os
import sys

def verify_images(directory="images", max_size_kb=90):
    max_size_bytes = max_size_kb * 1024
    success = True
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return False
        
    print(f"Verifying all images in '{directory}' are under {max_size_kb} KB...")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            size = os.path.getsize(filepath)
            status = "OK" if size <= max_size_bytes else "FAIL (TOO LARGE)"
            print(f"- {filename}: {size/1024:.2f} KB [{status}]")
            if size > max_size_bytes:
                success = False
                
    if success:
        print("Success: All images are optimized and under 90 KB limit!")
    else:
        print("Error: One or more images exceed the 90 KB limit.")
        
    return success

if __name__ == "__main__":
    if not verify_images():
        sys.exit(1)
    sys.exit(0)
