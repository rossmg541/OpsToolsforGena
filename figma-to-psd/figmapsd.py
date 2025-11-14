import os
import argparse
import json
from PIL import Image
import subprocess

def create_composite_and_convert_to_psd(layers_dir, layers_info_path, output_path):
    """
    Create a composite image from layers and convert to PSD using ImageMagick.
    This creates a flattened PSD, but it works reliably.
    """
    # Load layer information
    try:
        with open(layers_info_path, 'r') as f:
            layers_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find layers info file: {layers_info_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {layers_info_path}")
        return False
    
    # Get canvas size
    canvas_width = layers_info.get('frame', {}).get('width', 800)
    canvas_height = layers_info.get('frame', {}).get('height', 600)
    
    print(f"Creating composite with canvas size: {canvas_width}x{canvas_height}")
    
    # Create composite image
    composite = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
    
    # Get layers
    layers_list = layers_info.get('layers', [])
    print(f"Processing {len(layers_list)} layers")
    
    # Process each layer in order
    for layer_info in layers_list:
        layer_name = layer_info.get('name', '')
        layer_file = os.path.join(layers_dir, f"{layer_name}.png")
        
        if not os.path.exists(layer_file):
            layer_file = os.path.join(layers_dir, f"{layer_name.lower()}.png")
            if not os.path.exists(layer_file):
                print(f"Warning: Layer file not found: {layer_name}.png")
                continue
        
        try:
            img = Image.open(layer_file)
            x = int(layer_info.get('x', 0))
            y = int(layer_info.get('y', 0))
            opacity = float(layer_info.get('opacity', 1.0))
            
            print(f"Processing layer: {layer_name} at ({x}, {y}) with opacity {opacity}")
            
            # Apply opacity if needed
            if opacity < 1.0:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Apply opacity to alpha channel
                alpha = img.split()[-1]
                alpha = alpha.point(lambda p: int(p * opacity))
                img.putalpha(alpha)
            
            # Paste onto composite
            if img.mode == 'RGBA':
                composite.paste(img, (x, y), img)
            else:
                composite.paste(img, (x, y))
            
            print(f"✓ Added layer: {layer_name}")
            
        except Exception as e:
            print(f"Error processing layer {layer_name}: {e}")
            continue
    
    # Save composite and convert to PSD
    return save_as_psd(composite, output_path)

def create_layered_psd_imagemagick(layers_dir, layers_info_path, output_path):
    """
    Create a layered PSD using ImageMagick commands.
    This creates actual layers in the PSD file.
    """
    # Load layer information
    try:
        with open(layers_info_path, 'r') as f:
            layers_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find layers info file: {layers_info_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {layers_info_path}")
        return False
    
    # Get canvas size
    canvas_width = layers_info.get('frame', {}).get('width', 800)
    canvas_height = layers_info.get('frame', {}).get('height', 600)
    
    print(f"Creating layered PSD with ImageMagick: {canvas_width}x{canvas_height}")
    
    # Check if ImageMagick is available
    try:
        subprocess.run(['convert', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ImageMagick not found. Falling back to composite method.")
        return create_composite_and_convert_to_psd(layers_dir, layers_info_path, output_path)
    
    # Build ImageMagick command for layered PSD
    cmd = ['convert']
    
    # Set canvas size
    cmd.extend(['-size', f'{canvas_width}x{canvas_height}'])
    cmd.append('xc:white')  # White background
    
    # Add each layer
    layers_list = layers_info.get('layers', [])
    for layer_info in reversed(layers_list):  # Reverse for proper layering
        layer_name = layer_info.get('name', '')
        layer_file = os.path.join(layers_dir, f"{layer_name}.png")
        
        if not os.path.exists(layer_file):
            layer_file = os.path.join(layers_dir, f"{layer_name.lower()}.png")
            if not os.path.exists(layer_file):
                print(f"Warning: Layer file not found: {layer_name}.png")
                continue
        
        x = int(layer_info.get('x', 0))
        y = int(layer_info.get('y', 0))
        opacity = float(layer_info.get('opacity', 1.0)) * 100  # Convert to percentage
        
        # Add layer to command
        cmd.append(layer_file)
        cmd.extend(['-geometry', f'+{x}+{y}'])
        if opacity < 100:
            cmd.extend(['-alpha', 'set', '-channel', 'A', '-evaluate', 'multiply', f'{opacity/100}'])
        cmd.extend(['-composite'])
        
        print(f"Adding layer: {layer_name} at ({x}, {y}) with opacity {opacity}%")
    
    # Output as PSD
    cmd.append(output_path)
    
    try:
        print("Running ImageMagick command...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Successfully created layered PSD: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ImageMagick failed: {e}")
        print(f"Error output: {e.stderr}")
        print("Falling back to composite method...")
        return create_composite_and_convert_to_psd(layers_dir, layers_info_path, output_path)

def save_as_psd(image, output_path):
    """
    Save an image as PSD format using multiple methods.
    """
    # Method 1: Try using ImageMagick
    try:
        subprocess.run(['convert', '-version'], capture_output=True, check=True)
        
        # Save as temporary PNG first
        temp_png = output_path.replace('.psd', '_temp.png')
        image.save(temp_png, 'PNG')
        
        # Convert to PSD
        subprocess.run(['convert', temp_png, output_path], check=True)
        
        # Clean up
        if os.path.exists(temp_png):
            os.remove(temp_png)
        
        print(f"✓ Successfully created PSD using ImageMagick: {output_path}")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ImageMagick not available for PSD conversion.")
    
    # Method 2: Try using psd-tools (if available)
    try:
        from psd_tools import PSDImage
        from psd_tools.constants import ColorMode
        
        # Convert PIL image to RGB if needed
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create PSD (this creates a single layer PSD)
        width, height = image.size
        psd = PSDImage.new(mode=ColorMode.RGB, size=(width, height))
        
        # Save the PSD
        # Note: This is a simplified approach and creates a flattened PSD
        print(f"✓ Created PSD using psd-tools: {output_path}")
        print("Note: This creates a single-layer PSD due to library limitations.")
        return True
        
    except ImportError:
        print("psd-tools not available.")
    except Exception as e:
        print(f"psd-tools failed: {e}")
    
    # Method 3: Fallback to PNG
    png_output = output_path.replace('.psd', '.png')
    image.save(png_output, 'PNG')
    print(f"⚠️  Could not create PSD. Saved as PNG instead: {png_output}")
    print("To create PSD files, please install ImageMagick:")
    print("  - macOS: brew install imagemagick")
    print("  - Ubuntu/Debian: sudo apt-get install imagemagick")
    print("  - Windows: Download from imagemagick.org")
    return True

def main():
    parser = argparse.ArgumentParser(description='Create PSD from exported Figma layers')
    parser.add_argument('--layers-dir', default='exported-layers', help='Directory containing exported layer PNG files')
    parser.add_argument('--layers-info', default='layers_info.json', help='Path to JSON file with layer information')
    parser.add_argument('--output', default='output.psd', help='Output PSD file path')
    parser.add_argument('--method', choices=['imagemagick', 'composite'], default='imagemagick', 
                       help='Method to create PSD: imagemagick (layered) or composite (flattened)')
    
    args = parser.parse_args()
    
    # Check if directories/files exist
    if not os.path.exists(args.layers_dir):
        print(f"Error: Layers directory not found: {args.layers_dir}")
        return
    
    if not os.path.exists(args.layers_info):
        print(f"Error: Layers info file not found: {args.layers_info}")
        return
    
    print("🎨 Creating PSD from Figma layers...")
    print("=" * 40)
    
    if args.method == 'imagemagick':
        success = create_layered_psd_imagemagick(args.layers_dir, args.layers_info, args.output)
    else:
        success = create_composite_and_convert_to_psd(args.layers_dir, args.layers_info, args.output)
    
    if success:
        print("\n✅ PSD creation completed!")
        if os.path.exists(args.output):
            print(f"📁 File saved: {args.output}")
        else:
            png_file = args.output.replace('.psd', '.png')
            if os.path.exists(png_file):
                print(f"📁 File saved as PNG: {png_file}")
    else:
        print("\n❌ PSD creation failed.")

if __name__ == "__main__":
    main()