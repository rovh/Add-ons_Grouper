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



custom_scene_name = ".Addons_Helper_Data"


class Addons_Helper_List_actions(Operator):
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
            return "Up"
        elif properties.action == 'DOWN':
            return "Down"

    def invoke(self, context, event):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_groups_list_index

        try:
            item = scene.addons_groups_list[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scene.addons_groups_list) - 1:
                scene.addons_groups_list.move(idx, idx+1)
                wm.addons_groups_list_index += 1

            elif self.action == 'UP' and idx >= 1:
                scene.addons_groups_list.move(idx, idx-1)
                wm.addons_groups_list_index -= 1
                

        return {"FINISHED"}
class Addons_Helper_List_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_groups_list.list_action_add"
    bl_label = ""
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    # def draw(self, context):
    #     layout = self.layout

    #     layout.prop(self, "text_input", text = "Name")

    # def invoke(self, context, event):
    #     self.unit_input = bpy.context.window_manager.setprecisemesh.length
    #     return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def description(cls, context, properties):
        return "Add"

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_groups_list_index

        try:
            item = scene.addons_groups_list[idx]
        except IndexError:
            pass

        item = scene.addons_groups_list.add()

        wm.addons_groups_list_index = len(scene.addons_groups_list) - 1

        return {"FINISHED"}       
class Addons_Helper_List_actions_remove(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_groups_list.list_action_remove"
    bl_label = "Remove"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.addons_groups_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scene = context.scene
        wm = context.window_manager
        idx = wm.addons_groups_list_index
        
        if idx == 0:
            wm.addons_groups_list_index = 0
        else:
            wm.addons_groups_list_index -= 1
        
        scene.addons_groups_list.remove(idx)

        return {"FINISHED"}  
class Addons_Helper_List_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "addons_groups_list.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.addons_groups_list)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.addons_groups_list):
            context.scene.addons_groups_list.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
class Addons_Helper_List_actions_bool(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "addons_groups_list.list_action_bool"
    bl_label = ""
    bl_description = "Checkmark"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        # bpy.context.scene.addons_groups_list_index = self.my_index

        scene = context.scene
        # idx = scene.addons_groups_list_index
        idx = self.my_index

        try:
            item = scene.addons_groups_list[idx]
        except IndexError:
            pass

        
        if scene.addons_groups_list[idx].bool == True:
            scene.addons_groups_list[idx].bool = False
            if len(scene.addons_groups_list) > 1:
                scene.addons_groups_list.move(idx, 0)
        else:
            scene.addons_groups_list[idx].bool = True
            scene.addons_groups_list.move(idx, len(scene.addons_groups_list) - 1)


        return {"FINISHED"}


def count_enabled_and_disabled(group_index):
    index = group_index
    item_is_disabled_count = 0
    item_is_enabled_count = 0
    for i in bpy.context.scene.addons_list:

        module_name = find_addon_name(i.text, module_name=True)
        prefs = bpy.context.preferences
        used_ext = {ext.module for ext in prefs.addons}
        item_is_enabled = module_name in used_ext

        if item_is_enabled == True and i.index_from_group == index:
            item_is_enabled_count += 1

        if item_is_enabled == False and i.index_from_group == index:
            item_is_disabled_count += 1

    return item_is_enabled_count, item_is_disabled_count


class ADDONS_GROUPER_LIST_UL_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        scene = context.scene
        wm = context.window_manager

        try:
            item = scene.addons_groups_list[index]
        except IndexError:
            pass


        first_column = layout.column(align = 1)

        first_row = first_column.row(align = 1)

        tex = "  " + str(index + 1)
        # split = first_row.split(factor = .05)
        # split.label(text = tex)
        # split.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index

        row = first_row.row(align = 1)
        depress = True if index == wm.addons_groups_list_index else False
        ico = "PLAY" if index == wm.addons_groups_list_index else "NONE"
        row.operator("addons_list.list_move", icon= ico, text = tex, depress = depress).group_index = index
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
            row_center.operator("addons_list.list_move", icon=item.symbols, text = item.name, depress = 1).group_index = index
            row_right.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index
        else:
            row_left.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index
            row_center.operator("addons_list.list_move", icon=item.symbols, text = item.name, depress = 0).group_index = index
            row_right.operator("addons_list.list_move", icon= "NONE", text = " ", depress = 0).group_index = index

        





        
        
        


        # row = first_row.row()
        # row.operator("addons_list.list_move", icon="UV_SYNC_SELECT", text = "").group_index = index
        # row.scale_y = 1.5



        # if index == scene.addons_groups_list_index:

        #     # first_row.label(icon = "TRIA_RIGHT")
        #     first_row.label(icon = "TRIA_DOWN")

        #     first_row.label(text = item.name, icon = item.symbols)
            
        #     # first_row.label(icon = "TRIA_LEFT")
        #     first_row.label(icon = "TRIA_DOWN")

        # else:

        #     first_row.label(text = item.name, icon = item.symbols)



        
        if index != wm.addons_groups_list_index:
            
            first_column.separator(factor = 1.5)

            if index == (wm.addons_groups_list_index - 1):
                first_column.separator(factor = 7)

        else:




            main_box = first_column.box()
            main_box = main_box.box()
            main_column = main_box.column(align = 1)





            # main_column.separator(factor = 1)




            # right_row = main_column.row(align = 1)
            # right_row.scale_y = 1

            # right_row_left = right_row.row(align = 1)
            # right_row_left.scale_x = 1.4
            # right_row_left.operator("addons_helper.open_browser_or_folder", text = "", icon = "URL", emboss = 1).link = item.link_text
            
            # right_row_right = right_row.row(align = 1)
            # right_row_right.scale_x = .5
            # right_row_right.prop(item, "link_text", emboss=1, text = "")



            main_column.separator(factor = 1.5)




            

            # right_row_left = right_row.row(align = 1)
            # right_row_left.scale_x = 1.4
            # right_row_left.operator("addons_helper.open_browser_or_folder", text = "", icon = "FILEBROWSER", emboss = 1).link = item.addon_link
            
            
                        

            

            # main_column.separator(factor = 1.5)

            

            
            item_is_enabled_count, item_is_disabled_count = count_enabled_and_disabled(index)
            

            row = main_column.row()

            if item_is_enabled_count == 0:
                row.operator("addons_helper.switch", icon="CHECKMARK", text = "Enable All").group_index__and__action = str(index) + "_ENABLE"
            elif item_is_disabled_count == 0:
                row.operator("addons_helper.switch", icon="CHECKBOX_DEHLT", text = "Disable All").group_index__and__action = str(index) + "_DISABLE"
            else:
                row.operator("addons_helper.switch", icon="CHECKBOX_DEHLT", text = "Disable All").group_index__and__action = str(index) + "_DISABLE"
                row.operator("addons_helper.switch", icon="CHECKMARK", text = "Enable All").group_index__and__action = str(index) + "_ENABLE"
            

            row.scale_x = .5
            row.scale_y = 1.2
            row.alignment = "CENTER"

            main_column.separator(factor = 3)




            row = main_column.row()
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


            row = main_column.row(align = 1)
            row_left = row.row(align = 1)
            row_left.alignment = "LEFT"
            row_left.label(icon = "BLENDER")
            row_left.label(text = " Label:")
            row_left.prop(item, 'symbols', expand = True)



            main_column.separator(factor = 1.5)



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
            


            row_right =  row.row(align = 1)
            row_right.alignment = "RIGHT"


            row_right.operator("addons_list.find", icon="VIEWZOOM", text = "")


            row_right.separator(factor = 1)
            
            row_right.operator("addons_list.list_action", icon="TRIA_UP", text = "").action = "UP"
            row_right.operator("addons_list.list_action", icon="TRIA_DOWN", text = "").action = "DOWN"

            row_right.separator(factor = 3.5)

            row_right.operator("addons_list.list_action_remove", icon="PANEL_CLOSE", text = "").group_index = index


            rows = 2
            wm = context.window_manager
            main_column.template_list("ADDONS_LIST_UL_items", "", scene, "addons_list", wm, "addons_list_index", rows=rows)

            first_column.separator(factor = 9)



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




class Notes_List_Collection(PropertyGroup):


    # addons_list: CollectionProperty(type=Addons_List_Collection)

    text: StringProperty()
    link_text: StringProperty()
    link_text_2: StringProperty()
    addon_link: StringProperty()
    # description: StringProperty()
    # description_2: StringProperty()
    # description_3: StringProperty()
    ico_name: StringProperty(default = "BLANK1")
    name: StringProperty(default = "-")
    bool_view: BoolProperty()

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

    ]


    symbols_list = []
    for name in names_list:
        symbols_list.append(    (name,  "",  "" , name,  names_list.index(name)),       )

    # symbols_list = [
    #     ('LAYER_ACTIVE'         ,  "",  "" ,  "LAYER_ACTIVE",          1),
    #     ('DISCLOSURE_TRI_RIGHT' ,  "",  "" ,  "DISCLOSURE_TRI_RIGHT",  2),
    #     ('DISCLOSURE_TRI_DOWN'  ,  "",  "" ,  "DISCLOSURE_TRI_DOWN",   3),
    #     ('TRIA_RIGHT'           ,  "",  "" ,  "TRIA_RIGHT",            4),
    #     ('TRIA_DOWN'            ,  "",  "" ,  "TRIA_DOWN",             5),
    #     ('RIGHTARROW'           ,  "",  "" ,  "RIGHTARROW",            6),
    #     ('DOWNARROW_HLT'        ,  "",  "" ,  "DOWNARROW_HLT",         7),
    #     ('KEYTYPE_KEYFRAME_VEC' ,  "",  "" ,  "KEYTYPE_KEYFRAME_VEC",  8),
    #     ('KEYTYPE_BREAKDOWN_VEC',  "",  "" ,  "KEYTYPE_BREAKDOWN_VEC", 9),
    #     ('KEYTYPE_EXTREME_VEC'  ,  "",  "" ,  "KEYTYPE_EXTREME_VEC",   10),            
    #     ('KEYFRAME_HLT'         ,  "",  "" ,  "KEYFRAME_HLT",          11), 
    # ]


    symbols: EnumProperty(
        items=(

            symbols_list           
            
        ),
        default = 'LAYER_ACTIVE',
        description = "The icon to be used instead of the sign",
        name = "Line of text"
        )


blender_classes_Addons_Groups_List = [
    Notes_List_Collection,
    
    Addons_Helper_List_actions,
    Addons_Helper_List_actions_add,
    Addons_Helper_List_actions_remove,
    ADDONS_GROUPER_LIST_UL_items,
    Addons_Helper_List_actions_bool,
    Addons_Helper_List_clearList,
    
]
