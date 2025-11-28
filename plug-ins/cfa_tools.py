import maya.cmds as cmds
import maya.mel as mel
import os

class CFATools:
    """CFA Tools - ABC导入插件"""
    
    def __init__(self):
        self.plugin_name = "cfa_tools"
        self.menu_name = "CFAToolsMenu"
    
    def create_menu(self):
        """创建菜单栏"""
        # 删除已存在的菜单（如果存在）
        if cmds.menu(self.menu_name, exists=True):
            cmds.deleteUI(self.menu_name)
        
        # 创建主菜单
        main_menu = cmds.menu(self.menu_name, label="CFA Tools", parent="MayaWindow")
        
        # 创建模型插件父级菜单
        model_plugin_menu = cmds.menuItem(
            label="模型插件",
            parent=main_menu,
            subMenu=True
        )
        
        # 在模型插件菜单下创建ABC导入菜单项
        cmds.menuItem(
            label="导入ABC文件",
            parent=model_plugin_menu,
            command=lambda x: self.import_abc_file()
        )
        
        # 添加分隔符
        cmds.menuItem(divider=True, parent=main_menu)
        
        # 添加关于菜单项
        cmds.menuItem(
            label="关于CFA Tools",
            parent=main_menu,
            command=lambda x: self.show_about()
        )
        
        print("CFA Tools菜单已创建")
    
    def import_abc_file(self):
        """导入ABC文件"""
        try:
            # 打开文件选择对话框
            file_path = cmds.fileDialog2(
                fileFilter="Alembic Files (*.abc)",
                dialogStyle=2,
                caption="选择ABC文件"
            )
            
            if file_path:
                file_path = file_path[0]
                print(f"正在导入ABC文件: {file_path}")
                
                # 使用Maya的Alembic导入命令
                # 首先确保Alembic插件已加载
                if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
                    cmds.loadPlugin("AbcImport")
                
                # 执行ABC导入
                mel.eval(f'AbcImport -mode import "{file_path}";')
                
                cmds.confirmDialog(
                    title="导入成功",
                    message=f"ABC文件已成功导入: {os.path.basename(file_path)}",
                    button=["确定"]
                )
                
        except Exception as e:
            error_msg = f"导入ABC文件时出错: {str(e)}"
            print(error_msg)
            cmds.confirmDialog(
                title="导入错误",
                message=error_msg,
                button=["确定"]
            )
    
    def show_about(self):
        """显示关于信息"""
        about_text = """CFA Tools v1.0

功能:
• 导入Alembic (ABC) 文件
• 自动菜单栏集成

开发者: CFA Tools Team
"""
        cmds.confirmDialog(
            title="关于CFA Tools",
            message=about_text,
            button=["确定"]
        )
    
    def initialize_plugin(self):
        """初始化插件"""
        try:
            self.create_menu()
            print("CFA Tools插件初始化完成")
            return True
        except Exception as e:
            print(f"CFA Tools插件初始化失败: {str(e)}")
            return False

# 全局插件实例
cfa_tools_instance = None

def initializePlugin(mobject):
    """Maya插件初始化函数"""
    global cfa_tools_instance
    try:
        cfa_tools_instance = CFATools()
        if cfa_tools_instance.initialize_plugin():
            print("CFA Tools插件已成功加载")
        else:
            print("CFA Tools插件加载失败")
    except Exception as e:
        print(f"CFA Tools插件初始化错误: {str(e)}")

def uninitializePlugin(mobject):
    """Maya插件卸载函数"""
    global cfa_tools_instance
    try:
        # 删除菜单
        if cmds.menu("CFAToolsMenu", exists=True):
            cmds.deleteUI("CFAToolsMenu")
        
        cfa_tools_instance = None
        print("CFA Tools插件已卸载")
    except Exception as e:
        print(f"CFA Tools插件卸载错误: {str(e)}")

# 如果直接运行，用于测试
if __name__ == "__main__":
    cfa_tools_instance = CFATools()
    cfa_tools_instance.initialize_plugin()
