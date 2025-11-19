import sys
import os
import cv2
import torch
import numpy as np
import warnings
import traceback

# 🛡️ TQDM Fix for EXE (Console Crash Fix)
if sys.stdout is None or sys.stderr is None:
    class DummyWriter:
        def write(self, *args, **kwargs): pass
        def flush(self): pass
    if sys.stdout is None: sys.stdout = DummyWriter()
    if sys.stderr is None: sys.stderr = DummyWriter()

# 🛡️ Monkey Patch basicsr (Scanning Fix)
try:
    import basicsr.utils
    def dummy_scandir(dir_path, suffix=None, recursive=False, full_path=False): return [] 
    basicsr.utils.scandir = dummy_scandir
except ImportError: pass

# 🚑 Torchvision Patch
try:
    import torchvision.transforms.functional as F
    sys.modules["torchvision.transforms.functional_tensor"] = F
except ImportError: pass

warnings.filterwarnings("ignore")
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from gfpgan import GFPGANer

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

MODEL_PATHS = {
    'RealESRGAN_x4': resource_path(os.path.join('weights', 'RealESRGAN_x4plus.pth')),
    'GFPGAN': resource_path(os.path.join('weights', 'GFPGANv1.4.pth'))
}

class AIEngine:
    def __init__(self, update_callback=None):
        self.update_callback = update_callback
        self.device = self._get_device()
        self._load_models()

    def _get_device(self):
        if torch.cuda.is_available(): return torch.device('cuda')
        torch.set_num_threads(os.cpu_count())
        return torch.device('cpu')

    def log(self, msg, progress=0):
        if self.update_callback: self.update_callback(msg, progress)

    def _load_models(self):
        self.log("🧠 Initializing AI Core...", 5)
        if not os.path.exists(MODEL_PATHS['RealESRGAN_x4']):
            raise FileNotFoundError(f"Missing Model: {MODEL_PATHS['RealESRGAN_x4']}")
            
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        self.upscaler = RealESRGANer(scale=4, model_path=MODEL_PATHS['RealESRGAN_x4'], model=model, tile=0, tile_pad=10, pre_pad=0, half=(self.device.type == 'cuda'), device=self.device)
        self.face_enhancer = GFPGANer(model_path=MODEL_PATHS['GFPGAN'], upscale=4, arch='clean', channel_multiplier=2, bg_upsampler=self.upscaler)
        self.log("✅ Engine Ready", 10)

    def process_pipeline(self, img_path, output_path, category='general', resolution='balance'):
        res_map = {
            'fast': ('1080p (Fast)', 1920, 200),
            'balance': ('2K (Balance)', 2560, 300),
            'best': ('4K (Best)', 3840, 300),
            'ultra': ('8K (Ultra)', 7680, 400),
            'ultimate': ('16K (Ultimate)', 15360, 400)
        }
        display_name, target_long, tile_sz = res_map.get(resolution, ('Custom', 2560, 300))
        
        self.log(f"📂 Processing ({display_name})...", 15)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None: raise ValueError("Invalid Image")
        
        h, w = img.shape[:2]
        required_input = int(target_long / 4)
        ratio = required_input / max(h, w)
        img = cv2.resize(img, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
        self.upscaler.tile_size = tile_sz

        if category == 'denoise': img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        self.log("⚙️ Neural Network Running...", 40)
        try:
            if category == 'general' or category == 'ultra_sharp': output, _ = self.upscaler.enhance(img, outscale=4)
            elif category == 'face' or category == 'denoise': _, _, output = self.face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True, weight=0.5)
            elif category == 'old_photo': _, _, output = self.face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True, weight=0.8)

            if category == 'ultra_sharp':
                gaussian = cv2.GaussianBlur(output, (0, 0), 2.0)
                output = cv2.addWeighted(output, 1.5, gaussian, -0.5, 0)

            self.log("💾 Saving...", 90)
            cv2.imwrite(output_path, output)
            self.log("✨ Done!", 100)
            return True
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", 0)
            raise RuntimeError(str(e))