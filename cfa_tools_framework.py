import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import importlib

class CFAToolsFramework:
    """CFA Tools 插件框架 - 统一管理所有公司插件"""
    
    def __init__(self):
        self.framework_name = "CFA Tools Framework"
        self.menu_name = "CFAToolsMenu"
        self.plugins_dir = "plugins"
        self.loaded_plugins = {}
        
    def get_plugins_directory(self):
        """获取插件目录路径"""
        # 获取当前框架文件所在目录
        framework_dir = os.path.dirname(os.path.abspath(__file__))
        plugins_dir = os.path.join(framework_dir, self.plugins_dir)
        return plugins_dir
    
    def discover_plugins(self):
        """发现可用的插件"""
        plugins_dir = self.get_plugins_directory()
        
        if not os.path.exists(plugins_dir):
            print(f"插件目录不存在: {plugins_dir}")
            return []
        
        plugins = []
        for item in os.listdir(plugins_dir):
            if item.endswith('.py') and not item.startswith('__'):
                plugin_name = item[:-3]  # 移除.py扩展名
                plugins.append(plugin_name)
        
        print(f"发现插件: {plugins}")
        return plugins
    
    def load_plugin(self, plugin_name):
        """动态加载插件"""
        try:
            plugins_dir = self.get_plugins_directory()
            
            # 添加插件目录到Python路径
            if plugins_dir not in sys.path:
                sys.path.append(plugins_dir)
            
            # 动态导入插件模块
            plugin_module = importlib.import_module(plugin_name)
            
            # 检查插件是否实现了必要的接口
            if hasattr(plugin_module, 'get_plugin_info') and hasattr(plugin_module, 'register_commands'):
                plugin_info = plugin_module.get_plugin_info()
                
                # 注册插件命令
                commands = plugin_module.register_commands()
                
                self.loaded_plugins[plugin_name] = {
                    'module': plugin_module,
                    'info': plugin_info,
                    'commands': commands
                }
                
                print(f"插件 '{plugin_name}' 加载成功")
                return True
            else:
                print(f"插件 '{plugin_name}' 缺少必要的接口")
                return False
                
        except Exception as e:
            print(f"加载插件 '{plugin_name}' 失败: {str(e)}")
            return False
    
    def create_menu(self):
        """创建统一的CFA Tools菜单"""
        # 删除已存在的菜单
        if cmds.menu(self.menu_name, exists=True):
            cmds.deleteUI(self.menu_name)
        
        # 创建主菜单
        main_menu = cmds.menu(self.menu_name, label="CFA Tools", parent="MayaWindow")
        
        # 发现并加载所有插件
        available_plugins = self.discover_plugins()
        
        # 为每个插件创建子菜单
        for plugin_name in available_plugins:
            if self.load_plugin(plugin_name):
                self.create_plugin_submenu(main_menu, plugin_name)
        
        # 添加分隔符
        cmds.menuItem(divider=True, parent=main_menu)
        
        # 添加插件管理器
        cmds.menuItem(
            label="插件管理器",
            parent=main_menu,
            command=lambda x: self.show_plugin_manager()
        )
        
        # 添加关于菜单项
        cmds.menuItem(
            label="关于CFA Tools",
            parent=main_menu,
            command=lambda x: self.show_about()
        )
        
        print(f"CFA Tools框架菜单已创建，加载了 {len(self.loaded_plugins)} 个插件")
    
    def create_plugin_submenu(self, parent_menu, plugin_name):
        """为插件创建子菜单"""
        plugin_data = self.loaded_plugins[plugin_name]
        plugin_info = plugin_data['info']
        
        # 创建插件子菜单
        submenu = cmds.menuItem(
            label=plugin_info['name'],
            subMenu=True,
            parent=parent_menu,
            tearOff=True
        )
        
        # 添加插件的命令
        for command in plugin_data['commands']:
            cmds.menuItem(
                label=command['label'],
                parent=submenu,
                command=command['command']
            )
        
        # 添加分隔符
        cmds.menuItem(divider=True, parent=submenu)
        
        # 添加插件信息
        cmds.menuItem(
            label=f"关于 {plugin_info['name']}",
            parent=submenu,
            command=lambda x, p=plugin_name: self.show_plugin_info(p)
        )
    
    def show_plugin_manager(self):
        """显示插件管理器"""
        plugin_count = len(self.loaded_plugins)
        
        manager_text = f"CFA Tools 插件管理器\n\n"
        manager_text += f"已加载插件: {plugin_count} 个\n\n"
        
        for plugin_name, plugin_data in self.loaded_plugins.items():
            info = plugin_data['info']
            manager_text += f"• {info['name']} v{info['version']}\n"
            manager_text += f"  描述: {info['description']}\n"
            manager_text += f"  作者: {info['author']}\n\n"
        
        cmds.confirmDialog(
            title="CFA Tools 插件管理器",
            message=manager_text,
            button=["确定"]
        )
    
    def show_plugin_info(self, plugin_name):
        """显示插件详细信息"""
        if plugin_name in self.loaded_plugins:
            plugin_data = self.loaded_plugins[plugin_name]
            info = plugin_data['info']
            
            plugin_text = f"{info['name']} v{info['version']}\n\n"
            plugin_text += f"描述: {info['description']}\n"
            plugin_text += f"作者: {info['author']}\n"
            plugin_text += f"插件ID: {plugin_name}\n"
            
            cmds.confirmDialog(
                title=f"关于 {info['name']}",
                message=plugin_text,
                button=["确定"]
            )
    
    def show_about(self):
        """显示关于信息"""
        about_text = """CFA Tools Framework v1.0

统一插件管理框架
• 动态插件发现和加载
• 统一的菜单管理
• 插件热重载支持
• 公司标准插件接口

开发者: CFA Tools Team
"""
        cmds.confirmDialog(
            title="关于CFA Tools Framework",
            message=about_text,
            button=["确定"]
        )
    
    def initialize_framework(self):
        """初始化框架"""
        try:
            self.create_menu()
            print("CFA Tools框架初始化完成")
            return True
        except Exception as e:
            print(f"CFA Tools框架初始化失败: {str(e)}")
            return False

# 全局框架实例
cfa_framework_instance = None

def initializePlugin(mobject):
    """Maya插件初始化函数"""
    global cfa_framework_instance
    try:
        cfa_framework_instance = CFAToolsFramework()
        if cfa_framework_instance.initialize_framework():
            print("CFA Tools框架已成功加载")
        else:
            print("CFA Tools框架加载失败")
    except Exception as e:
        print(f"CFA Tools框架初始化错误: {str(e)}")

def uninitializePlugin(mobject):
    """Maya插件卸载函数"""
    global cfa_framework_instance
    try:
        # 删除菜单
        if cmds.menu("CFAToolsMenu", exists=True):
            cmds.deleteUI("CFAToolsMenu")
        
        cfa_framework_instance = None
        print("CFA Tools框架已卸载")
    except Exception as e:
        print(f"CFA Tools框架卸载错误: {str(e)}")

# 如果直接运行，用于测试
if __name__ == "__main__":
    cfa_framework_instance = CFAToolsFramework()
    cfa_framework_instance.initialize_framework()
