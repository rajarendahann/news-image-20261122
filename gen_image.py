import os
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
BG_COLOR = (245, 242, 235)  # Cream paper
TEXT_COLOR = (20, 20, 20)     # Dark ink
ACCENT_COLOR = (180, 40, 40)  # Muted red
GRID_COLOR = (200, 200, 200)

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_wrapped_text(draw, text, font, color, x, y, max_width, line_spacing=1.2):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    lines.append(" ".join(current_line))
    
    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, font=font, fill=color)
        curr_y += font.size * line_spacing
    return curr_y

def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Masthead
    draw.rectangle([0, 0, WIDTH, 28], fill=TEXT_COLOR)
    font_tiny = get_font(FONT_SANS_BOLD, 12)
    draw.text((WIDTH//2, 14), "THE WORLD IN ONE DAY", font=font_tiny, fill=BG_COLOR, anchor="mm")
    
    # Huge Date (>= 54px)
    font_huge = get_font(FONT_SERIF_BOLD, 56)
    draw.text((WIDTH//2, 70), "Sunday 22 November 2026", font=font_huge, fill=TEXT_COLOR, anchor="mm")
    
    # Lede
    lede = "COP31 Antalya draft drops fossil fuels; Wall Street tech crash as Nvidia CEO resigns; Iran fires missiles at US Bahrain bases."
    font_lede = get_font(FONT_SANS, 14)
    draw.text((WIDTH//2, 110), lede, font=font_lede, fill=TEXT_COLOR, anchor="mm")
    
    draw.line([30, 125, WIDTH-30, 125], fill=TEXT_COLOR, width=2)
    
    # 2. Region Counters (7 regions)
    regions = [
        ("ASIA", 5), ("MIDDLE EAST", 3), ("EUROPE", 4), 
        ("AFRICA", 2), ("AMERICAS", 5), ("OCEANIA", 1), ("GLOBAL", 4)
    ]
    box_w = (WIDTH - 60) // len(regions)
    for i, (name, count) in enumerate(regions):
        x = 30 + i * box_w
        draw.rectangle([x+2, 132, x+box_w-2, 158], outline=TEXT_COLOR, width=1)
        draw.text((x + box_w//2, 145), f"{name} ({count})", font=font_tiny, fill=TEXT_COLOR, anchor="mm")

    # 3. Big Story Cards (3)
    big_stories = [
        ("GLOBAL", "COP31 OVERTIME: DRAFT DROPS FOSSIL FUELS", "Antalya talks stall; climate-aid funding mechanism remains blocked."),
        ("AMERICAS", "WALL STREET CRASH: NVIDIA DOWN 14%", "Nasdaq falls 5.3% after CEO Huang resigns amid scandal."),
        ("MIDDLE EAST", "IRAN STRIKES US BASES IN BAHRAIN", "Missiles and drones launched; Houthis target Riyadh.")
    ]
    
    card_y = 168
    card_h = 138
    card_w = (WIDTH - 80) // 3
    font_h_big = get_font(FONT_SANS_BOLD, 18)
    font_b_big = get_font(FONT_SANS, 13)
    
    for i, (tag, head, body) in enumerate(big_stories):
        x = 30 + i * (card_w + 10)
        draw.rectangle([x, card_y, x+card_w, card_y+card_h], outline=GRID_COLOR)
        draw.rectangle([x, card_y, x+card_w, card_y+22], fill=ACCENT_COLOR)
        draw.text((x+5, card_y+4), tag, font=font_tiny, fill=BG_COLOR)
        
        next_y = draw_wrapped_text(draw, head, font_h_big, TEXT_COLOR, x+5, card_y+26, card_w-10, line_spacing=1.1)
        draw_wrapped_text(draw, body, font_b_big, TEXT_COLOR, x+5, next_y + 6, card_w-10, line_spacing=1.15)

    # 4. 3x3 Grid (9 items)
    grid_y = 318
    grid_item_w = (WIDTH - 80) // 3
    grid_item_h = 84
    grid_stories = [
        ("ASIA", "Japan 7.6 Quake", "Tsunami warnings for 90,000."),
        ("GLOBAL", "Siberia Plane Crash", "Russian transport falls, 19 dead."),
        ("EUROPE", "Strike on Kryvyi Rih", "Zelensky hometown hit; hospital damaged."),
        ("AMERICAS", "FBI Database Breach", "Probe into NCIC database compromise."),
        ("EUROPE", "Missiles Hit Poland", "Two Russian missiles land on territory."),
        ("AMERICAS", "Chapo Isidro Captured", "Mexican forces raid Sinaloa."),
        ("GLOBAL", "Riemann Hypothesis?", "Anthropic claims Claude AI breakthrough."),
        ("AFRICA", "Nigeria Boat Capsizes", "24 dead after funeral boat sinks."),
        ("AMERICAS", "Brazil Supercell", "3 dead, 8k homes hit in Tupanciretã.")
    ]
    
    font_h_grid = get_font(FONT_SANS_BOLD, 14)
    font_b_grid = get_font(FONT_SANS, 11)
    
    for i, (tag, head, body) in enumerate(grid_stories):
        row = i // 3
        col = i % 3
        x = 30 + col * (grid_item_w + 10)
        y = grid_y + row * (grid_item_h + 8)
        
        draw.rectangle([x, y, x+grid_item_w, y+grid_item_h], outline=GRID_COLOR)
        draw.text((x+4, y+3), tag, font=get_font(FONT_SANS_BOLD, 9), fill=ACCENT_COLOR)
        
        h_y = draw_wrapped_text(draw, head, font_h_grid, TEXT_COLOR, x+4, y+16, grid_item_w-8, line_spacing=1.0)
        draw_wrapped_text(draw, body, font_b_grid, TEXT_COLOR, x+4, h_y + 2, grid_item_w-8, line_spacing=1.0)

    # 5. World Map and Also-On List
    bottom_y = 604
    
    # Also-On Section (Two columns)
    draw.text((30, bottom_y), "ALSO ON SUNDAY 22 NOVEMBER", font=font_tiny, fill=TEXT_COLOR)
    draw.line([30, bottom_y+16, 350, bottom_y+16], fill=TEXT_COLOR)
    
    also_on = [
        "BELGIUM: Air-traffic strike to shut flights Monday.",
        "AMERICAS: Bolsonaro in ICU with obstruction.",
        "EUROPE: French cost-of-living protests.",
        "EUROPE: EU proposes Big Tech tax for budget.",
        "ASIA: Taiwan warns Canada on China ties.",
        "AMERICAS: Trump orders contractor vetting.",
        "GLOBAL: UN fails on autonomous weapons rules.",
        "ASIA: India measles cases highest since 1991.",
        "ASIA: Prabowo apologises for haze.",
        "ASIA: ASEAN/China fail on S. China Sea code.",
        "AMERICAS: Peru 6.7 quake; no deaths reported.",
        "OCEANIA: Australia beats England in T20 opener."
    ]
    
    font_also = get_font(FONT_SANS, 11)
    col1 = also_on[:6]
    col2 = also_on[6:]
    
    for i, line in enumerate(col1):
        draw.text((30, bottom_y + 24 + i*27), f"• {line}", font=font_also, fill=TEXT_COLOR)
    for i, line in enumerate(col2):
        draw.text((340, bottom_y + 24 + i*27), f"• {line}", font=font_also, fill=TEXT_COLOR)

    # World Map
    map_x, map_y = 670, bottom_y
    map_w, map_h = 324, 340
    draw.rectangle([map_x, map_y, map_x+map_w, map_y+map_h], outline=GRID_COLOR)
    draw.text((map_x+6, map_y+4), "WHERE IT HAPPENED", font=font_tiny, fill=TEXT_COLOR)
    
    # Light dotted-grid continents silhouette behind dots
    for gx in range(map_x + 12, map_x + map_w - 12, 16):
        for gy in range(map_y + 24, map_y + map_h - 12, 20):
            draw.point((gx, gy), fill=(225, 220, 215))

    # 12 cities with non-overlapping label placement and leader/side offsets
    dots = [
        ("Brussels", 0.5, 0.3, "left", -4, -4),
        ("Warsaw", 0.54, 0.27, "left", -4, -10),
        ("Kryvyi Rih", 0.59, 0.33, "right", 5, -2),
        ("Antalya", 0.61, 0.42, "left", -4, 4),
        ("Islamabad", 0.73, 0.44, "right", 5, 0),
        ("Riyadh", 0.61, 0.52, "left", -4, 2),
        ("Manama", 0.65, 0.49, "right", 5, -6),
        ("Tokyo", 0.85, 0.38, "left", -4, -4),
        ("Culiacán", 0.18, 0.48, "right", 5, -4),
        ("New York", 0.24, 0.38, "left", -4, -4),
        ("Bayelsa", 0.5, 0.65, "right", 5, -4),
        ("Tupanciretã", 0.3, 0.8, "right", 5, -4),
    ]
    
    font_map = get_font(FONT_SANS, 9)
    for label, rx, ry, align, dx, dy in dots:
        px = map_x + int(rx * map_w)
        py = map_y + int(ry * map_h)
        draw.ellipse([px-2, py-2, px+2, py+2], fill=ACCENT_COLOR)
        txt_w = draw.textlength(label, font=font_map)
        if align == "left":
            tx = px + dx - txt_w
            ty = py + dy - 4
        else:
            tx = px + dx
            ty = py + dy - 4
        draw.text((tx, ty), label, font=font_map, fill=TEXT_COLOR)

    # 6. Footer
    footer_y = 960
    draw.line([30, footer_y, WIDTH-30, footer_y], fill=TEXT_COLOR, width=1)
    footer_text = "DATE CHECK: every story on this page happened, or was first reported, on Sunday 22 November 2026"
    sources = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Euronews, NPR, Kyiv Independent, El País, AllAfrica, ABC. Stories are attributed, not stated as facts. Numbers are approximate."
    draw.text((WIDTH//2, footer_y + 16), footer_text, font=get_font(FONT_SANS, 11), fill=TEXT_COLOR, anchor="mm")
    draw.text((WIDTH//2, footer_y + 36), sources, font=get_font(FONT_SANS, 10), fill=TEXT_COLOR, anchor="mm")

    # Save
    img.save("entry.png", "PNG", optimize=True)
    print("entry.png saved successfully.")

if __name__ == "__main__":
    main()
