import bpy
import addon_utils
import pickle


from bpy.types import (
        Panel,
        PropertyGroup,
        Operator,
        UIList,
        )

from bpy.props import (
        FloatProperty,
        BoolProperty,
        PointerProperty,
        EnumProperty,
        StringProperty,
        IntProperty,
        CollectionProperty,
        )

from . import __name__ as addon_name



custom_scene_name = ".Addons_Helper_Data"

def find_addon_name(input_text, module_name = False):
    'bpy.ops.preferences.addon_enable(module="space_view3d_3d_navigation")'

    keyword = "="
    before_keyword, keyword, after_keyword = input_text.partition(keyword)

    output_text = after_keyword

    output_text = output_text.replace('"', "")
    output_text = output_text.replace(")", "")

    # addon_name = bpy.context.preferences.addons[output_text].module.title()
    addon_name = output_text

    if module_name == False:
        try:
            mod = addon_utils.addons_fake_modules.get(addon_name)
            info = addon_utils.module_bl_info(mod)
            addon_name = info["name"]
        except AttributeError:
            pass


    return addon_name



class Addons_List_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_list.list_action"
    bl_label = ""
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            # ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "") 
            ))

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'UP':
            return "Up"
        elif properties.action == 'DOWN':
            return "Down"

    def invoke(self, context, event):

        scene = context.scene
        # idx = scene.addons_list_index
        wm = context.window_manager
        idx = wm.addons_list_index

        try:
            item = wm.addons_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(wm.addons_list) - 1:
                wm.addons_list.move(idx, idx+1)
                wm.addons_list_index += 1

            elif self.action == 'UP' and idx >= 1:
                wm.addons_list.move(idx, idx-1)
                wm.addons_list_index -= 1
                

        return {"FINISHED"}
class Addons_List_list_move(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_list.list_move"
    bl_label = ""
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    group_index: IntProperty()

    index_from_add_action: BoolProperty()


    def execute(self, context):

        count = 0

        scene = context.scene
        wm = context.window_manager

        wm.addons_groups_list_index = self.group_index

        for index, element in enumerate(wm.addons_list):
            if element.index_from_group != self.group_index:

                for i in range(    index + 1,    len(wm.addons_list)   ):
                    if wm.addons_list[i].index_from_group == self.group_index:

                        idx = i

                        wm.addons_list.move(  idx, index )

                        
            else:
                if self.index_from_add_action:
                    count += 1

            wm.addons_list_index = count



        #     if self.action == 'DOWN' and idx < len(scene.addons_list) - 1:
                
        #         scene.addons_list_index += 1

        #     elif self.action == 'UP' and idx >= 1:
        #         scene.addons_list.move(idx, idx-1)
        #         scene.addons_list_index -= 1
                

        return {"FINISHED"}
class Addons_List_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_list.list_action_add"
    bl_label = ""
    bl_description = "Add item"
    bl_options = {'REGISTER'}

    group_index: IntProperty()

    @classmethod
    def description(cls, context, properties):
        return "Add"

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager
        # idx = scene.addons_list_index
        idx = wm.addons_list_index

        try:
            item = wm.addons_list[idx]
        except IndexError:
            pass

        item = wm.addons_list.add()

        # scene.addons_list_index = len(scene.addons_list) - 1

        item.index_from_group = self.group_index

        # bpy.ops.addons_list.list_move(group_index = self.group_index)

        # bpy.ops.addons_list.list_move(index_from_add_action = True)

        bpy.ops.addons_list.list_move(group_index = self.group_index, index_from_add_action = True)
        
        

        return {"FINISHED"}       
class Addons_List_actions_remove(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_list.list_action_remove"
    bl_label = "Remove"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    group_index: IntProperty()

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return bool(wm.addons_list)
                

    def invoke(self, context, event):

        wm = context.window_manager
        scene = context.scene
        idx = scene.addons_list_index
        # idx = wm.addons_list_index
        if wm.addons_list[idx].index_from_group == self.group_index:
            return context.window_manager.invoke_confirm(self, event)
        else:
            return {"FINISHED"}  

        

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_list_index
        
        if idx == 0:
            wm.addons_list_index = 0
        else:
            wm.addons_list_index -= 1
        
        wm.addons_list.remove(idx)

        return {"FINISHED"}  
class Addons_List_find(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_list.find"
    bl_label = "Remove"
    bl_description = "Find"
    bl_options = {'INTERNAL'}

    module_name: StringProperty


    def execute(self, context):
    

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_list_index

        try:
            item = wm.addons_list[idx]
        except IndexError:
            pass

        
        module_name = find_addon_name(item.text, module_name = True)

        bpy.ops.preferences.addon_show(module = module_name)

        return {"FINISHED"}  



class ADDONS_LIST_UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scene = context.scene
        wm = context.window_manager

        try:
            item = wm.addons_list[index]
        except IndexError:
            pass
        

        # item.index_copy = index

 
        # t = text_function(item.text)

        # addons = [
        #     (mod, addon_utils.module_bl_info(mod))
        #     for mod in addon_utils.modules(refresh=False)
        # ]

        # for mod, info in addons:
        #     _


        # for module in addon_utils.modules():
                # info = addon_utils.module_bl_info(t)

        # t = addon_utils.module_bl_info(t)

        # modules = addon_utils.modules(refresh=False)

        # my_info = None
        # for module in addon_utils.modules():
        #         info = addon_utils.module_bl_info(module)


        # if item.index_from_group != scene.addons_groups_list_index:

                # idx = index

                # if self.action == 'DOWN' and idx < len(scene.addons_list) - 1:
                # scene.addons_list.move( idx, (len(scene.addons_list) ) )
                # scene.addons_list_index += 1

                # elif self.action == 'UP' and idx >= 1:
                # scene.addons_list.move(idx, idx-1)
                # scene.addons_list_index -= 1

    
        
        if item.index_from_group == wm.addons_groups_list_index:
                                     
                
                


                if index == wm.addons_list_index:
                        ico = "TRIA_RIGHT"
                else:
                        ico = "NONE"

                


                
                
                main_row = layout.row()

                
                # userpref = context.preferences
                # used_ext = {ext.module for ext in userpref.addons}
                # for mod in addon_utils.modules(refresh=False):
                #         module_name = addon_name
                #         is_enabled = module_name in used_ext

                


                # for mod, info in addons:
                #     module_name = mod.__name__

                #     is_enabled = module_name in used_ext

                addon_name = find_addon_name(item.text, module_name=True)
                module_name = addon_name
                
                prefs = context.preferences
                used_ext = {ext.module for ext in prefs.addons}
                
                is_enabled = module_name in used_ext

                
                if module_name == "":
                        main_row.label(icon = "REMOVE")
                else:
                        main_row.operator(
                                "preferences.addon_disable" if is_enabled else "preferences.addon_enable",
                                icon='CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT', text="",
                                emboss=False,
                                ).module = module_name


                # if is_enabled:
                #         layout.operator("wm.addon_disable", 
                #                         icon='CHECKBOX_HLT', 
                #                         text=mod.bl_info["name"], 
                #                         emboss=False).module = module_name
                # else:
                #         layout.operator("wm.addon_enable", 
                #                         icon='CHECKBOX_DEHLT', 
                #                         text=mod.bl_info["name"], 
                #                         emboss=False).module = module_name


                row = main_row.row(align = 1)
                addon_name = find_addon_name(item.text)
                row.label(text =     "   "   +   str(index + 1)   +   ".   "   +   addon_name, icon = ico)
                row.alignment = "LEFT"

                row = main_row.row(align = 1)
                row.prop(item, "text", emboss=1, text = "")
                row.alignment = "RIGHT"

                if index == wm.addons_list_index:
                    row.label(icon = "TRIA_LEFT", text = "")


                # addons = [
                #     (mod, addon_utils.module_bl_info(mod))
                #     for mod in addon_utils.modules(refresh=False)
                # ]
                # for mod, info in addons:
                #     module_name = mod.__name__
                # label(text="%s: %s" % (info["category"], info["name"]))


        


class Addons_List_Collection(PropertyGroup):

    text: StringProperty()

    index_from_group: IntProperty()

   



blender_classes_Addons_List = [
        ADDONS_LIST_UL_items,
        Addons_List_Collection,
        Addons_List_actions_add,
        Addons_List_actions,
        Addons_List_actions_remove,
        Addons_List_find,
        Addons_List_list_move,
        

]