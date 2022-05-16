import importlib
import inspect
import sys
from pathlib import Path

import bpy

bl_info = {
    'name': 'Taremin Object Reference Checker',
    'category': '3D View',
    'author': 'Taremin',
    'location': 'View 3D > Tools',
    'description': "",
    'version': (0, 0, 2),
    'blender': (2, 80, 0),
    'wiki_url': '',
    'tracker_url': '',
    'warning': '',
}

# モジュール読み込み
module_names = [
    "ops",
    "props",
    "panel",
]
namespace = globals()
for name in module_names:
    fullname = '{}.{}.{}'.format(__package__, "lib", name)
    if fullname in sys.modules:
        namespace[name] = importlib.reload(sys.modules[fullname])
    else:
        namespace[name] = importlib.import_module(fullname)


# クラスの登録
classes = [
    # このファイル内のBlenderクラス
]

for module in module_names:
    def sort_by_lineno(x):
        return inspect.getsourcelines(x[1])[1]

    def get_class(module):
        return inspect.getmembers(module, inspect.isclass)

    def is_blender_class(obj):
        return hasattr(obj, "bl_rna")

    for module_class in [obj for name, obj in sorted(get_class(namespace[module]), key=sort_by_lineno) if is_blender_class(obj)]:
        classes.append(module_class)


def register():
    for value in classes:
        retry = 0
        while True:
            try:
                bpy.utils.register_class(value)
                break
            except ValueError:
                bpy.utils.unregister_class(value)
                retry += 1
                if retry > 1:
                    break
    props = namespace["props"]
    bpy.types.Scene.taremin_orc = bpy.props.PointerProperty(
        type=props.ObjectReferenceCheckerPanelProps)


def unregister():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass
    del bpy.types.Scene.taremin_orc
    Path(__file__).touch()


if __name__ == '__main__':
    register()
