import bpy
import inspect
from . import util


class VIEW3D_OT_ObjectReferenceChecker(bpy.types.Operator):
    bl_idname = "taremin.object_reference_checker"
    bl_label = 'Check'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = util.get_settings(context)
        target_obj = context.active_object

        settings.found_reference.clear()
        settings.current_object = target_obj

        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                for (attr_name, attr_value) in self.get_attr(mod):
                    if attr_value is target_obj:
                        prop = settings.found_reference.add()
                        prop.object_name = obj.name
                        prop.modifier_name = mod.name
                        prop.attribute_name = attr_name

        return {'FINISHED'}

    def get_attr(self, obj):
        return inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))


class VIEW3D_OT_ObjectReferenceCheckerSwitchObject(bpy.types.Operator):
    bl_idname = "taremin.object_reference_checker_switch_object"
    bl_label = 'Switch'
    bl_options = {'REGISTER', 'UNDO'}

    object_name: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        if self.object_name != "":
            obj = bpy.data.objects[self.object_name]
            context.window.view_layer.objects.active = obj
            obj.select_set(True)

        return {'FINISHED'}


class VIEW3D_OT_ObjectReferenceCheckerApplyModifier(bpy.types.Operator):
    bl_idname = "taremin.object_reference_checker_apply_modifier"
    bl_label = 'Apply'
    bl_options = {'REGISTER', 'UNDO'}

    object_name: bpy.props.StringProperty(options={'HIDDEN'})
    modifier_name: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        settings = util.get_settings(context)

        bpy.ops.object.select_all(action='DESELECT')

        obj = bpy.data.objects[self.object_name]
        context.window.view_layer.objects.active = obj
        obj.select_set(True)

        if obj.type == "MESH" and obj.data.shape_keys and hasattr(bpy.types, "OBJECT_OT_apply_selected_modifier"):
            bv = []
            for mod_index in range(len(obj.modifiers)):
                bv[mod_index] = obj.modifiers[mod_index].name == self.modifier_name
            bpy.ops.object.apply_selected_modifier(bv=bv)
        else:
            bpy.ops.object.modifier_apply(modifier=self.modifier_name)

        # update list
        remove_list = []
        for (i, ref) in enumerate(settings.found_reference):
            if ref.object_name == self.object_name and ref.modifier_name == self.modifier_name:
                remove_list.append(i)
        for idx in reversed(remove_list):
            settings.found_reference.remove(idx)

        return {'FINISHED'}
