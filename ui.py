import bpy
import btl_blender_exportgroups.ops as btlops


def menu_func(self, context):
    self.layout.operator(btlops.AddSelectedToExportGroupOperator.bl_idname)


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
            box_objects = box.box()
            if len(item.objects) > 0:
                box_objects.label(text="Objects", icon="OBJECT_DATA")
                for obj in item.objects:
                    box_objects.prop(obj.object, "name")
            else:
                box_objects.label(text="No objects in group")

            # add ops
            row = box.row()
            col = row.column()
            op_add = col.operator("scene.add_selected_to_group_no_query", icon="ADD")
            op_add.group_name = item.name
            col = row.column()
            op_remove = col.operator("scene.remove_selected_from_group", icon="REMOVE")
            op_remove.group_name = item.name
            col = row.column()
            op_select = col.operator("scene.select_export_group_objects", icon="SELECT_SET")
            op_select.group_name = item.name

            box_settings = box.box()
            box_settings.label(text="Export settings", icon="SETTINGS")
            for propname in [k
                             for k in item.settings.__annotations__.keys()
                             if k not in ["expanded", "group_selected"]]:
                box_settings.prop(item.settings, propname)


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
            "alembic_export_groups",
            context.scene,
            "alembic_export_index")

        self.layout.operator(
            "scene.create_export_group",
            text=btlops.CreateExportGroupOperator.bl_label,
            icon="ADD")
        self.layout.operator(
            "scene.export_groups",
            text=btlops.ExportGroupsOperator.bl_label,
            icon="EXPORT")
        self.layout.operator(
            "scene.export_selected_groups",
            text=btlops.ExportSelectedGroupsOperator.bl_label,
            icon="EXPORT")
        self.layout.operator(
            "scene.delete_selected_export_groups",
            icon="TRASH")
