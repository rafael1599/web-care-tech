import os
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# Configuration
BRAND_COLOR_RGB = (59, 130, 246)  # Electric Blue #3B82F6
BRAND_COLOR_DARK = (30, 64, 175)  # Darker Blue #1E40AF
BG_COLOR_START = (15, 23, 42)     # Slate 900
BG_COLOR_END = (0, 0, 0)          # Black

OUTPUT_DIR = r"c:\Users\rafis\Documents\Antigravity\Web-automation-business1\images"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    center_x, center_y = width / 2, height / 2
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = dist / max_dist
            mask_data.append(int(255 * ratio))
            
    mask.putdata(mask_data)
    return Image.composite(top, base, mask)

def draw_tech_grid(draw, width, height, step=50):
    for x in range(0, width, step):
        opacity = 30 if x % (step*4) == 0 else 10
        draw.line([(x, 0), (x, height)], fill=(BRAND_COLOR_RGB[0], BRAND_COLOR_RGB[1], BRAND_COLOR_RGB[2], opacity), width=1)
    
    for y in range(0, height, step):
        opacity = 30 if y % (step*4) == 0 else 10
        draw.line([(0, y), (width, y)], fill=(BRAND_COLOR_RGB[0], BRAND_COLOR_RGB[1], BRAND_COLOR_RGB[2], opacity), width=1)

def add_glowing_element(img, x, y, radius, color):
    # Create a blurred circle on a separate layer
    glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    
    # Outer glow (large blur)
    draw.ellipse((x - radius*1.5, y - radius*1.5, x + radius*1.5, y + radius*1.5), fill=(color[0], color[1], color[2], 50))
    glow = glow.filter(ImageFilter.GaussianBlur(radius/2))
    
    # Inner glow
    glow2 = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(glow2)
    draw2.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(color[0], color[1], color[2], 100))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius/4))
    
    # Core
    core = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_core = ImageDraw.Draw(core)
    draw_core.ellipse((x - radius*0.8, y - radius*0.8, x + radius*0.8, y + radius*0.8), outline=(255, 255, 255, 150), width=2)

    # Composite
    img.paste(glow, (0, 0), glow)
    img.paste(glow2, (0, 0), glow2)
    img.paste(core, (0, 0), core)

def create_placeholder(filename, width, height, text, is_logo=False):
    # 1. Background Gradient
    img = create_gradient(width, height, BG_COLOR_START, BG_COLOR_END)
    img = img.convert("RGBA")
    
    # 2. Tech Grid
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    draw_tech_grid(draw, width, height, step=40 if width < 600 else 60)
    img = Image.alpha_composite(img, overlay)
    
    # 3. Central Element
    cx, cy = width // 2, height // 2
    if is_logo:
        add_glowing_element(img, cx, cy, min(width, height) // 3, BRAND_COLOR_RGB)
    else:
        # Random glowing nodes for services
        for _ in range(3):
            rx = random.randint(width//4, width*3//4)
            ry = random.randint(height//4, height*3//4)
            add_glowing_element(img, rx, ry, random.randint(20, 60), BRAND_COLOR_DARK)
        
        # Main center glow
        add_glowing_element(img, cx, cy, 100, BRAND_COLOR_RGB)

    # 4. Text
    if text:
        draw = ImageDraw.Draw(img)
        try:
            # Try to load a reasonable font
            font_size = 60 if is_logo else 40
            font = ImageFont.truetype("arial.ttf", size=font_size)
        except IOError:
            font = ImageFont.load_default()
            
        # Draw text with shadow
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        tx = (width - text_w) / 2
        ty = (height - text_h) / 2
        
        # Shadow
        draw.text((tx+2, ty+2), text, fill=(0, 0, 0, 180), font=font)
        # Main text
        draw.text((tx, ty), text, fill=(255, 255, 255), font=font)

    # Save
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"Generated enhanced placeholder: {filepath}")

# Main execution
if __name__ == "__main__":
    print("Generating enhanced placeholders...")
    
    # Logo
    create_placeholder("logo.png", 512, 512, "Care Tech", is_logo=True)
    
    # Hero
    create_placeholder("hero_visual.png", 1200, 1200, "Future of Health\nAutomation", is_logo=False)

    # Services
    services = [
        ("service_1.png", "RCM Optimization"),
        ("service_2.png", "API Integration"),
        ("service_3.png", "Smart Claims AI"),
        ("service_4.png", "Eligibility Bots"),
        ("service_5.png", "Medical OCR"),
        ("service_6.png", "Cashflow Analytics")
    ]
    
    for filename, title in services:
        create_placeholder(filename, 800, 600, title)
        
    # Extras
    create_placeholder("showcase_1.png", 800, 600, "Dashboard View")
    create_placeholder("showcase_2.png", 800, 600, "Mobile App")
    
    print("Done!")
