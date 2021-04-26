# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Add-ons Grouper",
    "author" : "Rovh",
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : ".Add-ons"
}



import bpy
import addon_utils
import pickle
from bpy.app.handlers import persistent

from bpy.types import (
    Operator,
    AddonPreferences,
)

from bpy.props import (
    BoolProperty,
    )

from .Addons_Groups_List import *
from .Addons_List import *



custom_scene_name = ".Addons_Helper_Data"

class Addons_Helper_Preferences (AddonPreferences):
 
    bl_idname = __name__

    # preferences = bpy.context.preferences.addons[__name__].preferences

    # bpy.context.preferences.addons[__name__].addons_helper_list = CollectionProperty(type=Notes_List_Collection)

    # addons_helper_list: CollectionProperty(type=Notes_List_Collection)

    # t: IntProperty()

    # bpy.types.Scene.addons_list = CollectionProperty(type=Addons_List_Collection)


    def draw(self, context):
            
        layout = self.layout
        scene = bpy.context.scene

        rows = 2
        row = layout.row()
        row.template_list("ADDONS_GROUPER_LIST_UL_items", "", scene, "addons_helper_list", scene, "addons_helper_list_index", rows=rows)

        col = row.column(align=True)
        col.scale_x = 1.1
        col.scale_y = 1.2

        col.operator("addons_helper_list.list_action_add", icon='ADD', text="")
        col.operator("addons_helper_list.list_action_remove", icon='REMOVE', text="")
        # col.operator("addons_helper_list.list_action", icon='REMOVE', text="").action = 'REMOVE'
        
        col.separator(factor = 0.4)

        col.operator("addons_helper_list.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("addons_helper_list.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        # col.separator(factor = 0.4)

        # col.operator('window_manager.export_note_text', text = '', icon = 'IMPORT').action = 'scene*'

        # col.separator(factor = 0.4)

        # col.operator('window_manager.export_note_text', text = '', icon = 'EXPORT').action = 'scene_get*'

        col.separator(factor = 0.4)


        

        col.operator("addons_helper_list.clear_list", icon="TRASH", text = "")
        # row = layout.row()
        # col = row.column(align=True)
        # row = col.row(align=True)
        # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")

class Addons_Helper_Bool(Operator):
    """Tooltip"""
    bl_idname = "window_manager.bool"
    bl_label = ""
    bl_description = 'Display Noter Splash Screen on startup \n\n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut'
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}

    
    def execute(self, context):

        if bpy.data.scenes.find(custom_scene_name) == -1:
            bpy.data.scenes.new(custom_scene_name)


        if bpy.data.scenes[custom_scene_name].splash_screen == True:
            bpy.data.scenes[custom_scene_name].splash_screen = False
        else:
            bpy.data.scenes[custom_scene_name].splash_screen = True

            
                
        
        # if bpy.context.scene.splash_screen == True:
        #     for i in bpy.data.scenes:
        #         i.splash_screen = False
        # else:
        #     for i in bpy.data.scenes:
        #         i.splash_screen = True

        return {'FINISHED'}

class Addons_Helper_Open_Browser_Or_Folder(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_helper.open_browser_or_folder"
    bl_label = ""
    bl_description = "open browser or folder"
    bl_options = {'REGISTER'}

    link: StringProperty()

    def execute(self, context):

        bpy.ops.wm.url_open(url = self.link )

        return {"FINISHED"}

bool_swith = True

class Addons_Helper_Switch(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_helper.switch"
    bl_label = ""
    bl_description = "open browser or folder"
    bl_options = {'REGISTER'}

    group_index: IntProperty()

    group_index__and__action: StringProperty()


    def execute(self, context):

        keyword = "_"
        before_keyword, keyword, after_keyword = self.group_index__and__action.partition(keyword)
            
        self.group_index = int(before_keyword)
        action = after_keyword

        for item in bpy.context.scene.addons_list:

            if item.index_from_group == self.group_index:
                
                module_name = find_addon_name(item.text, module_name=True)
                
                prefs = context.preferences
                used_ext = {ext.module for ext in prefs.addons}
                
                is_enabled = module_name in used_ext

            

                if action == "ENABLE":
                    if is_enabled == False:
                        addon_utils.enable(
                        module_name, default_set=1, persistent=0, handle_error=None)
                
                else:
                    if is_enabled == True:
                        addon_utils.disable(
                        module_name, default_set=1,handle_error=None)
            

            
        # if bool_swith == True:
        #     bool_swith = False
        # else:
        #     bool_swith = True






        # Typically its enough to call:
        # import addon_utils
        # addon_utils.enable("my_addon")
        # addon_utils.disable("my_addon")

        return {"FINISHED"}

class Addons_Helper_Pickle(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_helper.pickle"
    bl_label = "Remove"
    bl_description = "Pickle"
    bl_options = {'INTERNAL'}

    action: bpy.props.EnumProperty(
        items=(
            ("EXPORT", "Export", ""),
            ("IMPORT", "Import", ""),
            ))

    def execute(self, context):
        
        # [   [('symbols', 0), ('name', '1111')],    [], [('name', '1111'), ('symbols', 3)]]

        if self.action == "IMPORT":

            with open('saved_data_Addons_Groups_List.pickle', 'rb') as f:
                data = pickle.load(f)

            length_data = len(data)
            length_addons_helper_list = len(context.scene.addons_helper_list)

            if length_data > length_addons_helper_list:
                length = length_data - length_addons_helper_list
                for _ in range(length):
                    context.scene.addons_helper_list.add()
                

            for index, element in enumerate(data):

                for i in element:

                    name = i[0]
                    value = i[1]

                    bpy.context.scene.addons_helper_list[index][name] = value

                    # print(name, value)




            with open('saved_data_Addons_List.pickle', 'rb') as f:
                data = pickle.load(f)

            length_data = len(data)
            length_addons_list = len(context.scene.addons_list)



            if length_data > length_addons_list:
                length = length_data - length_addons_list
                for _ in range(length):
                    context.scene.addons_list.add()


            for index, element in enumerate(data):

                for i in element:

                    name = i[0]
                    value = i[1]

                    bpy.context.scene.addons_list[index][name] = value

                    # print(name, value)
        
        elif self.action == "EXPORT":


            data = []
            for i in bpy.context.scene.addons_helper_list:
                data.append( i.items() )

            with open('saved_data_Addons_Groups_List.pickle', 'wb') as f:
                pickle.dump(data, f)

            # with open('saved_data_Addons_Groups_List.pickle', 'rb') as f:
            #     data_new = pickle.load(f)
            # print(data_new)


            data = []
            for i in bpy.context.scene.addons_list:
                data.append( i.items() )

            with open('saved_data_Addons_List.pickle', 'wb') as f:
                pickle.dump(data, f)

            # with open('saved_data_Addons_List.pickle', 'rb') as f:
            #     data_new = pickle.load(f)
            # print(data_new)



        return {"FINISHED"}  


# class Addons_Helper_(Operator):
#     """Move items up and down, add and remove"""
#     bl_idname = "addons_helper.open_browser_or_folder"
#     bl_label = ""
#     bl_description = "open browser or folder"
#     bl_options = {'REGISTER'}

#     link: StringProperty()

#     def execute(self, context):

#         bpy.ops.wm.url_open(url = self.link )

#         return {"FINISHED"}

@persistent
def load_handler(dummy):

    # print(11111111111111111111) 

    try:
        bpy.ops.addons_helper.pickle(action = "IMPORT")
    except RuntimeError:
        pass

    bpy.app.handlers.load_post.remove(load_handler)

# @persistent
# def end_handler(dummy):

#     try:
#         bpy.ops.addons_helper.pickle(action = "EXPORT")
#     except RuntimeError:
#         pass

#     bpy.app.handlers.load_post.remove(end_handler)




blender_classes = [

    Addons_Helper_Preferences,
    Addons_Helper_Bool,
    Addons_Helper_Open_Browser_Or_Folder,
    Addons_Helper_Switch,
    Addons_Helper_Pickle,
]

blender_classes = \
    blender_classes \
    + blender_classes_Addons_Groups_List \
    + blender_classes_Addons_List


def register():

    bpy.types.Scene.splash_screen = BoolProperty()

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


    bpy.types.Scene.addons_helper_list = CollectionProperty(type=Notes_List_Collection)
    bpy.types.Scene.addons_helper_list_index = IntProperty()

    bpy.types.Scene.addons_list = CollectionProperty(type=Addons_List_Collection)
    bpy.types.WindowManager.addons_list_index = IntProperty()

    # bpy.ops.addons_helper.pickle('IMPORT', "INVOKE_DEFAULT")
    # bpy.ops.addons_helper.pickle("INVOKE_DEFAULT")

    # pickle_action(action = "IMPORT")

    bpy.app.handlers.load_post.append(load_handler)

    # bpy.ops.addons_helper.pickle(action = "IMPORT")

def unregister():

    # pickle_action(action = "EXPORT")
    # bpy.ops.addons_helper.pickle('EXPORT', "INVOKE_DEFAULT")

    # bpy.app.handlers.load_post.append(end_handler)

    bpy.ops.addons_helper.pickle(action = "EXPORT")

    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.Scene.splash_screen

    del bpy.types.Scene.addons_helper_list
    del bpy.types.Scene.addons_helper_list_index

    del bpy.types.Scene.addons_list
    del bpy.types.WindowManager.addons_list_index

    


    
if __name__ == "__main__":
    register()
