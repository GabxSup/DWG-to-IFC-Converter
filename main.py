import sys
import os
import argparse
from converter import convert_dxf_to_ifc

def main():
    parser = argparse.ArgumentParser(description="DWG/DXF to IFC Converter")
    parser.add_argument("input_file", help="Path to input DWG or DXF file")
    parser.add_argument("-o", "--output", help="Path to output IFC file", default="output.ifc")
    parser.add_argument("--oda-path", help="Path to ODA File Converter executable (optional)", default=None)
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input_file)
    output_path = os.path.abspath(args.output)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
        
    ext = os.path.splitext(input_path)[1].lower()
    
    dxf_path = input_path
    temp_dxf = False
    
    # Handle DWG conversion if needed
    if ext == ".dwg":
        print("Detected DWG file. Attempting to convert to DXF first...")
        # Placeholder for ODA conversion logic
        # For now, we warn the user if they don't provide a DXF
        print("Warning: Direct DWG conversion requires ODA File Converter.")
        print("Please convert to DXF manually or provide ODA path (not fully implemented yet).")
        sys.exit(1)
    elif ext != ".dxf":
        print(f"Error: Unsupported file extension '{ext}'. Please use .dxf or .dwg")
        sys.exit(1)
        
    print(f"Converting '{dxf_path}' to '{output_path}'...")
    
    try:
        convert_dxf_to_ifc(dxf_path, output_path)
        print("Conversion completed successfully.")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
