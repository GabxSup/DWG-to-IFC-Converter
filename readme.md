# DWG to IFC Converter

A lightweight, open-source CLI tool to convert DWG and DXF files to IFC format. Built with Python, using `ezdxf` and `ifcopenshell`.

## Features
- **DXF Support**: Natively converts DXF files to IFC4.
- **DWG Support**: Wraps ODA File Converter (if installed) to handle DWG files.
- **IFC Structure**: Automatically generates a valid IFC project hierarchy (Site -> Building -> Storey).
- **Geometry Mapping**: improved mapping of 2D lines to 3D `IfcBuildingElementProxy` entities.

## Prerequisites
- Python 3.8+
- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter) (Optional, for DWG support)

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/DWGConverter.git
    cd DWGConverter
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Convert a DXF file
```bash
python main.py input_file.dxf -o output_file.ifc
```

### Convert a DWG file
Requires ODA File Converter to be installed.
```bash
python main.py input_file.dwg -o output_file.ifc --oda-path "/usr/bin/ODAFileConverter"
```

## How it Works
1.  **Parsing**: The tool reads DXF geometry using `ezdxf`.
2.  **Mapping**: It maps basic entities (Lines, etc.) to IFC equivalent classes.
3.  **Generation**: It uses `ifcopenshell` to construct the IFC schema and write the file.

## Contributing
Contributions are welcome! Please fork the repository and submit a Pull Request.

## License
MIT License
