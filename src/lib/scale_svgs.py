import os
import re

# Directory containing SVG files
svg_dir = r"d:\coding\SoC\tariffs\tariffs\static\lumber-trucks\web-svg"

# SVG files to process
svg_files = [
    "mhdv_monthly_2025.svg",
    "mhdv_yearly_export_value.svg",
    "mhdv_yearly_export_weight.svg",
    "slw_monthly_2025.svg",
    "slw_quan_share_BC.svg",
    "slw_share_us_world.svg",
    "slw_yearly_export_value.svg"
]

def scale_svg(input_path, output_path, target_width):
    """Scale an SVG to a target width while maintaining aspect ratio"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the original width and height
    width_match = re.search(r'width="(\d+)"', content)
    height_match = re.search(r'height="(\d+)"', content)
    
    if not width_match or not height_match:
        print(f"Could not find dimensions in {input_path}")
        return
    
    original_width = int(width_match.group(1))
    original_height = int(height_match.group(1))
    
    # Calculate new height maintaining aspect ratio
    aspect_ratio = original_height / original_width
    new_height = int(target_width * aspect_ratio)
    
    # Replace width and height
    new_content = re.sub(r'width="\d+"', f'width="{target_width}"', content)
    new_content = re.sub(r'height="\d+"', f'height="{new_height}"', new_content)
    
    # Write the new file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Created {os.path.basename(output_path)} ({target_width}x{new_height})")

# Process each SVG file
for svg_file in svg_files:
    input_path = os.path.join(svg_dir, svg_file)
    
    if not os.path.exists(input_path):
        print(f"Skipping {svg_file} - file not found")
        continue
    
    # Get base name without extension
    base_name = os.path.splitext(svg_file)[0]
    
    # Create 720px version
    output_720 = os.path.join(svg_dir, f"{base_name}-720.svg")
    scale_svg(input_path, output_720, 720)
    
    # Create 360px version
    output_360 = os.path.join(svg_dir, f"{base_name}-360.svg")
    scale_svg(input_path, output_360, 360)

print("\nDone! Created 720px and 360px versions of all SVG files.")
