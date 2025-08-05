import os
import base64
from lxml import etree
import cairosvg


FONT_MAP = {
	# Base fonts
	"Open Sans": "OpenSans",
	"OpenSans": "OpenSans",
	
	# Bold variants
	"Open Sans Bold": "OpenSansBold",
	"OpenSans Bold": "OpenSansBold",
	"Bold": "OpenSansBold",  # Catch-all for any font with bold weight
	
	# Italic variants
	"Open Sans Italic": "OpenSansItalic",
	"OpenSans Italic": "OpenSansItalic",
	"Italic": "OpenSansItalic",  # Catch-all for any font with italic style
	
	# Bold Italic variants
	"Open Sans Bold Italic": "OpenSansBoldItalic",
	"Open Sans BoldItalic": "OpenSansBoldItalic",
	"OpenSans Bold Italic": "OpenSansBoldItalic",
	"OpenSans BoldItalic": "OpenSansBoldItalic",
	"Bold Italic": "OpenSansBoldItalic",  # Catch-all
	"BoldItalic": "OpenSansBoldItalic"  # Catch-all
}

def get_svg_pixel_dimensions(root):
	width_attr = root.get("width", "")
	height_attr = root.get("height", "")
	viewBox = root.get("viewBox")

	def parse_length(length_str):
		if length_str.endswith("px"):
			return float(length_str[:-2])
		elif length_str.endswith("pt"):
			return float(length_str[:-2]) * 1.3333
		elif length_str.endswith("mm"):
			return float(length_str[:-2]) * 3.7795
		elif length_str.endswith("cm"):
			return float(length_str[:-2]) * 37.795
		elif length_str.endswith("in"):
			return float(length_str[:-2]) * 96
		elif length_str == "":
			return None
		else:
			return float(length_str)

	width = parse_length(width_attr)
	height = parse_length(height_attr)

	if not width or not height:
		if viewBox:
			_, _, vb_width, vb_height = viewBox.strip().split()
			width, height = float(vb_width), float(vb_height)
		else:
			raise ValueError("SVG must have width/height or viewBox")

	return width, height

def apply_font_map(root, font_map, svg_ns):

	def inline_css_styles(svg_root, ns):
		style_elements = svg_root.xpath(".//svg:style", namespaces={"svg": ns})
		css_rules = {}
		
		for style_elem in style_elements:
			if not style_elem.text:
				continue
				
			# Improved CSS parsing that handles multiple selectors
			for rule in style_elem.text.split('}'):
				rule = rule.strip()
				if not rule or '{' not in rule:
					continue
					
				# Split selectors and declarations
				selectors_part, declarations = rule.split('{', 1)
				declarations = declarations.strip().rstrip(';')
				
				# Process each selector in comma-separated list
				for selector in selectors_part.split(','):
					selector = selector.strip()
					if not selector.startswith('.'):
						continue
						
					class_name = selector[1:]
					# Append declarations to existing rules for this class
					if class_name in css_rules:
						css_rules[class_name] += '; ' + declarations
					else:
						css_rules[class_name] = declarations
		
		# Apply styles to elements
		if css_rules:
			for elem in svg_root.xpath(".//*[@class]", namespaces={"svg": ns}):
				classes = elem.get("class", "").split()
				inline_styles = []
				
				# Get existing inline style
				existing_style = elem.get("style", "")
				if existing_style:
					inline_styles.append(existing_style.rstrip(';'))
				
				# Add styles from CSS classes
				for class_name in classes:
					if class_name in css_rules:
						inline_styles.append(css_rules[class_name])
				
				# Combine all styles
				if inline_styles:
					combined_style = '; '.join(
						filter(None, [s.strip() for s in inline_styles])
					) + ';'
					elem.set("style", combined_style)
		
		# Remove style elements
		for style_elem in style_elements:
			parent = style_elem.getparent()
			if parent is not None:
				parent.remove(style_elem)
	
	# Process the SVG
	inline_css_styles(root, svg_ns)  # Inline CSS styles first


	text_nodes = root.xpath(".//svg:text | .//svg:tspan", namespaces={"svg": svg_ns})
	for node in text_nodes:
		# Store original attributes
		original_attrs = dict(node.attrib)
		
		# Parse style attribute
		style = node.get("style", "")
		style_parts = [part.strip() for part in style.split(";") if part.strip()]
		style_dict = {}
		for part in style_parts:
			if ":" in part:
				key, value = part.split(":", 1)
				style_dict[key.strip()] = value.strip()

		# Get font properties
		font_weight = original_attrs.get("font-weight", style_dict.get("font-weight", "normal")).lower()
		font_style = original_attrs.get("font-style", style_dict.get("font-style", "normal")).lower()
		current_font = style_dict.get("font-family", original_attrs.get("font-family", ""))
		
		# Clean current font name (remove quotes and get first font in stack)
		current_font = current_font.strip("'\"").split(",")[0].strip()

		# Determine font variant
		is_bold = "bold" in font_weight or "700" in font_weight
		is_italic = "italic" in font_style or "oblique" in font_style

		# Build lookup keys based ONLY on what exists in font_map
		lookup_keys = []
		if current_font:
			# Generate possible variants
			variants = []
			if is_bold and is_italic:
				variants.extend([
					f"{current_font} Bold Italic",
					f"{current_font} BoldItalic",
					"Bold Italic",
					"BoldItalic"
				])
			elif is_bold:
				variants.extend([f"{current_font} Bold", "Bold"])
			elif is_italic:
				variants.extend([f"{current_font} Italic", "Italic"])
			
			# Generate possible keys in order of preference
			for variant in variants:
				# Try full font name with variant
				lookup_keys.append(f"{current_font} {variant}" if " " not in variant else f"{current_font} {variant}")
				# Try variant alone (will only match if font_map has standalone variants)
				lookup_keys.append(variant)
			
			# Always try the base font name last
			lookup_keys.append(current_font)
		
		# Find the first matching font in font_map
		mapped_font = current_font  # default to original if no match found
		for key in lookup_keys:
			if key in font_map:
				mapped_font = font_map[key]
				break

		# Rest of the function remains the same...
		style_dict["font-family"] = mapped_font
		
		# Clean up font-weight and font-style
		if "bold" in mapped_font.lower():
			style_dict.pop("font-weight", None)
		else:
			style_dict["font-weight"] = "normal"
			
		if "italic" in mapped_font.lower():
			style_dict.pop("font-style", None)
		else:
			style_dict["font-style"] = "normal"

		# Remove Inkscape-specific attributes
		style_dict.pop("-inkscape-font-specification", None)
		original_attrs.pop("-inkscape-font-specification", None)

		# Rebuild style attribute
		updated_style = "; ".join(f"{k}: {v}" for k, v in style_dict.items() if v)
		if updated_style:
			updated_style += ";"

		# Update the node
		node.attrib.clear()
		
		# Set non-font attributes first
		for attr, value in original_attrs.items():
			if attr not in ["font-family", "font-weight", "font-style", "-inkscape-font-specification"]:
				node.set(attr, value)
		
		# Set the style attribute
		if updated_style:
			node.set("style", updated_style)
		
		# Explicitly set font-family as an attribute if it's not in style
		if "font-family" not in style_dict:
			node.set("font-family", mapped_font)


def rasterize_non_text_elements(root, width, height, svg_ns, input_svg_path):
    raster_root = etree.fromstring(etree.tostring(root))

    # Remove all text and tspan elements
    for elem in raster_root.xpath(".//svg:text | .//svg:tspan", namespaces={"svg": svg_ns}):
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)

    # Handle linked raster images: embed them as base64
    for image_elem in raster_root.xpath(".//svg:image", namespaces={"svg": svg_ns}):
        href = image_elem.get("{http://www.w3.org/1999/xlink}href") or image_elem.get("href")
        if href and not href.startswith("data:"):
            image_path = os.path.join(os.path.dirname(input_svg_path), href)
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    img_data = img_file.read()
                mime_type = "image/png" if href.lower().endswith(".png") else "image/jpeg"
                data_uri = f"data:{mime_type};base64," + base64.b64encode(img_data).decode("utf-8")
                image_elem.set("href", data_uri)
                if "{http://www.w3.org/1999/xlink}href" in image_elem.attrib:
                    del image_elem.attrib["{http://www.w3.org/1999/xlink}href"]

    # Save and convert raster-only copy
    temp_svg_path = "temp_raster.svg"
    with open(temp_svg_path, "wb") as f:
        f.write(etree.tostring(raster_root))

    # Render at 2x resolution but maintain original dimensions in output
    png_bytes = cairosvg.svg2png(
        url=temp_svg_path,
        output_width=int(width * 2),  # Double the width
        output_height=int(height * 2),  # Double the height
        dpi=192  # Double the DPI (96 * 2)
    )
    os.remove(temp_svg_path)
    return png_bytes




def keep_only_text_elements(root, svg_ns):
	# First, make a copy of the root to work with
	new_root = etree.Element(root.tag, root.attrib)
	
	# Find all text and tspan elements
	text_elements = root.xpath(".//svg:text | .//svg:tspan", namespaces={"svg": svg_ns})
	
	# For each text element, we need to preserve its entire ancestor chain
	for text_elem in text_elements:
		# Build the ancestor chain
		ancestors = []
		current = text_elem
		while current is not None and current != root:
			ancestors.append(current)
			current = current.getparent()
		
		# Now rebuild the hierarchy in our new root
		current_parent = new_root
		for ancestor in reversed(ancestors):
			# Check if this ancestor already exists in our new tree
			existing = None
			if 'id' in ancestor.attrib:
				existing = current_parent.xpath(f"./*[@id='{ancestor.attrib['id']}']")
			
			if existing:
				current_parent = existing[0]
			else:
				# Create a new element with all original attributes
				new_elem = etree.Element(ancestor.tag, ancestor.attrib)
				current_parent.append(new_elem)
				current_parent = new_elem
		
		# Finally, add the text element itself with all its attributes
		current_parent.append(etree.Element(text_elem.tag, text_elem.attrib))
		if text_elem.text:
			current_parent[-1].text = text_elem.text
	
	# Replace the original root's content with our new content
	root.clear()
	for attr, value in new_root.attrib.items():
		root.set(attr, value)
	for child in new_root:
		root.append(child)

def embed_png_as_background(root, png_bytes, width, height, svg_ns):
    png_base64 = base64.b64encode(png_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{png_base64}"

    viewBox = root.get("viewBox")
    if viewBox:
        x, y, vb_width, vb_height = map(float, viewBox.strip().split())
    else:
        x, y = 0, 0
        vb_width, vb_height = width, height

    # Create a group for the background image (behind everything)
    bg_group = etree.Element(f"{{{svg_ns}}}g", {"id": "background"})
    
    # Create image element with plain href (no namespace prefix)
    image_attrs = {
        "x": str(x),
        "y": str(y),
        "width": str(vb_width),  # Maintain original dimensions
        "height": str(vb_height),  # Maintain original dimensions
        "preserveAspectRatio": "xMidYMid meet",
        "href": data_uri
    }
    image_elem = etree.Element(f"{{{svg_ns}}}image", image_attrs)
    
    bg_group.append(image_elem)
    
    # Move all existing elements (text) to a foreground group
    fg_group = etree.Element(f"{{{svg_ns}}}g", {"id": "foreground"})
    for child in root[:]:
        fg_group.append(child)
    
    # Add groups to root (background first, then foreground)
    root.append(bg_group)
    root.append(fg_group)

def process_svg(input_svg_path, output_svg_path, font_map):
	parser = etree.XMLParser(remove_comments=True, remove_blank_text=True,  huge_tree=True)
	with open(input_svg_path, 'rb') as f:
		svg_data = f.read()
	root = etree.fromstring(svg_data, parser)

	nsmap = root.nsmap.copy()
	svg_ns = nsmap.get(None, "http://www.w3.org/2000/svg")

	width_px, height_px = get_svg_pixel_dimensions(root)

	# First create a copy for rasterization (before font mapping)
	raster_root = etree.fromstring(etree.tostring(root))
	png_bytes = rasterize_non_text_elements(raster_root, width_px, height_px, svg_ns, input_svg_path)

	# Now process the original
	apply_font_map(root, font_map, svg_ns)
	keep_only_text_elements(root, svg_ns)
	embed_png_as_background(root, png_bytes, width_px, height_px, svg_ns)

	# Write the final output with clean XML
	with open(output_svg_path, 'wb') as f:
		svg_string = etree.tostring(
			root, 
			pretty_print=True, 
			xml_declaration=True, 
			encoding="UTF-8"
		)
		# Clean up any unwanted namespace prefixes
		svg_string = svg_string.replace(b'ns0:', b'').replace(b'ns1:', b'')
		f.write(svg_string)

	print(f"✅ Final output written to {output_svg_path}")



# svg_to_convert = [
# 	["../routes/greensboro-nc/assets/greensboro-grocery-360.svg", "../../static/greensboro-nc/greensboro-grocery-360.svg"],
# 	["../routes/greensboro-nc/assets/greensboro-grocery-1080.svg", "../../static/greensboro-nc/greensboro-grocery-1080.svg"]
# ]

# INPUT_SVG_PATH = "../routes/bridgeport-ct/assets/map-asthma-360.svg"
# OUTPUT_SVG_PATH = "../routes/bridgeport-ct/assets/map-asthma-360-web.svg"

# if __name__ == "__main__":
# 	for svg in svg_to_convert:
# 		process_svg(svg[0], svg[1], FONT_MAP)


from pathlib import Path

def main():
	city = "halifax-ns"
	input_dir = "../routes/" + city + "/assets"  
	output_dir = "../../static/"  + city + "/web-svg"

	for svg_file in Path(input_dir).glob("*.svg"):
		output_path = Path(output_dir) / svg_file.name
		process_svg(svg_file, output_path, FONT_MAP)

if __name__ == "__main__":
	main()