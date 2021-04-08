import bpy
import sys
import os


import btl_blender_exportgroups.ops as btlops
import btl_blender_exportgroups.ui as btlui
import btl_blender_exportgroups.data as btldata


bl_info = {
    "name": "Alembic Export Groups",
    "author": "Mois Moshev (Bottleship)",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "description": "Persist groups of objects with their own alembic export settings",
    "category": "Object"
}


def register():
    bpy.utils.register_class(btldata.ExportGroupSettings)
    bpy.utils.register_class(btldata.GroupObject)
    bpy.utils.register_class(btldata.ExportGroup)

    bpy.types.Scene.alembic_export_groups = bpy.props.CollectionProperty(
        type=btldata.ExportGroup)
    bpy.types.Scene.alembic_export_index = bpy.props.IntProperty(
        name="Index for alembic export group",
        default=0)

    bpy.utils.register_class(btlops.AddSelectedToExportGroupOperator)
    bpy.utils.register_class(btlops.AddSelectedToExportGroupOperatorNoQuery)
    bpy.utils.register_class(btlops.RemoveSelectedFromExportGroupOperator)
    bpy.utils.register_class(btlops.SelectExportGroupObjectsOperator)
    bpy.utils.register_class(btlops.CreateExportGroupOperator)
    bpy.utils.register_class(btlui.ObjectExportGroupPanel)
    bpy.utils.register_class(btlui.SceneExportGroupPanel)
    bpy.utils.register_class(btlui.SceneExportGroupsPanel)
    bpy.utils.register_class(btlops.DeleteSelectedExportGroupsOperator)
    bpy.utils.register_class(btlops.ExportGroupsOperator)
    bpy.utils.register_class(btlops.ExportSelectedGroupsOperator)
    bpy.types.VIEW3D_MT_object.append(btlui.menu_func)


def unregister():
    del bpy.types.Scene.alembic_export_groups
    del bpy.types.Scene.alembic_export_index
    bpy.utils.unregister_class(btlops.ExportGroup)
    bpy.utils.unregister_class(btlops.GroupObject)
    bpy.utils.unregister_class(btldata.ExportGroupSettings)
    bpy.utils.unregister_class(btlops.AddSelectedToExportGroupOperator)
    bpy.utils.unregister_class(btlops.AddSelectedToExportGroupOperatorNoQuery)
    bpy.utils.unregister_class(btlops.RemoveSelectedFromExportGroupOperator)
    bpy.utils.unregister_class(btlops.CreateExportGroupOperator)
    bpy.utils.unregister_class(btlops.SelectExportGroupObjectsOperator)
    bpy.utils.unregister_class(btlui.ObjectExportGroupPanel)
    bpy.utils.unregister_class(btlui.SceneExportGroupPanel)
    bpy.utils.unregister_class(btlui.SceneExportGroupsPanel)
    bpy.utils.unregister_class(btlops.DeleteSelectedExportGroupsOperator)
    bpy.utils.unregister_class(btlops.ExportGroupsOperator)
    bpy.utils.unregister_class(btlops.ExportSelectedGroupsOperator)
    bpy.types.VIEW3D_MT_object.remove(btlui.menu_func)


if __name__ == "__main__":
    register()
