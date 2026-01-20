import ezdxf
import ifcopenshell
import ifcopenshell.api
import ifcopenshell.guid
import time
import uuid

def create_ifc_base(filename="output.ifc"):
    """
    Creates a new IFC file with a basic project structure.
    """
    model = ifcopenshell.file()
    
    # Create project, site, building, storey
    project = model.create_entity("IfcProject", GlobalId=ifcopenshell.guid.new(), Name="DXF Conversion Project")
    
    # Units
    ifcopenshell.api.run("unit.assign_unit", model)
    
    # Context
    model_context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body_context = ifcopenshell.api.run("context.add_context", model, context_type="Model", 
                                        context_identifier="Body", target_view="MODEL_VIEW", parent=model_context)
    
    
    site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite", name="Default Site")
    building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="Default Building")
    storey = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")
    
    ifcopenshell.api.run("aggregate.assign_object", model, relating_object=project, products=[site])
    ifcopenshell.api.run("aggregate.assign_object", model, relating_object=site, products=[building])
    ifcopenshell.api.run("aggregate.assign_object", model, relating_object=building, products=[storey])
    
    return model, storey, body_context

def convert_dxf_to_ifc(dxf_path, ifc_path):
    """
    Reads DXF and writes IFC.
    """
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    model, storey, body_context = create_ifc_base(ifc_path)
    
    # Simple container for all created elements
    owner_history = model.create_entity("IfcOwnerHistory") # Basic required entity often needed for older schemas, though optional in newer
    
    print(f"Analyzing {len(list(msp))} entities in ModelSpace...")
    
    count = 0
    
    for entity in msp:
        # We focus on LINE for creating walls/proxies
        # Real implementation would handle multiple geometry types
        
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            
            # Create a simple generic building element proxy for the line
            # In a real app, we would extrude this to make a wall
            
            # Create the curve geometry
            p1 = model.create_entity("IfcCartesianPoint", Coordinates=(float(start.x), float(start.y), float(start.z)))
            p2 = model.create_entity("IfcCartesianPoint", Coordinates=(float(end.x), float(end.y), float(end.z)))
            line = model.create_entity("IfcPolyline", Points=[p1, p2])
            
            shape = model.create_entity("IfcShapeRepresentation", 
                                        ContextOfItems=body_context, 
                                        RepresentationIdentifier="Body", 
                                        RepresentationType="Curve2D", 
                                        Items=[line])
                                        
            # Create the element
            # We map everything to IfcBuildingElementProxy for now
            element_name = f"Line_{count}"
            element = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingElementProxy", name=element_name)
            
            # Assign geometry
            ifcopenshell.api.run("geometry.assign_representation", model, product=element, representation=shape)
            
            # Assign to storey
            ifcopenshell.api.run("spatial.assign_container", model, relating_structure=storey, products=[element])
            
            count += 1
            
    print(f"Converted {count} supported entities.")
    model.write(ifc_path)
