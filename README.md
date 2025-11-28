# CFA Tools - Maya插件框架

CFA Tools是一个统一的Maya插件管理框架，允许您公司所有插件在统一的菜单中管理和使用。

## 功能特性

- 🚀 **自动加载**: Maya启动时自动加载插件
- 🎯 **统一管理**: 所有插件在CFA Tools菜单中统一管理
- 🔧 **动态发现**: 自动发现和加载plugins目录下的所有插件
- 📋 **插件管理器**: 内置插件管理器查看所有已加载插件
- 🛠️ **标准接口**: 统一的插件开发接口

## 文件结构

```
d:/MAYA_LIB/
├── cfa_tools.mod              # Maya模块描述文件
├── cfa_tools_framework.py     # 主框架文件
├── plugins/                   # 插件目录
│   ├── abc_importer.py       # ABC导入插件示例
│   └── plugin_template.py    # 插件开发模板
└── README.md                 # 说明文档
```

## 安装步骤

### 方法1: 手动安装

1. 将整个 `d:/MAYA_LIB/` 目录复制到您的Maya模块目录
2. 在Maya的模块目录中创建模块文件链接

### 方法2: 使用模块文件

1. 将 `cfa_tools.mod` 文件复制到Maya的模块目录:
   - Windows: `C:\Users\<用户名>\Documents\maya\<版本>\modules\`
   - 例如: `C:\Users\YourName\Documents\maya\2023\modules\cfa_tools.mod`

2. 确保 `d:/MAYA_LIB/` 目录存在且包含所有必要文件

### 验证安装

1. 启动Maya
2. 在菜单栏中应该看到 "CFA Tools" 菜单
3. 点击菜单查看已加载的插件

## 插件开发

### 插件接口要求

每个插件必须实现以下两个函数：

```python
def get_plugin_info():
    """返回插件信息字典"""
    return {
        'name': '插件名称',
        'version': '版本号',
        'description': '插件描述',
        'author': '作者名称'
    }

def register_commands():
    """返回命令列表"""
    return [
        {
            'label': '命令显示名称',
            'command': command_function
        }
    ]
```

### 开发步骤

1. 在 `plugins/` 目录中创建新的Python文件
2. 实现必需的接口函数
3. 添加您的功能函数
4. 重启Maya或重新加载插件

### 示例插件

参考 `plugins/plugin_template.py` 作为开发模板。

## 现有插件

### ABC导入器 (`abc_importer.py`)

功能:
- 导入单个ABC文件
- 批量导入ABC文件
- ABC导入设置

使用方法:
1. 在CFA Tools菜单中找到"ABC导入器"
2. 选择"导入ABC文件"或"批量导入ABC"
3. 选择要导入的文件或文件夹

## 故障排除

### 插件未显示在菜单中

1. 检查 `cfa_tools.mod` 文件路径是否正确
2. 确认插件文件在 `plugins/` 目录中
3. 检查插件是否实现了必需的接口函数
4. 查看Maya脚本编辑器中的错误信息

### 插件加载失败

1. 检查Python语法错误
2. 确认所有依赖的Maya模块已正确导入
3. 查看Maya脚本编辑器中的详细错误信息

## 开发指南

### 添加新插件

1. 复制 `plugin_template.py` 到新文件
2. 修改插件信息
3. 实现功能函数
4. 注册命令到 `register_commands()`

### 插件最佳实践

- 使用有意义的插件名称
- 提供清晰的插件描述
- 处理所有可能的异常
- 使用Maya的标准UI组件
- 在脚本编辑器中输出有用的调试信息

## 技术支持

如有问题，请检查:
1. Maya脚本编辑器中的错误信息
2. 插件文件路径和权限
3. Python语法和导入错误

## 版本历史

- v1.0 (2024): 初始版本发布
  - 基础插件框架
  - ABC导入器插件
  - 统一菜单管理
