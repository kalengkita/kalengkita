"""Rapikan foto produk: potong ruang transparan di sekeliling kaleng.
Pakai: taruh file ini di samping folder images, lalu jalankan:
    pip install pillow
    python rapikan_gambar.py
Hasil menimpa file di images/ (salinan asli disimpan di images/_asli/).
Logo (footer-*.webp) dilewati.
"""
import os, shutil
from PIL import Image

folder = "images"
backup = os.path.join(folder, "_asli")
os.makedirs(backup, exist_ok=True)

for name in sorted(os.listdir(folder)):
    if not name.lower().endswith(".webp") or name.startswith("footer"):
        continue
    path = os.path.join(folder, name)
    im = Image.open(path).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    if not box:
        print("lewati (kosong/tanpa transparansi):", name)
        continue
    shutil.copy2(path, os.path.join(backup, name))
    im.crop(box).save(path, "WEBP", quality=92, method=6)
    print("ok:", name, im.size, "->", (box[2]-box[0], box[3]-box[1]))
