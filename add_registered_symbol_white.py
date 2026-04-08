from PIL import Image, ImageDraw, ImageFont
import os

def add_registered_symbol_white(input_path, output_path):
    # Load white logo
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # Expand canvas
    new_width = width + 20
    new_img = Image.new("RGBA", (new_width, height), (0, 0, 0, 0))
    new_img.paste(img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    symbol = "®"
    pos_x = width - 5
    pos_y = 15
    
    # Draw it in PURE WHITE for this version
    white_color = (255, 255, 255, 255)
    
    draw.text((pos_x, pos_y), symbol, fill=white_color, font=font)
    
    # Autocrop
    bbox = new_img.getbbox()
    if bbox:
        new_img = new_img.crop(bbox)
        
    new_img.save(output_path, "PNG")
    print(f"White registered logo created: {output_path} (Size: {new_img.size})")

if __name__ == "__main__":
    src = r"C:\Users\david\Desktop\Projects-Antigravity\Inmobiliaria\logos_corporativos\weperty_logo_blanco_final.png"
    out = r"C:\Users\david\Desktop\Projects-Antigravity\Inmobiliaria\logos_corporativos\weperty_logo_blanco_final_registrado.png"
    add_registered_symbol_white(src, out)
