import bpy


class ObjectReferenceCheckerProps(bpy.types.PropertyGroup):
    object_name: bpy.props.StringProperty()
    modifier_name: bpy.props.StringProperty()
    attribute_name: bpy.props.StringProperty()


class ObjectReferenceCheckerPanelProps(bpy.types.PropertyGroup):
    found_reference: bpy.props.CollectionProperty(type=ObjectReferenceCheckerProps)
    index: bpy.props.IntProperty()
    current_object: bpy.props.PointerProperty(type=bpy.types.Object)
