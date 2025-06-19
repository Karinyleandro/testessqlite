import os
from pathlib import Path
from PIL import Image

input_dir   = Path("backend/backend/app/static/image/livros")      
output_dir  = input_dir / "resized" 
target_size = (1748, 2560)          
keep_aspect = True                # True → mantém proporção, False → força exato

# cria a pasta de saída se ainda não existir
output_dir.mkdir(parents=True, exist_ok=True)

exts = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}

for img_path in input_dir.iterdir():
    if img_path.suffix.lower() not in exts or not img_path.is_file():
        continue  

    with Image.open(img_path) as im:
        if keep_aspect:
            # redimensiona mantendo proporção (ajusta para caber)
            im.thumbnail(target_size, Image.Resampling.LANCZOS)
        else:
            # redimensiona exatamente para target_size
            im = im.resize(target_size, Image.Resampling.LANCZOS)

        # salva com mesmo nome em subpasta
        out_path = output_dir / img_path.name
        im.save(out_path)

        print(f"✔ {img_path.name} → {out_path.name}")

print("Processamento concluído!")