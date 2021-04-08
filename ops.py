import os
import bpy


def add_selected_objects_to_group(group_name, context):
    found_groups = [g for g in context.scene.alembic_export_groups
                    if g.name == group_name]

    # if group not found, create it
    if len(found_groups) == 0:
        new_group = context.scene.alembic_export_groups.add()
        new_group.name = group_name
        new_group.settings.start = context.scene.frame_start
        new_group.settings.end = context.scene.frame_end
        context.scene.alembic_export_index += 1
        for obj in context.selected_objects:
            obj_ref = new_group.objects.add()
            obj_ref.object = obj
    else:
        found_objects = [o.object for o in found_groups[0].objects]
        for obj in context.selected_objects:
            if obj not in found_objects:
                obj_ref = found_groups[0].objects.add()
                obj_ref.object = obj


def do_export_group(export_group, context):
    filedir = os.path.dirname(export_group.settings.filepath)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    for obj in bpy.data.objects:
        obj.select_set(state=False)

    for obj_ref in export_group.objects:
        obj_ref.object.select_set(state=True)

    # filter out args from property group
    opargs = {k: getattr(export_group.settings, k)
              for k in export_group.settings.__annotations__.keys()}
    return bpy.ops.wm.alembic_export(context.copy(),
                                     "EXEC_DEFAULT",
                                     **opargs)


class AddSelectedToExportGroupOperator(bpy.types.Operator):
    """ Add selected objects to an export group.
    If op is invoked, user will be asked for group name.
    """
    bl_idname = "scene.add_selected_to_group"
    bl_label = "Add selected objects to export group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: bpy.props.StringProperty(name="Group name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        self.report({"INFO"}, self.group_name)
        add_selected_objects_to_group(self.group_name, context)

        return {"FINISHED"}


class AddSelectedToExportGroupOperatorNoQuery(bpy.types.Operator):
    """ Add selected objects to an export group.
    If op is invoked, user will be asked for group name.
    """
    bl_idname = "scene.add_selected_to_group_no_query"
    bl_label = "Add selected objects to export group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: bpy.props.StringProperty(name="Group name")

    def execute(self, context):
        self.report({"INFO"}, self.group_name)
        add_selected_objects_to_group(self.group_name, context)
        return {"FINISHED"}


class RemoveSelectedFromExportGroupOperator(bpy.types.Operator):
    """ Remove selected objects from export group. """
    bl_idname = "scene.remove_selected_from_group"
    bl_label = "Remove selected objects from export group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: bpy.props.StringProperty(name="Group name")

    def execute(self, context):
        found_groups = [g for g in context.scene.alembic_export_groups if g.name == self.group_name]

        if len(found_groups) > 0:
            found_obj_idxs = [i for i, o in enumerate(found_groups[0].objects)
                              if o.object in context.selected_objects]
            found_obj_idxs.reverse()
            for idx in found_obj_idxs:
                found_groups[0].objects.remove(idx)
        else:
            return {"CANCELLED"}

        return {"FINISHED"}


class CreateExportGroupOperator(bpy.types.Operator):
    """ Create a new export group.
If invoked, user will be queried for group name
    """
    bl_idname = "scene.create_export_group"
    bl_label = "Create group"
    bl_options = {"REGISTER", "UNDO"}

    group_name: bpy.props.StringProperty(name="Group name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        found_groups = [g for g in context.scene.alembic_export_groups
                        if g.name == self.group_name]

        if len(found_groups) == 0:
            new_group = context.scene.alembic_export_groups.add()
            new_group.name = self.group_name
            new_group.settings.start = context.scene.frame_start
            new_group.settings.end = context.scene.frame_end
            for obj in context.selected_objects:
                obj_ref = new_group.objects.add()
                obj_ref.object = obj

        return {"FINISHED"}



class DeleteSelectedExportGroupsOperator(bpy.types.Operator):
    """ Delete the currently selected export groups.
    """
    bl_idname = "scene.delete_selected_export_groups"
    bl_label = "Delete selected export groups"

    def execute(self, context):
        selected_groups = [(i, s.name)
                     for i, s in enumerate(context.scene.alembic_export_groups)
                     if s.group_selected]
        idxs, names = zip(*selected_groups)

        # now delete the groups
        for group_idx in idxs:
            context.scene.alembic_export_groups.remove(group_idx)

        return {"FINISHED"}


class SelectExportGroupObjectsOperator(bpy.types.Operator):
    """ Select the objects contained in this group.
    """
    bl_idname = "scene.select_export_group_objects"
    bl_label = "Select objects within this group"

    group_name: bpy.props.StringProperty(name="Group name")

    def execute(self, context):
        found_groups = [g for g in context.scene.alembic_export_groups
                        if g.name == self.group_name]

        if len(found_groups) == 0:
            return {"CANCELLED"}

        # first deselect current selection
        for obj in context.selected_objects:
            obj.select_set(state=False)

        for obj_ref in found_groups[0].objects:
            obj_ref.object.select_set(state=True)

        return {"FINISHED"}


class ExportGroupsOperator(bpy.types.Operator):
    """ Export all alembic groups operator """
    bl_idname = "scene.export_groups"
    bl_label = "Export all groups"

    def execute(self, context):
        print("Running")
        for export_group in context.scene.alembic_export_groups:
            print("Exporting group {}".format(export_group.name))
            if export_group.settings.filepath == "":
                self.report(
                    {"ERROR"},
                    "Filepath cannot be empty for group {}".format(export_group.name))
                return {"CANCELLED"}

            do_export_group(export_group, context)

        self.report({"INFO"}, "All alembic groups exported")
        return {"FINISHED"}


class ExportSelectedGroupsOperator(bpy.types.Operator):
    """ Export the currently selected groups """
    bl_idname = "scene.export_selected_groups"
    bl_label = "Export selected groups"

    def execute(self, context):
        print("Running")
        for export_group in context.scene.alembic_export_groups:
            if not export_group.group_selected:
                continue

            print("Exporting group {}".format(export_group.name))
            if export_group.settings.filepath == "":
                self.report(
                    {"ERROR"},
                    "Filepath cannot be empty for group {}".format(export_group.name))
                return {"CANCELLED"}

            do_export_group(export_group, context)

        self.report({"INFO"}, "All selected alembic groups exported")
        return {"FINISHED"}


class SetSelectedGroupsRangeFromSceneOperator(bpy.types.Operator):
    """ Set the frame range of each selected group from the scene """
    bl_idname = "scene.set_selected_groups_range"
    bl_label = "Set selected groups range from scene"

    def execute(self, context):
        for export_group in context.scene.alembic_export_groups:
            if not export_group.group_selected:
                continue

            export_group.settings.start = context.scene.frame_start
            export_group.settings.end = context.scene.frame_end

        return {"FINISHED"}
