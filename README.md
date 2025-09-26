# 微信小程序项目文件打包与解包工具

这是一个使用 Python 开发的命令行工具集，用于将微信小程序项目源文件打包（编码）成一个单一的文本文件，并能从该文件中完美地还原（解码）出原始的项目结构。

这套工具是原始批处理（.bat）脚本的完全重构和升级版，解决了原脚本因命令行限制导致的所有问题，并提供了跨平台支持和更高的稳定性。

## ✨ 功能特性

*   📦 **打包为单文件**：将指定类型的小程序项目文件（如 `wxml`, `js`, `wxss`, `json` 等）合并编码为一个 `.txt` 文件，方便传输和分享。
*   📂 **结构化解码**：从打包文件中精确还原出原始的项目目录结构和所有文件内容。
*   🔐 **文件完整性校验**：在编码时为每个文件生成 SHA256 哈希值，并在解码后提供一键校验功能，确保文件在传输过程中没有被损坏或篡改。
*   ⚙️ **灵活配置**：通过 `config.ini` 文件可以轻松配置所有参数，如目标目录、输出文件、包含的文件类型、排除的目录等。
*   🚀 **命令行支持**：同时也支持通过命令行参数覆盖默认配置，满足不同使用场景的需求。
*   🛡️ **健壮性**：彻底解决了原批处理脚本遇到的路径过长、特殊字符、变量展开等问题。
*   💻 **跨平台兼容**：基于 Python 开发，可在 Windows, macOS, Linux 等主流操作系统上无差别运行。
*   🔄 **自动备份**：解码时会自动备份目标文件夹中已存在的旧文件，防止数据意外丢失。

##  MIGRATING_FROM_BAT_FILES.md

##  prerequisites
## 🚀 快速开始

### 1. 先决条件

-   确保您的系统中已经安装了 **Python 3.6** 或更高版本。
-   您可以在终端或命令行中运行 `python --version` 或 `python3 --version` 来检查。

### 2. 文件结构

为了获得最佳体验，建议您采用以下目录结构：

```
/wechat_mini_program_tools/
|
|-- 📄 config.ini               # 默认配置文件
|-- 🐍 encode_project.py        # 编码工具
|-- 🐍 decode_project.py        # 解码工具
|
|-- 📁 my_mini_program/          # (示例) 你要打包的小程序项目
|   |-- app.js
|   |-- app.json
|   |-- ...
|
|-- 📝 encoded_project.txt       # (示例) 编码后生成的输出文件
|-- 📁 decoded_project/         # (示例) 解码后还原的项目目录
```

### 3. 配置

在首次运行前，请根据您的需求修改 `config.ini` 文件。这是一个配置示例：

```ini
[DEFAULT]
# --- 编码配置 ---
# TARGET_DIR: 要打包的小程序项目根目录 ('.' 表示当前目录)
TARGET_DIR = my_mini_program

# OUTPUT_FILE: 编码后输出的文件名
OUTPUT_FILE = encoded_project.txt

# FILE_TYPES: 需要打包的文件扩展名，用空格分隔
FILE_TYPES = wxml js wxss wxs json png jpg gif

# EXCLUDE_DIRS: 需要排除的目录名，用空格分隔
EXCLUDE_DIRS = node_modules dist build .git unpackage

# --- 解码配置 ---
# SOURCE_FILE: 要解码的源文件名
SOURCE_FILE = encoded_project.txt

# OUTPUT_DIR: 解码后文件存放的目录
OUTPUT_DIR = decoded_project

# BACKUP: 解码时是否备份已存在的目标目录 (yes/no)
BACKUP = yes
```

## 📖 使用方法

请在工具所在的目录打开您的终端或命令行工具。

### 编码 (打包项目)

**用法1：使用 `config.ini` 中的默认配置**

直接运行脚本，它会自动读取配置文件。

```bash
python encode_project.py
```

**用法2：通过命令行参数指定目录和文件名**

命令行参数会覆盖 `config.ini` 中的设置。

```bash
# 格式: python encode_project.py [要编码的目录] [输出文件名]
python encode_project.py ./my_project my_encoded_app.txt
```

编码完成后，您会在目录下看到一个新生成的 `.txt` 文件，其中包含了项目的所有源码和元数据。

### 解码 (还原项目)

**用法1：使用 `config.ini` 中的默认配置**

```bash
python decode_project.py
```

**用法2：通过命令行参数指定源文件和输出目录**

```bash
# 格式: python decode_project.py [要解码的文件] [输出目录]
python decode_project.py my_encoded_app.txt ./restored_project
```

解码过程结束后，脚本会提示您按任意键开始文件完整性校验，它会逐一对比每个文件的哈希值，并报告成功和失败的数量。