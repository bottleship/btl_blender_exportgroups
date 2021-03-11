import bpy
import sys

from bpy import context


bl_info = {
    "name": "Alembic Export Groups",
    "blender": (2, 80, 0),
    "category": "Object"
}


class AddSelectedToExportGroupOperator(bpy.types.Operator):
    """ Add selected objects to an export group.
    If op is invoked, user will be asked for group name.
    """
    bl_idname = "object.add_selected_to_group"
    bl_label = "Add selected objects to export group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: bpy.props.StringProperty(name="Group name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self.report({"INFO"}, self.group_name)
        found_groups = [g for g in context.scene.alembic_export_settings if g.name == self.group_name]

        # if group not found, create it
        if len(found_groups) == 0:
            new_group = context.scene.alembic_export_settings.add()
            new_group.name = self.group_name
            context.scene.alembic_export_index += 1

        for obj in context.selected_objects:
            obj.export_group = self.group_name

        return {"FINISHED"}


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
    Also contains a couple of service settings like expanded and group_selected.
    """
    expanded: bpy.props.BoolProperty(
        name="Expanded",
        default=False)
    group_selected: bpy.props.BoolProperty(
        name="Selected",
        default=False)
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
        description="Enable this to run the import in the background, disable to block Blender while importing. ",
        default=False)


class ObjectExportGroupPanel(bpy.types.Panel):
    """ Panel in which the user can enter a group name to add to. """
    bl_idname = "OBJECT_PT_export_group"
    bl_label = "Alembic export group"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        if context.object is not None:
            self.layout.prop(context.object, "export_group")


class SceneExportGroupPanel(bpy.types.UIList):
    """ Panel that contains settings for a single group
    """
    bl_idname = "SCENE_UL_export_group"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        box = layout.box()
        row = box.row()
        col = row.column()
        col.prop(item, "expanded",
                 icon="TRIA_DOWN" if item.expanded else "TRIA_RIGHT",
                 icon_only=True, emboss=False)
        col = row.column()
        col.prop(item, "name")
        col = row.column()
        col.prop(item, "group_selected")

        if item.expanded:
            for propname in [k
                             for k in item.__annotations__.keys()
                             if k not in ["expanded", "group_selected"]]:
                box.prop(item, propname)


class SceneExportGroupsPanel(bpy.types.Panel):
    """ Top-level panel for export settings.
    """
    bl_label = "Alembic export group settings"
    bl_idname = "SCENE_PT_export_groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Alembic export group settings"

    def draw(self, context):
        self.layout.template_list(
            "SCENE_UL_export_group",
            "",
            context.scene,
            "alembic_export_settings",
            context.scene,
            "alembic_export_index")

        self.layout.operator(
            "scene.export_groups",
            text=ExportGroupsOperator.bl_label,
            icon="EXPORT")
        self.layout.operator(
            "scene.export_selected_groups",
            text=ExportSelectedGroupsOperator.bl_label,
            icon="EXPORT")
        self.layout.operator(
            "scene.delete_selected_export_groups",
            icon="TRASH")


class DeleteSelectedExportGroupsOperator(bpy.types.Operator):
    """ Delete the currently selected export groups.
    """
    bl_idname = "scene.delete_selected_export_groups"
    bl_label = "Delete selected export groups"

    def execute(self, context):
        selected_groups = [(i, s.name)
                     for i, s in enumerate(context.scene.alembic_export_settings)
                     if s.group_selected]
        idxs, names = zip(*selected_groups)

        # first clear property on objects in groups
        for obj in bpy.data.objects:
            if obj.export_group in names:
                obj.export_group = ""

        # now delete the groups
        for settings_idx in idxs:
            context.scene.alembic_export_settings.remove(settings_idx)

        return {"FINISHED"}


def export_group(settings):
    for obj in bpy.data.objects:
        obj.select_set(obj.export_group == settings.name)

    # filter out args from property group
    opargs = {k: getattr(settings, k)
              for k in settings.__annotations__.keys()
              if k not in ["name", "expanded", "group_selected"]}
    return bpy.ops.wm.alembic_export(context.copy(),
                                     "EXEC_DEFAULT",
                                     **opargs)


class ExportGroupsOperator(bpy.types.Operator):
    """ Export all alembic groups operator """
    bl_idname = "scene.export_groups"
    bl_label = "Export all groups"

    def execute(self, context):
        print("Running")
        for settings in context.scene.alembic_export_settings:
            print("Exporting group {}".format(settings.name))
            if settings.filepath == "":
                self.report(
                    {"ERROR"},
                    "Filepath cannot be empty for group {}".format(settings.name))
                return {"CANCELLED"}

            export_group(settings)

        self.report({"INFO"}, "All alembic groups exported")
        return {"FINISHED"}


class ExportSelectedGroupsOperator(bpy.types.Operator):
    """ Export the currently selected groups """
    bl_idname = "scene.export_selected_groups"
    bl_label = "Export selected groups"

    def execute(self, context):
        print("Running")
        for settings in context.scene.alembic_export_settings:
            if not settings.group_selected:
                continue

            print("Exporting group {}".format(settings.name))
            if settings.filepath == "":
                self.report(
                    {"ERROR"},
                    "Filepath cannot be empty for group {}".format(settings.name))
                return {"CANCELLED"}

            export_group(settings)

        self.report({"INFO"}, "All selected alembic groups exported")
        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(AddSelectedToExportGroupOperator.bl_idname)


def register():
    bpy.types.Object.export_group = bpy.props.StringProperty(
        name="Export group",
        description="Name of alembic export group")
    bpy.utils.register_class(ExportGroupSettings)
    bpy.types.Scene.alembic_export_settings = bpy.props.CollectionProperty(
        type=ExportGroupSettings)
    bpy.types.Scene.alembic_export_index = bpy.props.IntProperty(
        name="Index for alembic export group",
        default=0)
    bpy.utils.register_class(AddSelectedToExportGroupOperator)
    bpy.utils.register_class(ObjectExportGroupPanel)
    bpy.utils.register_class(SceneExportGroupPanel)
    bpy.utils.register_class(SceneExportGroupsPanel)
    bpy.utils.register_class(DeleteSelectedExportGroupsOperator)
    bpy.utils.register_class(ExportGroupsOperator)
    bpy.utils.register_class(ExportSelectedGroupsOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    del bpy.types.Object.export_group
    del bpy.types.Scene.alembic_export_settings
    del bpy.types.Scene.alembic_export_index
    bpy.utils.unregister_class(ExportGroupSettings)
    bpy.utils.unregister_class(AddSelectedToExportGroupOperator)
    bpy.utils.unregister_class(ObjectExportGroupPanel)
    bpy.utils.unregister_class(SceneExportGroupPanel)
    bpy.utils.unregister_class(SceneExportGroupsPanel)
    bpy.utils.unregister_class(DeleteSelectedExportGroupsOperator)
    bpy.utils.unregister_class(ExportGroupsOperator)
    bpy.utils.unregister_class(ExportSelectedGroupsOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
