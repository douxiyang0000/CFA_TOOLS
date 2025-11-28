import maya.cmds as cmds
import maya.mel as mel

def get_plugin_info():
    """返回插件信息 - 必需接口"""
    return {
        'name': '插件名称',
        'version': '1.0',
        'description': '插件功能描述',
        'author': '开发者名称'
    }

def register_commands():
    """注册插件命令 - 必需接口"""
    return [
        {
            'label': '命令1',
            'command': command_function_1
        },
        {
            'label': '命令2', 
            'command': command_function_2
        },
        # 添加更多命令...
    ]

def command_function_1(*args):
    """命令1的功能实现"""
    try:
        # 在这里实现命令1的功能
        cmds.confirmDialog(
            title="命令1",
            message="命令1已执行",
            button=["确定"]
        )
    except Exception as e:
        print(f"命令1执行错误: {str(e)}")

def command_function_2(*args):
    """命令2的功能实现"""
    try:
        # 在这里实现命令2的功能
        cmds.confirmDialog(
            title="命令2",
            message="命令2已执行",
            button=["确定"]
        )
    except Exception as e:
        print(f"命令2执行错误: {str(e)}")

# 添加更多功能函数...

# 测试函数
if __name__ == "__main__":
    print("插件模板测试")
    print(f"插件信息: {get_plugin_info()}")
    print(f"注册的命令: {len(register_commands())} 个")
