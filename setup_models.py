import os
import requests

def download_file(url, filename):
    print(f"⬇️ Downloading: {filename} from Hugging Face...")
    try:
        # Stream=True zaroori hai badi files ke liye
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Download Complete: {filename}")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {str(e)}")
        # Agar download fail ho jaye to corrupt file delete kar do
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    # Weights folder banao agar nahi hai
    if not os.path.exists('weights'):
        os.makedirs('weights')
        
    # --- HUGGING FACE DIRECT LINKS (Fast & Reliable) ---
    models = {
        # Real-ESRGAN Model (approx 64MB)
        "weights/RealESRGAN_x4plus.pth": "https://huggingface.co/lllyasviel/Annotators/resolve/main/RealESRGAN_x4plus.pth",
        
        # GFPGAN Face Model (approx 332MB)
        "weights/GFPGANv1.4.pth": "https://huggingface.co/gmk123/GFPGAN/resolve/main/GFPGANv1.4.pth"
    }
    
    print("🔍 Checking AI Models...")
    for path, url in models.items():
        if not os.path.exists(path):
            download_file(url, path)
        else:
            # Check file size to ensure it's not a corrupted 0kb file
            if os.path.getsize(path) < 1024: # Less than 1KB means corrupted
                print(f"⚠️ Corrupted file found: {path}. Re-downloading...")
                os.remove(path)
                download_file(url, path)
            else:
                print(f"⚡ Found existing: {path}")
            
    print("\n🎉 Setup Complete! Ab 'python modern_gui.py' chala.")