import customtkinter as ctk
from tkinter import filedialog, messagebox, Canvas
from PIL import Image, ImageTk
import threading
import os
import traceback
from ai_engine import AIEngine

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ProfessionalImageViewer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.src_img = None; self.tk_img = None
        self.img_original_full = None; self.img_enhanced_full = None
        self.scale = 1.0; self.offset_x = 0.0; self.offset_y = 0.0
        
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_move)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<Button-4>", self.on_zoom); self.canvas.bind("<Button-5>", self.on_zoom)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<KeyPress-space>", self.show_original_view)
        self.canvas.bind("<KeyRelease-space>", self.show_enhanced_view)
        self.canvas.focus_set()

    def load_image(self, path):
        self.img_original_full = Image.open(path).convert("RGB")
        self.img_enhanced_full = None
        self.src_img = self.img_original_full
        self.fit_to_screen()

    def load_enhanced(self, path):
        self.img_enhanced_full = Image.open(path).convert("RGB")
        self.src_img = self.img_enhanced_full
        self.redraw()

    def fit_to_screen(self):
        if not self.src_img: return
        cw = self.canvas.winfo_width(); ch = self.canvas.winfo_height()
        if cw < 10: cw, ch = 600, 400
        iw, ih = self.src_img.size
        self.scale = min(cw/iw, ch/ih) * 0.9
        self.offset_x = (cw - iw * self.scale) / 2; self.offset_y = (ch - ih * self.scale) / 2
        self.redraw()

    def on_resize(self, event):
        if self.src_img: self.redraw()

    def redraw(self):
        if not self.src_img: return
        cw = self.canvas.winfo_width(); ch = self.canvas.winfo_height()
        draw_scale = self.scale
        if self.img_original_full and self.src_img == self.img_enhanced_full:
            rel_factor = self.img_enhanced_full.width / self.img_original_full.width
            draw_scale = self.scale / rel_factor
            
        left = -self.offset_x / draw_scale; top = -self.offset_y / draw_scale
        right = (cw - self.offset_x) / draw_scale; bottom = (ch - self.offset_y) / draw_scale
        
        iw, ih = self.src_img.size
        new_w = int(iw * draw_scale); new_h = int(ih * draw_scale)
        if new_w < 1 or new_h < 1: return

        try:
            if new_w > cw * 2 or new_h > ch * 2:
                crop_box = (max(0, left), max(0, top), min(iw, right), min(ih, bottom))
                crop_w, crop_h = crop_box[2] - crop_box[0], crop_box[3] - crop_box[1]
                if crop_w <= 0 or crop_h <= 0: return
                cropped = self.src_img.crop(crop_box)
                final_w = int(crop_w * draw_scale); final_h = int(crop_h * draw_scale)
                resample = Image.Resampling.NEAREST if draw_scale < 1.0 else Image.Resampling.BILINEAR
                disp = cropped.resize((final_w, final_h), resample)
                dest_x = max(0, self.offset_x + (crop_box[0] * draw_scale)); dest_y = max(0, self.offset_y + (crop_box[1] * draw_scale))
            else:
                disp = self.src_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
                dest_x, dest_y = self.offset_x, self.offset_y
            
            self.tk_img = ImageTk.PhotoImage(disp)
            self.canvas.delete("all")
            self.draw_grid(cw, ch)
            self.canvas.create_image(dest_x, dest_y, anchor="nw", image=self.tk_img)
        except: pass

    def draw_grid(self, w, h):
        self.canvas.create_line(w/2, 0, w/2, h, fill="#333", dash=(4, 4))
        self.canvas.create_line(0, h/2, w, h/2, fill="#333", dash=(4, 4))
    
    def on_drag_start(self, event): self.canvas.scan_mark(event.x, event.y); self.last_drag_x = event.x; self.last_drag_y = event.y
    def on_drag_move(self, event):
        dx = event.x - self.last_drag_x; dy = event.y - self.last_drag_y
        self.offset_x += dx; self.offset_y += dy
        self.last_drag_x = event.x; self.last_drag_y = event.y
        self.redraw()
    def on_zoom(self, event):
        if not self.src_img: return
        factor = 1.15 if (event.num == 4 or event.delta > 0) else 0.85
        mx, my = event.x, event.y
        new_scale = self.scale * factor
        if new_scale < 0.05: new_scale = 0.05
        if new_scale > 50.0: new_scale = 50.0
        self.offset_x = mx - (mx - self.offset_x) * (new_scale / self.scale)
        self.offset_y = my - (my - self.offset_y) * (new_scale / self.scale)
        self.scale = new_scale
        self.redraw()
    def show_original_view(self, event=None):
        if self.img_original_full: self.src_img = self.img_original_full; self.redraw()
    def show_enhanced_view(self, event=None):
        if self.img_enhanced_full: self.src_img = self.img_enhanced_full; self.redraw()


class UltimateEnhancerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ULTRA RESOLUTION STUDIO v7.0 (Open Source)")
        self.geometry("1280x800")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.file_path = None; self.setup_sidebar()
        self.viewer = ProfessionalImageViewer(self)
        self.viewer.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def setup_sidebar(self):
        sb = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#111")
        sb.grid(row=0, column=0, sticky="nsew"); sb.grid_rowconfigure(10, weight=1)
        ctk.CTkLabel(sb, text="AI WORKSTATION", font=("Impact", 26), text_color="#00a8ff").grid(row=0, column=0, pady=25)
        
        self.btn_open = ctk.CTkButton(sb, text="📂 LOAD IMAGE", command=self.open_img, fg_color="#2f3640", height=40, font=("Arial", 12, "bold"))
        self.btn_open.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(sb, text="AI MODEL TARGET", font=("Arial", 11, "bold"), text_color="gray").grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")
        self.cat_var = ctk.StringVar(value="General Enhancement")
        self.cat_menu = ctk.CTkOptionMenu(sb, variable=self.cat_var, fg_color="#2c3e50", values=["General Enhancement", "Face Restoration (Portrait)", "Old Photo Repair", "Denoise & Fix", "Ultra Sharp"])
        self.cat_menu.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(sb, text="QUALITY & SPEED", font=("Arial", 11, "bold"), text_color="gray").grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")
        self.res_var = ctk.StringVar(value="balance")
        self.frame_res = ctk.CTkFrame(sb, fg_color="transparent")
        self.frame_res.grid(row=5, column=0, padx=10, sticky="ew")
        ctk.CTkRadioButton(self.frame_res, text="Fast ⚡", variable=self.res_var, value="fast", fg_color="#2ecc71").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(self.frame_res, text="Balance ⚖️", variable=self.res_var, value="balance", fg_color="#3498db").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(self.frame_res, text="Best 💎", variable=self.res_var, value="best", fg_color="#9b59b6").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(self.frame_res, text="Ultra 🌟", variable=self.res_var, value="ultra", fg_color="#f1c40f").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(self.frame_res, text="Ultimate (16K) 🔥", variable=self.res_var, value="ultimate", fg_color="#e74c3c").grid(row=2, column=0, columnspan=2, padx=10, pady=(5,0), sticky="ew")

        self.btn_run = ctk.CTkButton(sb, text="⚡ IGNITE RENDER", command=self.run_thread, height=60, fg_color="#27ae60", font=("Arial", 16, "bold"), state="disabled")
        self.btn_run.grid(row=7, column=0, padx=20, pady=40, sticky="ew")
        
        self.progress = ctk.CTkProgressBar(sb, progress_color="#00a8ff")
        self.progress.grid(row=8, column=0, padx=20, sticky="ew"); self.progress.set(0)
        self.lbl_status = ctk.CTkLabel(sb, text="Ready", font=("Consolas", 10))
        self.lbl_status.grid(row=9, column=0, pady=10)
        ctk.CTkLabel(sb, text="[ SPACEBAR ] to Compare", text_color="#fbc531", font=("Arial", 12, "bold")).grid(row=11, column=0, pady=20)

    def open_img(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg *.webp *.bmp")])
        if path: self.file_path = path; self.viewer.load_image(path); self.btn_run.configure(state="normal"); self.lbl_status.configure(text="Image Loaded"); self.progress.set(0)

    def update_ui(self, msg, prog): self.lbl_status.configure(text=f"{msg} ({prog}%)"); self.progress.set(prog/100)
    def run_thread(self): self.btn_run.configure(state="disabled", text="RENDERING...", fg_color="#c0392b"); threading.Thread(target=self.process).start()

    def process(self):
        try:
            out_path = os.path.splitext(self.file_path)[0] + f"_{self.res_var.get()}.png"
            cat_map = {"General Enhancement": "general", "Face Restoration (Portrait)": "face", "Old Photo Repair": "old_photo", "Denoise & Fix": "denoise", "Ultra Sharp": "ultra_sharp"}
            
            engine = AIEngine(update_callback=self.update_ui)
            engine.process_pipeline(self.file_path, out_path, category=cat_map[self.cat_var.get()], resolution=self.res_var.get())
            
            self.viewer.load_enhanced(out_path)
            self.lbl_status.configure(text="✅ Render Complete")
            self.btn_run.configure(state="normal", text="⚡ IGNITE RENDER", fg_color="#27ae60")
            self.viewer.canvas.focus_set()
            
        except Exception as e:
            self.lbl_status.configure(text="❌ Error Occurred")
            full_error = traceback.format_exc()
            messagebox.showerror("Render Failed", f"Error Details:\n{str(e)}\n\nFull Traceback:\n{full_error}")
            self.btn_run.configure(state="normal", text="⚡ IGNITE RENDER", fg_color="#27ae60")

if __name__ == "__main__":
    app = UltimateEnhancerApp()
    app.mainloop()