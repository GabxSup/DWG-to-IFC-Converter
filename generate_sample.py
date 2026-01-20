import ezdxf

def create_sample_dxf(filename="sample.dxf"):
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # Add some lines
    msp.add_line((0, 0), (10, 0))
    msp.add_line((10, 0), (10, 10))
    msp.add_line((10, 10), (0, 10))
    msp.add_line((0, 10), (0, 0))
    
    doc.saveas(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_sample_dxf()
