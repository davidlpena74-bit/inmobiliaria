from PIL import Image, ImageDraw, ImageFont
import os

def add_registered_symbol(input_path, output_path):
    # Load logo
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    # We will expand the canvas slightly to the right for the ®
    new_width = width + 20
    new_img = Image.new("RGBA", (new_width, height), (0, 0, 0, 0))
    new_img.paste(img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    
    # Try to load a font, or use default
    try:
        # On windows, Arial is usually available
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    # Text to draw
    symbol = "®"
    
    # Find position: top right of the wordmark (where the 'y' ends)
    # The 'y' ends around 'width'
    pos_x = width - 5
    pos_y = 15 # Top of the logo area
    
    # Draw it in the same color as the 'y' (which is navy blue #1e2844)
    # Actually, the 'y' part is #1e2844. 
    # I'll use that color.
    navy_color = (30, 40, 68, 255)
    
    draw.text((pos_x, pos_y), symbol, fill=navy_color, font=font)
    
    # Autocrop empty space
    bbox = new_img.getbbox()
    if bbox:
        new_img = new_img.crop(bbox)
        
    new_img.save(output_path, "PNG")
    print(f"Registered logo created: {output_path} (Size: {new_img.size})")

if __name__ == "__main__":
    src = r"C:\Users\david\Desktop\Projects-Antigravity\Inmobiliaria\logos_corporativos\weperty_logo_color_final.png"
    out = r"C:\Users\david\Desktop\Projects-Antigravity\Inmobiliaria\logos_corporativos\weperty_logo_color_final_registrado.png"
    add_registered_symbol(src, out)
