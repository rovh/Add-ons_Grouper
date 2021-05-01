import bpy


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

from .Addons_List import *



custom_scene_name = ".Addons_Grouper_Data"


class Addons_Groups_List_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_groups_list.list_action"
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
            return "Up\
                \nUp active element in the list"
        elif properties.action == 'DOWN':
            return "Down\
                \nDown active element in the list"

    def invoke(self, context, event):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_groups_list_index

        try:
            item = wm.addons_groups_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(wm.addons_groups_list) - 1:
                wm.addons_groups_list.move(idx, idx+1)
                wm.addons_groups_list_index += 1


                for element in wm.addons_list:

                    if element.index_from_group == idx:
                        element.index_from_group = -1

                    elif element.index_from_group == idx + 1:
                        element.index_from_group = -2


                for element in wm.addons_list:
                    if element.index_from_group == -1:
                        element.index_from_group = idx + 1

                    elif element.index_from_group == -2:
                        element.index_from_group = idx




            elif self.action == 'UP' and idx >= 1:
                wm.addons_groups_list.move(idx, idx-1)
                wm.addons_groups_list_index -= 1


                for element in wm.addons_list:

                    if element.index_from_group == idx:
                        element.index_from_group = -1

                    elif element.index_from_group == idx - 1:
                        element.index_from_group = -2


                for element in wm.addons_list:
                    if element.index_from_group == -1:
                        element.index_from_group = idx - 1

                    elif element.index_from_group == -2:
                        element.index_from_group = idx
                

        return {"FINISHED"}
class Addons_Groups_List_actions_add(Operator):
    bl_idname = "addons_groups_list.list_action_add"
    bl_label = "Add"
    bl_description = "Add Group"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    # def draw(self, context):
    #     layout = self.layout

    #     layout.prop(self, "text_input", text = "Name")

    # def invoke(self, context, event):
    #     self.unit_input = bpy.context.window_manager.setprecisemesh.length
    #     return context.window_manager.invoke_props_dialog(self)


    # @classmethod
    # def description(cls, context, properties):
    #     return "Add"

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_groups_list_index

        try:
            item = wm.addons_groups_list[idx]
        except IndexError:
            pass

        item = wm.addons_groups_list.add()

        wm.addons_groups_list_index = len(wm.addons_groups_list) - 1

        return {"FINISHED"}       
class Addons_Groups_List_actions_remove(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_groups_list.list_action_remove"
    bl_label = "Remove"
    bl_description = "Remove selected Group"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return bool(wm.addons_groups_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager

        idx = wm.addons_groups_list_index
       
        

        if idx < len(wm.addons_groups_list) - 1:

            for element in wm.addons_list:

                if element.index_from_group == idx:
                    element.index_from_group = -1

                elif element.index_from_group == idx + 1:
                    element.index_from_group = -2


            for element in wm.addons_list:
                if element.index_from_group == -1:
                    element.index_from_group = idx + 1

                elif element.index_from_group == -2:
                    element.index_from_group = idx


        
        if idx == 0:
            wm.addons_groups_list_index = 0
        else:
            wm.addons_groups_list_index -= 1

        wm.addons_groups_list.remove(idx)

        for element in wm.addons_list:
            if element.index_from_group == idx:
                wm.addons_list.remove(idx)

        return {"FINISHED"}  
class Addons_Groups_List_clear(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_groups_list.clear_list"
    bl_label = "Clear"
    bl_description = "Clear All Groups"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return bool(wm.addons_groups_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        wm = context.window_manager
        if bool(wm.addons_groups_list):
            wm.addons_groups_list.clear()
            if bool(wm.addons_list):
                wm.addons_list.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}


def count_enabled_and_disabled(group_index):
    index = group_index
    item_is_disabled_count = 0
    item_is_enabled_count = 0

    for i in bpy.context.window_manager.addons_list:

        module_name = find_addon_name(i.text, module_name=True)

        if bool(module_name):

            prefs = bpy.context.preferences
            used_ext = {ext.module for ext in prefs.addons}
            item_is_enabled = module_name in used_ext

            if item_is_enabled == True and i.index_from_group == index:
                item_is_enabled_count += 1

            if item_is_enabled == False and i.index_from_group == index:
                item_is_disabled_count += 1

    return item_is_enabled_count, item_is_disabled_count


class ADDONS_GROUPS_LIST_UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        # scene = context.scene
        wm = context.window_manager

        # try:
        #     item = scene.addons_groups_list[index]
        # except IndexError:
        #     pass


        first_column = layout.column(align = 1)

        first_row = first_column.row(align = 1)

        tex = "  " + str(index + 1)
        # split = first_row.split(factor = .05)
        # split.label(text = tex)
        # split.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index
        item_is_enabled_count, item_is_disabled_count = count_enabled_and_disabled(index)
        depress = True if index == wm.addons_groups_list_index and item.show == True else False
        depress_2 = True if index == wm.addons_groups_list_index else False


        row = first_row.row(align = 1)


        if item_is_enabled_count == 0 and item_is_disabled_count != 0:
            # row = first_row.row(align = 1)
            # row.label(icon = "CHECKBOX_DEHLT")
            ic = "CHECKBOX_DEHLT"
        elif item_is_enabled_count != 0 and item_is_disabled_count == 0:
            # row = first_row.row(align = 1)
            # row.label(icon = "CHECKMARK")
            ic = "CHECKMARK"

        else:
            ic = "BLANK1"
        


        row.operator("addons_list.list_move", icon= ic, text = "", depress = 0, emboss = 0).group_index = index
        row.scale_x = 1.1


        row = first_row.row(align = 1)

        
        ico = "TRIA_DOWN" if index == wm.addons_groups_list_index and item.show == True else "NONE"
        
        row.operator("addons_list.list_move", icon= ico, text = tex, depress = depress_2, emboss = 1).group_index = index
        # row.alignment = "LEFT"
        # row.alignment = "CENTER"
        row.scale_x = .2
        
        # row = first_row.row(align = 1)
        row = first_row
        
        row_left = row.row(align = 1)
        row_left.scale_x = .9
        # row_left.alignment = "CENTER"
        # row_left.alignment = "LEFT"

        row_center = row.row(align = 1)
        row_center.alignment = "CENTER"
        row_center.scale_x = 1.5

        row_right = row.row(align = 1)
        # row_right.alignment = "CENTER"




        if index == wm.addons_groups_list_index:
            row_left.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index          
            row_center.operator("addons_list.list_move", icon=item.symbols, text = item.name, depress = depress).group_index = index
            # row_right.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index
           
        else:
            
            row_left.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index
            row_center.operator("addons_list.list_move", icon=item.symbols, text = item.name, depress = 0).group_index = index
            
            

        row_right.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index

        
    
        item_is_enabled_count, item_is_disabled_count = count_enabled_and_disabled(index)

        if  bpy.data.scenes.find(custom_scene_name) != -1:
            depress = True if item.auto_enable == True and bool(bpy.data.scenes[custom_scene_name].auto_enable_list) == True else False
            depress_2 = True if item.auto_disable == True and bool(bpy.data.scenes[custom_scene_name].auto_disable_list) == True else False
        else:
            depress = False
            depress_2 = False


        op = row_right.operator("addons_grouper.auto_enable_disable_list", icon="CHECKMARK", text = "", depress = depress)
        op.action = "enable"
        op.group_index = index
        
        op = row_right.operator("addons_grouper.auto_enable_disable_list", icon="CHECKBOX_DEHLT", text = "", depress = depress_2)
        op.action = "disable"
        op.group_index = index


        
        if index != wm.addons_groups_list_index:
            
            first_column.separator(factor = 3)
        
        else:
    
            if item.show == False:
                first_column.separator(factor = 3)

            if item.show == True:


                if index == (wm.addons_groups_list_index - 1):
                    first_column.separator(factor = 7)


                main_box = first_column.box()
                main_box = main_box.box()
                main_column = main_box.column(align = 1)

                main_column.separator(factor = 3)



                # main_column.separator(factor = 1)




                # right_row = main_column.row(align = 1)
                # right_row.scale_y = 1

                # right_row_left = right_row.row(align = 1)
                # right_row_left.scale_x = 1.4
                # right_row_left.operator("addons_grouper.open_browser_or_folder", text = "", icon = "URL", emboss = 1).link = item.link_text
                
                # right_row_right = right_row.row(align = 1)
                # right_row_right.scale_x = .5
                # right_row_right.prop(item, "link_text", emboss=1, text = "")



                # main_column.separator(factor = 1.5)




                

                # right_row_left = right_row.row(align = 1)
                # right_row_left.scale_x = 1.4
                # right_row_left.operator("addons_grouper.open_browser_or_folder", text = "", icon = "FILEBROWSER", emboss = 1).link = item.addon_link
                
                
                            

                

                # main_column.separator(factor = 1.5)

                

                
                item_is_enabled_count, item_is_disabled_count = count_enabled_and_disabled(index)
                

                main_row = main_column.row(align = 0)

                row = main_row.row(align = 1)
                # row.scale_x = 1.1
                row.label(icon = "QUIT", text = "")
                

                op = row.operator("addons_grouper.auto_enable_disable_list", icon="CHECKMARK", text = "", depress = depress)
                op.action = "enable"
                op.group_index = index
                
                op = row.operator("addons_grouper.auto_enable_disable_list", icon="CHECKBOX_DEHLT", text = "", depress = depress_2)
                op.action = "disable"
                op.group_index = index
                
                
                row.alignment = "LEFT"


                row = main_row.row(align = 0)

                if item_is_enabled_count == 0:
                    op = row.operator("addons_grouper.switch", icon="CHECKMARK", text = "Enable All")
                    op.action = "ENABLE"
                    op.group_index = index

                elif item_is_disabled_count == 0:
                    op = row.operator("addons_grouper.switch", icon="CHECKBOX_DEHLT", text = "Disable All")
                    op.action = "DISABLE"
                    op.group_index = index
                else:
                    op = row.operator("addons_grouper.switch", icon="CHECKBOX_DEHLT", text = "Disable All")
                    op.action = "DISABLE"
                    op.group_index = index
                    
                    op = row.operator("addons_grouper.switch", icon="CHECKMARK", text = "Enable All")
                    op.action = "ENABLE"
                    op.group_index = index


                row.scale_x = .5
                row.scale_y = 1.3
                row.alignment = "CENTER"
                
            
                row = main_row.row(align = 0)
        
                row.label(icon = "BLANK1")
                row.prop(item, "show_parameters", emboss=1, text = "", icon = "OUTLINER_DATA_GP_LAYER")
                row.alignment = "RIGHT"
                
                


                main_column.separator(factor = 2)

                


                if item.show_parameters == True:

                    main_column.separator(factor = 1)

                    box = main_column.box()

                    row = box.row()
                    row_left = row.row(align = 1)
                    row_left.alignment = "LEFT"
                    row_left.label(icon = "OUTLINER_OB_FONT", text = "Add-ons Group Name:")
                    row.prop(item, "name", emboss=1, text = "")


                    main_column.separator(factor = 1.5)



                # row = main_column.row(align = 1)
                # row_left = row.row(align = 1)
                # row_left.alignment = "LEFT"
                # row_left.label(icon = "HELP")
                # row_left.label(text = " Description:")


                # row = row.row(align = 1)
                # row.prop(item, "description", emboss=1, text = "")

                # row = main_column.row(align = 1)
                # row.prop(item, "description_2", emboss=1, text = "")

                # row = main_column.row(align = 1)
                # row.prop(item, "description_3", emboss=1, text = "")


                    main_column.separator(factor = 1.5)


                    row = box.row(align = 1)
                    row_left = row.row(align = 1)
                    row_left.alignment = "LEFT"
                    row_left.label(icon = "BLENDER")
                    row_left.label(text = " Label:")
                    row_left.prop(item, 'symbols', expand = True)



                    # main_column.separator(factor = 1.5)



                # right_row = main_column.row(align = 1)


                # t = text_function(item.addon_link)

                # right_row_right = right_row.row(align = 1)
                # right_row_right.scale_x = .5
                # right_row_right.label(text = t)
                # right_row_right.prop(item, "addon_link", emboss=1, text = "")



                main_column.separator(factor = 2)

                row = main_column.row()
                scale = 1.1
                row.scale_x = scale
                row.scale_y = scale

                row_left = row.row()
                row_left.alignment = "LEFT"
                row_left.operator("addons_list.list_action_add", icon="FILE_NEW", text = "Add Add-on").group_index = index
                row_left.scale_x = .9
                # count = 0
                # for element in wm.addons_list:
                #     if element.index_from_group == index:
                #         count += 1
                # row_left.label(text = "Amt : " + str(count)  )
                row_left.label(text = "Amt : " + str(item_is_enabled_count + item_is_disabled_count)  )


                row_right =  row.row(align = 1)
                row_right.alignment = "RIGHT"


                row_right.operator("addons_grouper.open_browser_or_folder", icon="URL", text = "")

                row_right.separator(factor = 1)

                row_right.operator("addons_list.find", icon="VIEWZOOM", text = "")

                row_right.separator(factor = 1)
                
                row_right.operator("addons_list.list_action", icon="TRIA_UP", text = "").action = "UP"
                row_right.operator("addons_list.list_action", icon="TRIA_DOWN", text = "").action = "DOWN"

                row_right.separator(factor = 3.5)

                row_right.operator("addons_list.list_action_remove", icon="PANEL_CLOSE", text = "").group_index = index


                rows = 2
                wm = context.window_manager
                main_column.template_list("ADDONS_LIST_UL_items", "", wm, "addons_list", wm, "addons_list_index", rows=rows)


                if len(wm.addons_groups_list)-1 != index:
                    first_column.separator(factor = 7)
                

            # first_column.separator(factor = 2)



                # main_box.separator(factor = 1)
                # first_column.separator(factor = 8)

                # main_column.separator(factor = 3)
                # row = main_column.row()
                # row.scale_y = .5
                # row.alignment = "CENTER"
                # split = row.split()
                # split.label(icon = "BLANK1")
                # for _ in range(10):
                #     split.label(text = "_____________")
                



            # left_row.scale_x = .3

            # row.scale_y = 2

            # column_main = layout.column(align = 1)
            # box = column_main.box()
            # column = box.column(align = 1)
            # row_header = column.row(align = 1)
            # row_header.scale_y = .8


            # if bpy.context.scene.addons_groups_list[index].bool == True:
            #     row_info = row_header.row(align = 1)
            #     row_info.operator("addons_groups_list.list_action_bool", text = "", icon = "CHECKBOX_DEHLT", emboss = 0).my_index = index
            #     row_info.alignment = 'RIGHT'

            #     # row_info = row_header.row(align = 1)
            #     # row_info.operator("addons_groups_list.list_action_bool", text = "", icon = "SHADING_SOLID", emboss = 0).my_index = index
            #     # row_info.alignment = 'CENTER'
            # else:
            #     row_info = row_header.row(align = 1)
            #     row_info.operator("addons_groups_list.list_action_bool", text = "", icon = "BOOKMARKS", emboss = 0).my_index = index
            #     row_info.alignment = 'LEFT'

            # if item.text.count("\n") > 0:
            #     multiple_strokes = True
            # else:
            #     multiple_strokes = False


            # if multiple_strokes == True:
            #     text_parts_list = item.text.split('\n')
            #     # self.draw_text(text_parts_list)
            #     column.separator(factor=.5)
            #     col = column
            #     for i in text_parts_list:
            #         row = col.row(align = 1)
            #         row.label(text = i)
            #         row.scale_y = 0
            # else:
            #     column.separator(factor=.6)
            #     column.prop(item, "text", emboss=1, text = "")
            
            # column_main.separator(factor=1.1)

class Addons_Groups_List_Collection(PropertyGroup):
    
    show: BoolProperty()

    show_parameters: BoolProperty(name = "Show Parameters for this Group")

    text: StringProperty()

    ico_name: StringProperty(default = "BLANK1")

    name: StringProperty(default = "-", name = "Group Name")

    auto_enable: BoolProperty(default = False)

    auto_disable: BoolProperty(default = False)
    

    names_list = [
        "LAYER_ACTIVE",
        "NODE_MATERIAL",
        "TEXTURE_DATA",
        "BRUSH_TEXDRAW",
        "RESTRICT_RENDER_OFF",
        "ONIONSKIN_ON",
        "ACTION",
        "COMMUNITY",
        "MODIFIER",
        "SHADERFX",
        "AUTO",
        "MOD_BOOLEAN",
        "NODETREE",
        "FILE_FOLDER",
        "FILE_BLEND",
        "EDITMODE_HLT",
        "SEQUENCE",
        "QUIT",
        "FILE_SCRIPT",

    ]

    symbols_list = []
    for name in names_list:
        symbols_list.append(    (name,  "",  "" , name,  names_list.index(name)),       )

    symbols: EnumProperty(
        items=(

            symbols_list           
            
        ),
        default = 'LAYER_ACTIVE',
        description = "The icon to be used for this group",
        name = "Icon"
        )


blender_classes_Addons_Groups_List = [
    Addons_Groups_List_Collection,
    
    Addons_Groups_List_actions,
    Addons_Groups_List_actions_add,
    Addons_Groups_List_actions_remove,
    ADDONS_GROUPS_LIST_UL_items,
    Addons_Groups_List_clear,
    
]
