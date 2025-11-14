import os
import json
import argparse
from PIL import Image

def scan_layers_directory(layers_dir):
    """
    Scan the layers directory and return information about found PNG files.
    """
    layer_files = []
    
    if not os.path.exists(layers_dir):
        print(f"Error: Directory '{layers_dir}' does not exist.")
        return layer_files
    
    # Get all PNG files in the directory
    for filename in os.listdir(layers_dir):
        if filename.lower().endswith('.png'):
            layer_files.append(filename)
    
    # Sort files alphabetically for consistent ordering
    layer_files.sort()
    
    return layer_files

def get_image_info(image_path):
    """
    Get basic information about an image file.
    """
    try:
        with Image.open(image_path) as img:
            return {
                'width': img.size[0],
                'height': img.size[1],
                'mode': img.mode
            }
    except Exception as e:
        print(f"Warning: Could not read image info from {image_path}: {e}")
        return {'width': 0, 'height': 0, 'mode': 'RGB'}

def estimate_canvas_size(layers_dir, layer_files):
    """
    Estimate canvas size based on the largest dimensions found in layer images.
    """
    max_width = 800  # Default fallback
    max_height = 600  # Default fallback
    
    for filename in layer_files:
        image_path = os.path.join(layers_dir, filename)
        img_info = get_image_info(image_path)
        max_width = max(max_width, img_info['width'])
        max_height = max(max_height, img_info['height'])
    
    return max_width, max_height

def generate_layers_info(layers_dir='exported-layers', output_file='layers_info.json', update_existing=False):
    """
    Generate or update layers_info.json based on PNG files in the layers directory.
    """
    print(f"Scanning directory: {layers_dir}")
    
    # Scan for PNG files
    layer_files = scan_layers_directory(layers_dir)
    
    if not layer_files:
        print(f"No PNG files found in '{layers_dir}' directory.")
        return False
    
    print(f"Found {len(layer_files)} PNG files:")
    for filename in layer_files:
        print(f"  - {filename}")
    
    # Load existing JSON if updating
    existing_data = {}
    if update_existing and os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
            print(f"Loaded existing data from {output_file}")
        except Exception as e:
            print(f"Warning: Could not load existing JSON file: {e}")
            existing_data = {}
    
    # Estimate canvas size
    canvas_width, canvas_height = estimate_canvas_size(layers_dir, layer_files)
    
    # Use existing frame dimensions if available
    if 'frame' in existing_data:
        canvas_width = existing_data['frame'].get('width', canvas_width)
        canvas_height = existing_data['frame'].get('height', canvas_height)
    
    # Create layers info structure
    layers_info = {
        "frame": {
            "width": canvas_width,
            "height": canvas_height
        },
        "layers": []
    }
    
    # Create a mapping of existing layers for updates
    existing_layers = {}
    if 'layers' in existing_data:
        for layer in existing_data['layers']:
            existing_layers[layer.get('name', '')] = layer
    
    # Process each PNG file
    y_offset = 0  # Stack layers vertically by default
    layer_spacing = 50  # Space between layers if stacking
    
    for i, filename in enumerate(layer_files):
        # Extract layer name (remove .png extension)
        layer_name = os.path.splitext(filename)[0]
        
        # Get image dimensions
        image_path = os.path.join(layers_dir, filename)
        img_info = get_image_info(image_path)
        
        # Check if this layer already exists in the JSON
        if layer_name in existing_layers:
            # Use existing layer data
            layer_data = existing_layers[layer_name].copy()
            print(f"  Using existing data for: {layer_name}")
        else:
            # Create new layer data with intelligent defaults
            layer_data = {
                "name": layer_name,
                "x": 0,  # Default to left edge
                "y": y_offset,  # Stack vertically
                "opacity": 1.0
            }
            
            # Update y_offset for next layer (stacking approach)
            y_offset += max(50, img_info['height'] // 4)  # Space layers out
            
            print(f"  Created new entry for: {layer_name}")
        
        # Add image info as comments (these won't affect the PSD creation)
        layer_data["_image_width"] = img_info['width']
        layer_data["_image_height"] = img_info['height']
        layer_data["_image_mode"] = img_info['mode']
        
        layers_info["layers"].append(layer_data)
    
    # Add helpful comments to the JSON
    layers_info["_instructions"] = {
        "frame": "Set the canvas size for your PSD file",
        "layers": {
            "name": "Must match the PNG filename (without .png)",
            "x": "Horizontal position in pixels (0 = left edge)",
            "y": "Vertical position in pixels (0 = top edge)", 
            "opacity": "Layer opacity (1.0 = 100%, 0.5 = 50%, etc.)"
        },
        "_image_*": "These are auto-generated info fields - you can ignore them"
    }
    
    # Save the JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(layers_info, f, indent=2)
        
        print(f"\n✅ Successfully {'updated' if update_existing else 'created'} {output_file}")
        print(f"📋 Canvas size: {canvas_width}x{canvas_height}")
        print(f"🎨 Layers: {len(layers_info['layers'])}")
        
        print(f"\n📝 Next steps:")
        print(f"   1. Edit {output_file} to adjust layer positions (x, y coordinates)")
        print(f"   2. Update canvas size in 'frame' section if needed")
        print(f"   3. Adjust opacity values if needed")
        print(f"   4. Run: python create_layered_psd.py")
        
        return True
        
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate layers_info.json from exported layer files')
    parser.add_argument('--layers-dir', default='exported-layers', help='Directory containing exported layer PNG files')
    parser.add_argument('--output', default='layers_info.json', help='Output JSON file path')
    parser.add_argument('--update', action='store_true', help='Update existing JSON file instead of creating new')
    parser.add_argument('--canvas-width', type=int, help='Override canvas width')
    parser.add_argument('--canvas-height', type=int, help='Override canvas height')
    
    args = parser.parse_args()
    
    print("🔍 Figma Layers Info Generator")
    print("=" * 40)
    
    success = generate_layers_info(
        layers_dir=args.layers_dir,
        output_file=args.output,
        update_existing=args.update
    )
    
    if not success:
        print("\n❌ Failed to generate layers info file.")
        return
    
    # Show preview of generated file
    if os.path.exists(args.output):
        print(f"\n📄 Preview of {args.output}:")
        print("-" * 30)
        try:
            with open(args.output, 'r') as f:
                data = json.load(f)
            
            print(f"Frame: {data['frame']['width']}x{data['frame']['height']}")
            print("Layers:")
            for layer in data['layers']:
                name = layer.get('name', 'unnamed')
                x = layer.get('x', 0)
                y = layer.get('y', 0)
                opacity = layer.get('opacity', 1.0)
                print(f"  • {name}: position({x}, {y}), opacity({opacity})")
                
        except Exception as e:
            print(f"Could not preview file: {e}")

if __name__ == "__main__":
    main()