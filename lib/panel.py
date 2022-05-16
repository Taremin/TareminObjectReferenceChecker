import bpy
import inspect
from . import ops, util


def get_attr(obj):
    return inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))


class VIEW3D_PT_ObjectReferenceCheckerPanel(bpy.types.Panel):
    bl_label = 'Object Reference Checker'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'
    bl_category = 'Taremin'

    def draw(self, context):
        layout = self.layout
        settings = util.get_settings(context)

        row = layout.row()
        col = row.column()
        col.prop(settings, "current_object", text="")
        col.enabled = False

        if context.active_object is None:
            return

        col = row.column()
        active = col.operator(
            ops.VIEW3D_OT_ObjectReferenceCheckerSwitchObject.bl_idname,
            text="",
            icon='RESTRICT_SELECT_OFF'
        )
        if settings.current_object is not None:
            active.object_name = settings.current_object.name
            col.enabled = True
        else:
            col.enabled = False

        row = layout.row()
        col = row.column()

        col.template_list(
            listtype_name="VIEW3D_UL_ObjectReferenceChecker",
            list_id="",
            dataptr=settings,
            propname="found_reference",
            active_dataptr=settings,
            active_propname="index",
            type="DEFAULT",
        )

        layout.operator(ops.VIEW3D_OT_ObjectReferenceChecker.bl_idname)


class VIEW3D_UL_ObjectReferenceChecker(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.ui_units_x = 1.0

        col = layout.column()
        row = col.row()
        row.label(text=item.object_name, translate=False)
        row.label(text=item.modifier_name, translate=False)

        col = row.row(align=True)
        active = col.operator(
            ops.VIEW3D_OT_ObjectReferenceCheckerSwitchObject.bl_idname,
            text="",
            icon='RESTRICT_SELECT_OFF'
        )
        active.object_name = item.object_name

        apply = col.operator(
            ops.VIEW3D_OT_ObjectReferenceCheckerApplyModifier.bl_idname,
            text="",
            icon='MODIFIER'
        )
        apply.object_name = item.object_name
        apply.modifier_name = item.modifier_name
