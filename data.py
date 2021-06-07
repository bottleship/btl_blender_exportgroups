import bpy

# These enums are literal copies of the ones defined in io_alembic.c
enum_modifier_triangulate_quad_method_items = [
    ("BEAUTY", "Beauty", "Split the quads in nice triangles, slower method", 1),
    ("FIXED", "Fixed", "Split the quads on the first and third vertices", 2),
    ("FIXED_ALTERNATE", "Fixed alternate", "Split the quads on the 2nd and 4th vertices", 4),
    ("SHORTEST_DIAGONAL", "Shortest diagonal", "Split the quads on the 2nd and 4th vertices", 8)]

enum_modifier_triangulate_ngon_method_items = [
    ("BEAUTY", "Beauty", "Arrange the new triangles evenly (slow)", 1),
    ("CLIP", "Clip", "Split the polygons with an ear clipping algorithm", 2)]


class ExportGroupSettings(bpy.types.PropertyGroup):
    """ Complete set of settings for exporting alembic.
    These are the same as the settings defined in io_alembic.c
    which, however, are bound to the ui and not exposed in Python.
    """
    filepath: bpy.props.StringProperty(
        name="File path",
        subtype="FILE_PATH")
    start: bpy.props.IntProperty(name="Start frame")
    end: bpy.props.IntProperty(name="End frame")
    xsamples: bpy.props.IntProperty(
        name="Transform samples",
        default=1,
        min=1,
        max=128)
    gsamples: bpy.props.IntProperty(
        name="Geometry samples",
        default=1,
        min=1,
        max=128)
    sh_open: bpy.props.FloatProperty(
        name="Shutter Open",
        default=0.0,
        min=-1.0,
        max=1.0)
    sh_close: bpy.props.FloatProperty(
        name="Shutter Close",
        default=1.0,
        min=-1.0,
        max=1.0)
    selected: bpy.props.BoolProperty(
        name="Selected objects only",
        description="Export only selected objects",
        default=True)
    renderable_only: bpy.props.BoolProperty(
        name="Renderable objects only",
        description="Export only objects marked renderable in the outliner",
        default=True)
    visible_objects_only: bpy.props.BoolProperty(
        name="Visible objects only",
        description="Export only objects that are visible",
        default=False)
    flatten: bpy.props.BoolProperty(
        name="Flatten hierarchy",
        description="Do not preserve objects' parent/child relationship",
        default=False)
    uvs: bpy.props.BoolProperty(
        name="UVs",
        description="Export UVs",
        default=True)
    packuv: bpy.props.BoolProperty(
        name="Pack UV islands",
        description="Export UVs with packed island",
        default=True)
    normals: bpy.props.BoolProperty(
        name="Normals",
        description="Export normals",
        default=True)
    vcolors: bpy.props.BoolProperty(
        name="Vertex colors",
        description="Export vertex colors",
        default=False)
    face_sets: bpy.props.BoolProperty(
        name="Face sets",
        description="Export per face shading group assignments",
        default=False)
    subdiv_schema: bpy.props.BoolProperty(
        name="Use subdivision schema",
        description="Export meshes using Alembic's subdivision schema",
        default=False)
    apply_subdiv: bpy.props.BoolProperty(
        name="Apply subdivision surface",
        description="Export subdivision surfaces as meshes",
        default=False)
    curves_as_mesh: bpy.props.BoolProperty(
        name="Curves as mesh",
        description="Export curves and NURBS surfaces as meshes",
        default=False)
    use_instancing: bpy.props.BoolProperty(
        name="Use instancing",
        description="Export data of duplicated objects as Alembic instances; speeds up the export; can be disabled for compatibility with other software",
        default=False)
    global_scale: bpy.props.FloatProperty(
        name="Scale",
        description="Value by which to enlarge or shrink the objects with respect to the world's origin",
        default=1.0,
        min=0.0001,
        max=1000.0)
    triangulate: bpy.props.BoolProperty(
        name="Triangulate",
        description="Export Polygons (Quads & NGons) as Triangles",
        default=False)
    quad_method: bpy.props.EnumProperty(
        name="Quad method",
        description="Method for splitting the quads into triangles",
        items=enum_modifier_triangulate_quad_method_items,
        default="SHORTEST_DIAGONAL")
    ngon_method: bpy.props.EnumProperty(
        name="Polygon method",
        description="Method for splitting the polygons into triangles",
        items=enum_modifier_triangulate_ngon_method_items,
        default="BEAUTY")
    export_hair: bpy.props.BoolProperty(
        name="Export hair",
        description="Export hair particle systems as animated curves",
        default=True)
    export_particles: bpy.props.BoolProperty(
        name="Export particles",
        description="Export non-hair particle systems",
        default=True)
    export_custom_properties: bpy.props.BoolProperty(
        name="Export custom properties",
        description="Export custom properties to Alembic .userProperties",
        default=True)
    as_background_job: bpy.props.BoolProperty(
        name="Run as background job",
        description="Enable this to run the export in the background, disable to block Blender while exporting. ",
        default=True)


class GroupObject(bpy.types.PropertyGroup):
    """ This is a pointer to an object;
    used in a collection in the export group.
    """
    object: bpy.props.PointerProperty(type=bpy.types.Object)


class ExportGroup(bpy.types.PropertyGroup):
    """ The export group combines the list of objects,
    the export settings, and a couple of service properties.
    """
    expanded: bpy.props.BoolProperty(
        name="Expanded",
        default=False)
    group_selected: bpy.props.BoolProperty(
        name="Selected",
        default=False)
    objects: bpy.props.CollectionProperty(
        name="Objects",
        type=GroupObject)
    settings: bpy.props.PointerProperty(
        name="Settings",
        type=ExportGroupSettings)
