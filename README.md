# ⚡ Ultra Resolution Studio v7.0

### *A Public Utility by NoteMate*

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch)
![Powered By](https://img.shields.io/badge/Powered_By-NoteMate_AI-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg?style=for-the-badge)

**Ultra Resolution Studio** is a powerful, offline desktop application released publicly by **NoteMate**. Just as major tech giants release standalone tools for the community, NoteMate is making its internal image restoration engine available to everyone.

This tool leverages state-of-the-art Deep Learning models (**Real-ESRGAN** & **GFPGAN**) to upscale and restore low-quality images. Unlike standard tools, it hallucinates missing details to convert blurry photos into crisp **4K, 8K, or even 16K** masterpieces.

---

## 🚀 Features

* **🧠 Hybrid AI Engine:** Combines `Real-ESRGAN` for textures and `GFPGAN` for blind face restoration.
* **⚡ Smart Resolution Lock:**
    * **Fast ⚡ (1080p):** Instant results for social media.
    * **Balance ⚖️ (2K):** Perfect for desktop viewing.
    * **Best 💎 (4K):** Print-grade quality.
    * **Ultra 🌟 (8K):** Professional design work.
    * **Ultimate 🔥 (16K):** Extreme detail reconstruction (God Mode).
* **🎨 Professional GUI:** Built with `CustomTkinter` for a modern, dark-themed experience.
* **🔍 Advanced Viewer:** "Google Maps-style" Zoom & Pan with synchronized **Original vs. Enhanced** comparison (Hold Spacebar).
* **🔒 100% Offline:** No data is uploaded to the cloud. Everything runs locally on your CPU/GPU.
* **🛠️ Crash-Proof:** Implemented dynamic tiling and "Resolution Locking" to prevent OOM (Out of Memory) errors on low-end PCs.

---

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.10+**
* **Git**
* **NVIDIA GPU** (Optional, but recommended for speed)

### 1. Clone the Repository
```bash
git clone [https://github.com/abhi5511/Image_Inhancer.git](https://github.com/abhi5511/Image_Inhancer.git)
cd Image_Inhancer
2. Create Virtual Environment (Recommended)
Bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Download AI Models
We have a dedicated script to fetch the required .pth weights from Hugging Face automatically.

Bash

python setup_models.py
5. Run the App
Bash

python modern_gui.py
🎮 Usage Guide
Load Image: Click "Load Image" to select any JPG/PNG/WEBP file.

Select Target:

General: For landscapes, art, and objects.

Face Restoration: Special mode for portraits (NoteMate Engine).

Old Photo: Aggressive restoration for damaged vintage photos.

Select Quality:

Choose Fast for speed or Ultimate for max detail.

Ignite Render: Click the button and wait for the magic.

Compare: Hold Spacebar or Right Click on the image to see the Before/After difference instantly.

🏗️ Tech Stack
Frontend: CustomTkinter (Python)

Backend: PyTorch, OpenCV, NumPy

AI Models:

Real-ESRGAN (Upscaling)

GFPGAN (Face Restoration)

Packaging: PyInstaller & Inno Setup

🤝 Contributing
Contributions are welcome! This is an open initiative by NoteMate.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is dedicated to the public domain under the Creative Commons Zero v1.0 Universal (CC0 1.0) license. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. See LICENSE for more information.

Made with ❤️ by Abhi (Team NoteMate)