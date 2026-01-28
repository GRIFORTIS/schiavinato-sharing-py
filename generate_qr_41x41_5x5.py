import os

def create_qr_grid_v6(filename="qr_v6_grid_5x5.svg", cell_size_mm=5):
    """
    Generates a Version 6 (41x41) QR grid SVG for manual filling.
    Includes Finder Patterns and the V6 Alignment Pattern.
    Grid layout: 5x5 groups, with the last row/column being 6 units wide/tall.
    """
    version = 6
    size = 17 + (4 * version)  # 41 modules
    
    # SVG Configuration
    scale = 3.7795  # pixels per mm (approx 96 DPI)
    cell_px = cell_size_mm * scale
    margin_px = 4 * cell_px
    full_width = (size * cell_px) + (2 * margin_px)
    
    svg = [
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg width="{full_width}" height="{full_width}" viewBox="0 0 {full_width} {full_width}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="100%" height="100%" fill="white"/>',
        f'<g transform="translate({margin_px}, {margin_px})">'
    ]

    # 1. Draw the Grid
    # Pass 1: Subtle dashed lines for all cells
    svg.append(f'<g stroke="#000" stroke-width="0.5" stroke-dasharray="1,2">')
    # Vertical lines
    for i in range(size + 1):
        x = i * cell_px
        svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{size * cell_px}"/>')
    # Horizontal lines
    for i in range(size + 1):
        y = i * cell_px
        svg.append(f'<line x1="0" y1="{y}" x2="{size * cell_px}" y2="{y}"/>')
    svg.append('</g>')

    # Pass 2: Strong solid lines for groups of 5 (last group is 6)
    # Group boundaries at: 0, 5, 10, 15, 20, 25, 30, 35, 41
    group_indices = [0, 5, 10, 15, 20, 25, 30, 35, 41]
    
    svg.append(f'<g stroke="#000" stroke-width="1.5">')
    # Vertical group lines
    for i in group_indices:
        x = i * cell_px
        svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{size * cell_px}"/>')
    # Horizontal group lines
    for i in group_indices:
        y = i * cell_px
        svg.append(f'<line x1="0" y1="{y}" x2="{size * cell_px}" y2="{y}"/>')
    svg.append('</g>')

    # Helper to draw a filled rectangle (x, y, w, h in modules)
    def rect(x, y, w, h, color="black"):
        return f'<rect x="{x * cell_px}" y="{y * cell_px}" width="{w * cell_px}" height="{h * cell_px}" fill="{color}"/>'

    # Helper to draw a Finder Pattern (7x7)
    def draw_finder(x, y):
        s = []
        s.append(rect(x, y, 7, 7, "black"))       # Outer box
        s.append(rect(x+1, y+1, 5, 5, "white"))   # White ring
        s.append(rect(x+2, y+2, 3, 3, "black"))   # Inner box
        return s

    # Helper to draw Alignment Pattern (5x5)
    def draw_alignment(x, y):
        # x, y is the top-left corner of the 5x5 area
        s = []
        s.append(rect(x, y, 5, 5, "black"))       # Outer box
        s.append(rect(x+1, y+1, 3, 3, "white"))   # White ring
        s.append(rect(x+2, y+2, 1, 1, "black"))   # Center dot
        return s

    # 2. Draw Fixed Patterns
    # Finder Patterns (Top-Left, Top-Right, Bottom-Left)
    svg.extend(draw_finder(0, 0))
    svg.extend(draw_finder(size - 7, 0))
    svg.extend(draw_finder(0, size - 7))

    # Alignment Pattern for V6 (Center at 34,34 -> Top-Left at 32,32)
    # V6 alignment coords are 6, 34. 
    # (6,6), (6,34), (34,6) are occupied by finders. (34,34) is the only free one.
    svg.extend(draw_alignment(32, 32))

    # 3. Timing Patterns (connecting finders)
    # Horizontal (row 6)
    for c in range(8, size - 8):
        if c % 2 == 0:
            svg.append(rect(c, 6, 1, 1, "black"))
            
    # Vertical (col 6)
    for r in range(8, size - 8):
        if r % 2 == 0:
            svg.append(rect(6, r, 1, 1, "black"))

    svg.append('</g>')
    svg.append('</svg>')

    with open(filename, "w") as f:
        f.write("\n".join(svg))
    
    print(f"Generated {filename} (Size: {size}x{size}, Cell: {cell_size_mm}mm)")

if __name__ == "__main__":
    create_qr_grid_v6()
