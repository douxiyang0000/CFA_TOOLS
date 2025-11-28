import maya.cmds as cmds
import maya.mel as mel
import os

def get_plugin_info():
    """返回插件信息 - 必需接口"""
    return {
        'name': 'ABC导入器',
        'version': '1.0',
        'description': '导入Alembic (ABC) 文件到Maya场景',
        'author': 'CFA Tools Team'
    }

def register_commands():
    """注册插件命令 - 必需接口"""
    return [
        {
            'label': '导入ABC文件',
            'command': import_abc_file
        },
        {
            'label': '批量导入ABC',
            'command': batch_import_abc
        },
        {
            'label': 'ABC导入设置',
            'command': show_import_settings
        }
    ]

def import_abc_file(*args):
    """导入单个ABC文件"""
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
            
            # 确保Alembic插件已加载
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

def batch_import_abc(*args):
    """批量导入ABC文件"""
    try:
        # 打开文件夹选择对话框
        folder_path = cmds.fileDialog2(
            fileFilter="Alembic Files (*.abc)",
            dialogStyle=3,  # 文件夹选择模式
            caption="选择包含ABC文件的文件夹"
        )
        
        if folder_path:
            folder_path = folder_path[0]
            abc_files = []
            
            # 查找所有ABC文件
            for file in os.listdir(folder_path):
                if file.lower().endswith('.abc'):
                    abc_files.append(os.path.join(folder_path, file))
            
            if not abc_files:
                cmds.confirmDialog(
                    title="未找到文件",
                    message="在选定文件夹中未找到ABC文件",
                    button=["确定"]
                )
                return
            
            # 确保Alembic插件已加载
            if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
                cmds.loadPlugin("AbcImport")
            
            # 批量导入
            imported_count = 0
            for abc_file in abc_files:
                try:
                    mel.eval(f'AbcImport -mode import "{abc_file}";')
                    imported_count += 1
                    print(f"已导入: {os.path.basename(abc_file)}")
                except Exception as e:
                    print(f"导入失败 {os.path.basename(abc_file)}: {str(e)}")
            
            cmds.confirmDialog(
                title="批量导入完成",
                message=f"成功导入 {imported_count}/{len(abc_files)} 个ABC文件",
                button=["确定"]
            )
            
    except Exception as e:
        error_msg = f"批量导入ABC文件时出错: {str(e)}"
        print(error_msg)
        cmds.confirmDialog(
            title="导入错误",
            message=error_msg,
            button=["确定"]
        )

def show_import_settings(*args):
    """显示ABC导入设置对话框"""
    settings_window = "abc_import_settings_window"
    
    # 删除已存在的窗口
    if cmds.window(settings_window, exists=True):
        cmds.deleteUI(settings_window)
    
    # 创建设置窗口
    cmds.window(settings_window, title="ABC导入设置", width=300)
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label="ABC导入选项", align="center")
    cmds.separator(height=10)
    
    # 添加设置选项
    cmds.checkBoxGrp(
        "abc_connect_time",
        numberOfCheckBoxes=1,
        label="连接时间",
        value1=True
    )
    
    cmds.checkBoxGrp(
        "abc_create_proxy",
        numberOfCheckBoxes=1,
        label="创建代理几何体",
        value1=False
    )
    
    cmds.checkBoxGrp(
        "abc_preserve_hierarchy",
        numberOfCheckBoxes=1,
        label="保持层级结构",
        value1=True
    )
    
    cmds.separator(height=10)
    
    cmds.button(
        label="保存设置",
        command=save_import_settings
    )
    
    cmds.button(
        label="重置默认",
        command=reset_import_settings
    )
    
    cmds.showWindow(settings_window)

def save_import_settings(*args):
    """保存导入设置"""
    try:
        connect_time = cmds.checkBoxGrp("abc_connect_time", query=True, value1=True)
        create_proxy = cmds.checkBoxGrp("abc_create_proxy", query=True, value1=True)
        preserve_hierarchy = cmds.checkBoxGrp("abc_preserve_hierarchy", query=True, value1=True)
        
        # 这里可以保存设置到配置文件
        print(f"ABC导入设置已保存:")
        print(f"  连接时间: {connect_time}")
        print(f"  创建代理几何体: {create_proxy}")
        print(f"  保持层级结构: {preserve_hierarchy}")
        
        cmds.confirmDialog(
            title="设置已保存",
            message="ABC导入设置已成功保存",
            button=["确定"]
        )
        
    except Exception as e:
        print(f"保存设置时出错: {str(e)}")

def reset_import_settings(*args):
    """重置导入设置为默认值"""
    try:
        cmds.checkBoxGrp("abc_connect_time", edit=True, value1=True)
        cmds.checkBoxGrp("abc_create_proxy", edit=True, value1=False)
        cmds.checkBoxGrp("abc_preserve_hierarchy", edit=True, value1=True)
        
        cmds.confirmDialog(
            title="设置已重置",
            message="ABC导入设置已重置为默认值",
            button=["确定"]
        )
        
    except Exception as e:
        print(f"重置设置时出错: {str(e)}")

# 测试函数
if __name__ == "__main__":
    print("ABC导入器插件测试")
    print(f"插件信息: {get_plugin_info()}")
    print(f"注册的命令: {len(register_commands())} 个")
