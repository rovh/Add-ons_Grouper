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
    "description" : "Add-ons Grouper is an add-on created to simplify and extend the management of add-ons by creating add-ons groups and using additional options.",
    "blender" : (3, 0, 0),
    "version" : (1,0),
    "location" : "",
    "warning" : "",
    "category" : ".Add-ons",
    "wiki_url": "https://github.com/rovh/Add-ons_Grouper",
    "tracker_url": "https://github.com/rovh/Add-ons_Grouper/issues",
}



import bpy
import addon_utils
import pickle
from bpy.app.handlers import persistent
import os
import pathlib

from bpy.types import (
    Operator,
    AddonPreferences,
)

from bpy.props import (
    BoolProperty,
    )

from .Addons_Groups_List import *
from .Addons_List import *



custom_scene_name = ".Addons_Grouper_Data"

class Addons_Grouper_Preferences (AddonPreferences):
 
    bl_idname = __name__

    # preferences = bpy.context.preferences.addons[__name__].preferences

    # bpy.context.preferences.addons[__name__].addons_groups_list = CollectionProperty(type=Notes_List_Collection)

    # addons_groups_list: CollectionProperty(type=Addons_Groups_List_Collection)

    # t: IntProperty()

    # bpy.types.Scene.addons_list = CollectionProperty(type=Addons_List_Collection)

    auto_enable_disable: BoolProperty(name = "Auto enable/disable on Blender start", description = \
        """This parameter is responsible for automatically enabling add-ons with selected "Auto enable/disable" option.\
        \nFor example, if you open a .blend file, the add-ons with marked "Auto enable/disable" option will be enabled/disabled with Blender start.\
        \nAttention: this function only works if you open .blend file directly, if you do not open it directly*, then "Auto enable/disable on Blender start" will not work.\
        \n * This means that you do not first open Blender and then create or open the desired file, but select it directly.
        """)

    def draw(self, context):
        wm = context.window_manager
            
        layout = self.layout

        row = layout.row(align = 1)

        row_left = row.row()
        row_left.operator("addons_grouper.pickle", icon='FILE_REFRESH', text="").action = "IMPORT"
        row_left.scale_x = 10
        row_left.alignment = "LEFT"


        row_right = row.row(align = 1)
        row_right.operator("addons_grouper.switch_2", icon='CHECKBOX_HLT', text="")
        # row_right.separator(factor = .5)
        row_right.scale_x = 1.35
        row_right.scale_y = 1.2
        row_right.alignment = "RIGHT"
        

        rows = 2
        row = layout.row(align = 1)
        row.template_list("ADDONS_GROUPS_LIST_UL_items", "", wm, "addons_groups_list", wm, "addons_groups_list_index", rows=rows)

        col = row.column(align=True)
        col.scale_x = 1.1
        col.scale_y = 1.2

        col.operator("addons_groups_list.list_action_add", icon='ADD', text="")
        col.operator("addons_groups_list.list_action_remove", icon='REMOVE', text="")
        # col.operator("addons_groups_list.list_action", icon='REMOVE', text="").action = 'REMOVE'
        
        col.separator(factor = 0.4)

        col.operator("addons_groups_list.list_action", icon='TRIA_UP', text="").action = 'UP'
        col.operator("addons_groups_list.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

        # col.separator(factor = 0.4)

        # col.operator('window_manager.export_note_text', text = '', icon = 'IMPORT').action = 'scene*'

        # col.separator(factor = 0.4)

        # col.operator('window_manager.export_note_text', text = '', icon = 'EXPORT').action = 'scene_get*'

        col.separator(factor = 0.4)


        

        col.operator("addons_groups_list.clear_list", icon="TRASH", text = "")

        col.separator(factor = 4)



        # row = col.row(align = 1)
        # row.operator("addons_grouper.switch_2", icon='CHECKBOX_HLT', text="")
        # row.scale_y = 2
        # row.alignment = "CENTER"
        
        col.separator(factor = 2)

        
        row = col.row(align = 0)
        row.prop(self, "auto_enable_disable", icon='QUIT', text="")
        row.scale_x = .9
        row.scale_y = .9
        row.alignment = "CENTER"


        row = col.row(align = 0)
        row.operator("addons_grouper.pop_up_menu", icon='INFO', text="")
        row.scale_x = .9
        row.scale_y = .9
        row.alignment = "CENTER"

        # row = layout.row()
        # col = row.column(align=True)
        # row = col.row(align=True)
        # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")

class Addons_Grouper_Open_Browser_Or_Folder(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_grouper.open_browser_or_folder"
    bl_label = "Open link in browser or folder"
    bl_description = "Open the link that is specified in the active(selected) add-on"
    bl_options = {'REGISTER'}

    # link: StringProperty()

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return bool(wm.addons_list)

    def execute(self, context):

        wm = context.window_manager

        try:
            link = wm.addons_list[wm.addons_list_index].addon_link
        except IndexError:
            pass
        else:
            bpy.ops.wm.url_open(url = link )
        # bpy.ops.wm.url_open(url = "R" )

        return {"FINISHED"}

class Addons_Grouper_Switch_2(Operator):
    bl_idname = "addons_grouper.switch_2"
    bl_label = ""
    bl_description = 'Enable or Disable Group depending on "Auto enable/disable" option'
    bl_options = {'REGISTER'}

    use_refresh: BoolProperty()

    @classmethod
    def description(cls, context, properties):

        if  properties.use_refresh == True:
            return 'Refresh and Enable or Disable Group depending on "Auto enable/disable" option'
        else:
            return 'Enable or Disable Group depending on "Auto enable/disable" option'


    def execute(self, context):

        if self.use_refresh == True:

            bpy.ops.addons_grouper.pickle(action='IMPORT', condition = True)

        auto_enable_disable()

        text = "Add-ons were refreshed"
        self.report( {"INFO"}, text)

        return {"FINISHED"}

class Addons_Grouper_Switch(Operator):
    bl_idname = "addons_grouper.switch"
    bl_label = ""
    bl_description = "Enable or Disable All Add-ons in this group"
    bl_options = {'REGISTER'}

    group_index: IntProperty()

    action: StringProperty()

    auto_enable_disable: BoolProperty()

    auto_enable_disable_list: StringProperty()

    def execute(self, context):

        wm = context.window_manager


        if self.auto_enable_disable == True:

            if  bpy.data.scenes.find(custom_scene_name) == -1:
                bpy.data.scenes.new(custom_scene_name)
            
                # auto_enable_list = bpy.data.scenes[custom_scene_name].auto_enable_list
                # auto_disable_list = bpy.data.scenes[custom_scene_name].auto_disable_list
                
                # if bool(auto_enable_list) == True:               
                #     auto_list = auto_enable_list
                # elif bool(auto_disable_list) == True:
                #     auto_list = auto_disable_list
                # else:
                #     return {"FINISHED"}

            auto_list = self.auto_enable_disable_list

            action = self.action

            auto_list  = auto_list.split(".")
            try:
                auto_list.pop(0)
                auto_list.pop(-1)
            except IndexError:
                pass


            for group_index in auto_list:

                group_index = int(group_index)

                for item in wm.addons_list:

                    if group_index == item.index_from_group:

                        module_name = find_addon_name(item.text, module_name=True)

                        if bool(module_name) == True:
                        
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

        else:
               

            group_index = self.group_index
            action = self.action


            for item in wm.addons_list:

                if item.index_from_group == self.group_index:
                    
                    module_name = find_addon_name(item.text, module_name=True)

                    if bool(module_name) == True:
                    
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



        # Typically its enough to call:
        # import addon_utils
        # addon_utils.enable("my_addon")
        # addon_utils.disable("my_addon")

        return {"FINISHED"}

class Addons_Grouper_Pickle(Operator):
    bl_idname = "addons_grouper.pickle"
    bl_label = "Refresh"
    bl_description = "If for some reason the created groups are not displayed, then this button should help"
    bl_options = {'INTERNAL'}

    action: bpy.props.EnumProperty(
        items=(
            ("EXPORT", "Export", ""),
            ("IMPORT", "Import", ""),
            ))

    condition: BoolProperty()

    refresh: BoolProperty()

    def execute(self, context):

        wm = context.window_manager

        # print(wm.addons_groups_list.items())

        file_folder_path_absolute = pathlib.Path(__file__).parent.absolute()
        
        if self.condition == True:
            
            if bool(wm.addons_groups_list) == False:
                text = "Add-ons will be refreshed"
                self.report( {"INFO"}, text)
            else:
                return {"FINISHED"} 

        # [   [('symbols', 0), ('name', '1111')],    [], [('name', '1111'), ('symbols', 3)]]

        if self.action == "IMPORT":

            
            file_folder_path = os.path.join(file_folder_path_absolute, 'saved_data_Addons_Groups_List.pickle')
            with open(file_folder_path, 'rb') as f:
                data = pickle.load(f)



            length_data = len(data)
            length_addons_helper_list = len(wm.addons_groups_list)

            if length_data > length_addons_helper_list:
                length = length_data - length_addons_helper_list
                for _ in range(length):
                    wm.addons_groups_list.add()
                



            for index, element in enumerate(data):

                for i in element:

                    name = i[0]
                    value = i[1]

                    wm.addons_groups_list[index][name] = value

                    # print(name, value)

                # wm.addons_groups_list[0]["auto_enable"].remove()
                # wm.addons_groups_list[0]["auto_enable"].remove()



            file_folder_path = os.path.join(file_folder_path_absolute, 'saved_data_Addons_List.pickle')
            with open(file_folder_path, 'rb') as f:
                data = pickle.load(f)

            length_data = len(data)
            length_addons_list = len(wm.addons_list)



            if length_data > length_addons_list:
                length = length_data - length_addons_list
                for _ in range(length):
                    wm.addons_list.add()


            for index, element in enumerate(data):

                for i in element:

                    name = i[0]
                    value = i[1]

                    wm.addons_list[index][name] = value

                    # print(name, value)
        
        elif self.action == "EXPORT":


            data = []
            for i in wm.addons_groups_list:
                data.append( i.items() )
            

            file_folder_path = os.path.join(file_folder_path_absolute, 'saved_data_Addons_Groups_List.pickle')
            with open(file_folder_path, 'wb') as f:
                pickle.dump(data, f)



            data = []
            for i in wm.addons_list:
                data.append( i.items() )


            file_folder_path = os.path.join(file_folder_path_absolute, 'saved_data_Addons_List.pickle')
            with open(file_folder_path, 'wb') as f:
                pickle.dump(data, f)


        if self.refresh == True:
            bpy.ops.addons_list.list_move( group_index = wm.addons_groups_list_index)

        return {"FINISHED"}  

class Pop_Up_Operator(Operator):
    bl_idname = "addons_grouper.pop_up_menu"
    bl_label = ""
    bl_description = "Tip Menu"

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        col = layout.column(align = 1)

        col.label(text = '''If you don't want changes to the enabled and disabled add-ons to be saved, you can enable''')
        col.label(text = 'manual saving (Blender Preferences window >> bottom left corner >> "Save & Load" menu >> "Auto-Save Preferences").' )
        col.label(text = 'Then the changes will be saved only when the save button is clicked.')
        col.separator(factor = 1.5)
        col.label(text = 'But be careful: If you make changes in Blender Preferences, you may need to click "Save Preferences" button.')
        col.label(text = '''If there are changes that need to be saved, an icon(*) will appear next to the button name.''')



    def invoke(self, context, event): 
        # preferences = bpy.context.preferences.addons[__name__].preferences
        # height = bpy.context.window.height
        # width = bpy.context.window.width


        

        # if location_cursor == True:
            # return context.window_manager.invoke_props_dialog(self, width = width_menu)
        # else:

            # x = event.mouse_x
            # y = event.mouse_y 

            # location_x = width  * preferences.pop_up_menus_location_x
            # location_y = height * preferences.pop_up_menus_location_y

            # bpy.context.window.cursor_warp(location_x , location_y)


        invoke = context.window_manager.invoke_props_dialog(self, width = 700)

        # invoke = context.window_manager.invoke_props_dialog(self, width=width_menu)
        # return context.window_manager.invoke_popup(self, width=700)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_props_popup(self, event)
        # return context.window_manager.invoke_confirm(self, event)


        # bpy.context.window.cursor_warp(x , y)

        return invoke




def finding(sufix, place_name, enable):

    sufix_2 = "." + sufix + "."
    sufix_3 = sufix + "."
    sufix_4 = "." + sufix

    x = place_name 

    find = bpy.data.scenes[custom_scene_name][x].find(sufix_2)

    if enable == True:

        if find == -1:
            
            if len(bpy.data.scenes[custom_scene_name][x]) == 0:
                
                bpy.data.scenes[custom_scene_name][x] += sufix_2
            else:

                bpy.data.scenes[custom_scene_name][x] += sufix_3
        
    else:

        if find == 0:
            bpy.data.scenes[custom_scene_name][x] = bpy.data.scenes[custom_scene_name][x].replace(sufix_4, "")
        else:
            bpy.data.scenes[custom_scene_name][x] = bpy.data.scenes[custom_scene_name][x].replace(sufix_3, "") 

        if len(bpy.data.scenes[custom_scene_name][x]) < 3:
            bpy.data.scenes[custom_scene_name][x] = ""

def extra_draw(self, context):

    layout = self.layout

    layout.separator(factor = .9)

    row = layout.row(align = 1)
    
    op = row.operator("addons_grouper.switch_2", icon='CHECKBOX_HLT', text="", emboss = 0)
    op.use_refresh = True
    # row.separator(factor = .7)

    # row.operator("addons_grouper.switch_2", icon='CHECKBOX_HLT', text="", emboss = 0)



class Addons_Grouper_List_auto_enable_disable_list(Operator):
    bl_idname = "addons_grouper.auto_enable_disable_list"
    bl_label = "Auto enable/disable"
    bl_description = ""
    bl_options = {'REGISTER'}

    group_index: IntProperty()

    action: StringProperty()

    @classmethod
    def description(cls, context, properties):

        if  properties.action == 'enable':
            return "Enable add-ons from this group when you start Blender\
                    \nand disable when you close Blender"

        elif properties.action  == 'disable':
            return "Disable add-ons from this group when you start Blender \
                    \nand enable when you close Blender"



    def execute(self, context):

        if bpy.data.scenes.find(custom_scene_name) == -1:
            bpy.data.scenes.new(custom_scene_name)

        wm = context.window_manager
            

        group_index = self.group_index
        action = self.action



        auto_enable_list = 'auto_enable_list'
        auto_enable = 'auto_enable'

        auto_disable_list = 'auto_disable_list'
        auto_disable = 'auto_disable'

        if action == "enable":
            x = auto_enable_list
            y = auto_enable

            x_2 = auto_disable_list
            y_2 = auto_disable

        elif action == "disable":
            x = auto_disable_list
            y = auto_disable

            x_2 = auto_enable_list
            y_2 = auto_enable



    
        """auto_enable"""
        try:
            wm.addons_groups_list[group_index][auto_enable]
        except KeyError:
            wm.addons_groups_list[group_index][auto_enable] = wm.addons_groups_list[group_index].auto_enable


        """auto_enable_list"""
        try:
            bpy.data.scenes[custom_scene_name][auto_enable_list]
        except KeyError:
            bpy.data.scenes[custom_scene_name][auto_enable_list] = bpy.data.scenes[custom_scene_name].auto_enable_list


        """auto_disable"""
        try:
            wm.addons_groups_list[group_index][auto_disable]
        except KeyError:
            wm.addons_groups_list[group_index][auto_disable] = wm.addons_groups_list[group_index].auto_disable


        """auto_disable_list"""
        try:
            bpy.data.scenes[custom_scene_name][auto_disable_list]
        except KeyError:
            bpy.data.scenes[custom_scene_name][auto_disable_list] =bpy.data.scenes[custom_scene_name].auto_disable_list




        if wm.addons_groups_list[group_index][y] == True:
            wm.addons_groups_list[group_index][y] = False
            enable = False

        elif wm.addons_groups_list[group_index][y] == False:
            wm.addons_groups_list[group_index][y] = True
            wm.addons_groups_list[group_index][y_2] = False
            enable = True
    



        sufix = str(group_index)
        
        if enable == True:
            finding(sufix = sufix, place_name = x, enable = enable)
            finding(sufix = sufix, place_name = x_2, enable = not enable)
        elif enable == False:
            finding(sufix = sufix, place_name = x, enable = enable)

        


        # print()
        # print()
        # print(bpy.data.scenes[custom_scene_name][x], y) 
        # print(bpy.data.scenes[custom_scene_name][x_2], y_2) 

        






        # if len(bpy.data.scenes[custom_scene_name].auto_enable_list) != 0:
        #     split_list_before = bpy.data.scenes[custom_scene_name].auto_enable_list.split(".")
        #     length_before = len(split_list_before)
        # else:
        #     length_before = 0
     





        # if len(bpy.data.scenes[custom_scene_name].auto_enable_list) == 0:
        #     sufix = str(group_index)
        #     auto_enable_list_maybe = str(group_index)
        # else:
        #     sufix = "." + str(group_index)
        #     sufix_2 =  str(group_index)
        #     auto_enable_list_maybe = bpy.data.scenes[custom_scene_name].auto_enable_list + sufix

        





        # if len(auto_enable_list_maybe) != 0:
        #     split_list_after = auto_enable_list_maybe.split(".")
        #     split_list_after = set(split_list_after)
        #     length_after = len(split_list_after)
        # else:
        #     length_after = 0




        # if length_after > length_before:
        #     bpy.data.scenes[custom_scene_name].auto_enable_list = auto_enable_list_maybe
        # else:
        #     if length_before == 1:
        #         bpy.data.scenes[custom_scene_name].auto_enable_list = bpy.data.scenes[custom_scene_name].auto_enable_list.replace(sufix_2, "") 
        #     bpy.data.scenes[custom_scene_name].auto_enable_list = bpy.data.scenes[custom_scene_name].auto_enable_list.replace(sufix, "")





        # split_list = bpy.data.scenes[custom_scene_name].auto_enable_list.split(".")
        # print (bpy.data.scenes[custom_scene_name].auto_enable_list)
          
        # print(split_list)
        # print()
        # print()
        # print(length_before)
        # print(length_after)



               
        return {"FINISHED"}



def auto_enable_disable( reverse = False):
    if  bpy.data.scenes.find(custom_scene_name) != -1:

        auto_enable_list = bpy.data.scenes[custom_scene_name].auto_enable_list
        auto_disable_list = bpy.data.scenes[custom_scene_name].auto_disable_list

        if bool(auto_enable_list) == True:

            action = "ENABLE" if reverse == False else "DISABLE"

            bpy.ops.addons_grouper.switch(auto_enable_disable = True, action = action, auto_enable_disable_list = auto_enable_list)

        if bool(auto_disable_list) == True:

            action = "DISABLE" if reverse == False else "ENABLE"

            bpy.ops.addons_grouper.switch(auto_enable_disable = True, action = action, auto_enable_disable_list = auto_disable_list)



@persistent
def load_handler(dummy):

    # try:
    #     bpy.ops.addons_grouper.pickle(action = "IMPORT")
    # except RuntimeError:
    #     pass

    bpy.ops.addons_grouper.pickle(action = "IMPORT")

    if bpy.context.preferences.addons[__name__].preferences.auto_enable_disable:
        auto_enable_disable(reverse = False)
        
    bpy.app.handlers.load_post.remove(load_handler)

# @persistent
# def end_handler(dummy):

#     try:
#         bpy.ops.addons_grouper.pickle(action = "EXPORT")
#     except RuntimeError:
#         pass

#     bpy.app.handlers.load_post.remove(end_handler)




blender_classes = [

    Addons_Grouper_Preferences,
    Addons_Grouper_Open_Browser_Or_Folder,
    Addons_Grouper_Switch,
    Addons_Grouper_Switch_2,
    Addons_Grouper_Pickle,
    Addons_Grouper_List_auto_enable_disable_list,
    Pop_Up_Operator,
]

blender_classes = \
    blender_classes \
    + blender_classes_Addons_Groups_List \
    + blender_classes_Addons_List


def register():

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

    bpy.types.Scene.auto_enable_list = StringProperty()
    bpy.types.Scene.auto_disable_list = StringProperty()

    bpy.types.WindowManager.addons_groups_list = CollectionProperty(type=Addons_Groups_List_Collection)
    bpy.types.WindowManager.addons_groups_list_index = IntProperty(name = "Add-on")

    bpy.types.WindowManager.addons_list = CollectionProperty(type=Addons_List_Collection)
    bpy.types.WindowManager.addons_list_index = IntProperty(name = "Add-on")

    # bpy.ops.addons_grouper.pickle('IMPORT', "INVOKE_DEFAULT")
    # bpy.ops.addons_grouper.pickle("INVOKE_DEFAULT")

    # pickle_action(action = "IMPORT")

    bpy.types.TOPBAR_MT_editor_menus.append(extra_draw)


    bpy.app.handlers.load_post.append(load_handler)

    # bpy.ops.addons_grouper.pickle(action = "IMPORT")

def unregister():

    bpy.types.TOPBAR_MT_editor_menus.remove(extra_draw)

    # pickle_action(action = "EXPORT")
    # bpy.ops.addons_grouper.pickle('EXPORT', "INVOKE_DEFAULT")

    # bpy.app.handlers.load_post.append(end_handler)

    
    bpy.ops.addons_grouper.pickle(action = "EXPORT")
    if bpy.context.preferences.addons[__name__].preferences.auto_enable_disable:
        auto_enable_disable(reverse = True)
    # bpy.ops.addons_grouper.switch(action = "DISABLE", auto_enable = True)

    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.WindowManager.addons_groups_list
    del bpy.types.WindowManager.addons_groups_list_index

    del bpy.types.WindowManager.addons_list
    del bpy.types.WindowManager.addons_list_index

    del bpy.types.Scene.auto_enable_list
    del bpy.types.Scene.auto_disable_list
    


    
if __name__ == "__main__":
    register()
