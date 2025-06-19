开发环境
========================================
本项目在Windows系统上，使用 Python 3.12 开发，并使用 MySQL 9.1.0 作为数据库。

数据库初始化流程
========================================
1. 在终端登录，或打开 MySQL Workbench 程序 (可以在开始菜单里找到它)。
2. 使用 root 用户和密码登录。
3. 创建数据库：
   - 点击左上角的 "创建数据库" 按钮，打开新建数据库窗口。
   - 输入数据库名称 literature_management_system，然后点击 "创建" 按钮。
   - 或直接在 SQL 窗口中运行命令：CREATE DATABASE literature_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

测试数据导入方法
========================================
只需按照下面的步骤配置好所需的数据库，然后运行 app.py 程序，打开浏览器并访问 https://127.0.0.1:5000 即可在界面中导入测试数据。

项目安装与使用指南 (Windows版)
========================================
欢迎使用本系统！本指南将引导您在 Windows 电脑上完成所有安装和配置步骤。请严格按照顺序操作。
## 安装基础软件
您的电脑需要安装三个核心软件：Python, MySQL, 和 Docker。

1. 安装 Python (程序引擎)
   - 访问 Python 官网: https://www.python.org/downloads/
   - 点击黄色的 "Download Python" 按钮下载最新版本。
   - 运行下载的 .exe 安装程序。
   - 在安装界面底部，务必勾选 "Add python.exe to PATH" 复选框。
   - 点击 "Install Now"，等待安装完成。
2. 安装 MySQL (数据仓库)
   - 访问 MySQL 官网: https://dev.mysql.com/downloads/installer/
   - 下载页面下方较小的那个版本 (文件名通常包含 web-community)。
   - 运行下载的安装程序。
   - 在 "Choosing a Setup Type" 界面，选择 "Server only"。
   - 一路点击 "Next" 直到 "Accounts and Roles" 界面。
   - 为 root 用户（最高管理员）设置一个您能记住的密码，并用纸笔记下来，稍后会用到。
   - 继续点击 "Next" 完成所有安装。
3. 安装 Docker Desktop (PDF解析服务)
   - 访问 Docker 官网: https://www.docker.com/products/docker-desktop/
   - 下载并安装 Docker Desktop for Windows。
   - 安装过程中，请同意启用 WSL 2，这可能需要重启电脑。
   - 安装后，从桌面或开始菜单启动 Docker Desktop，并等待它完全启动（系统右下角的鲸鱼图标停止动画）。
  
## 配置项目文件
1. 解压项目:将您收到的项目压缩包（.zip 文件），解压到电脑桌面上。桌面上会出现一个 literature-manager 文件夹。
2. 配置密码:
   - 进入桌面上的 literature-manager 文件夹。
   - 找到 app.py 文件，右键点击 -> 打开方式 -> 记事本(Notepad)。
   - 在文件中找到这一行：DB_PASS = 'YourStrongPassword'
  将引号里的 YourStrongPassword 替换为您在 1.2 步中为 MySQL 设置的 root 用户真实密码。
   - 保存并关闭文件。
   
## 初始化服务与环境
这一步我们将使用 PowerShell 工具来执行一系列命令。
(如何打开 PowerShell: 点击Windows开始菜单，输入 PowerShell，然后点击打开。)
1. 启动 PDF 解析服务：在 PowerShell 窗口中，运行以下命令：
docker run -d --name grobid_service --init -p 8070:8070 lfoppiano/grobid:0.8.0

2. 创建数据库
   - 打开 MySQL Workbench 程序 (可以在开始菜单里找到它)。
   - 使用 root 用户和您设置的密码登录。
   - 点击左上角的 "SQL+" 图标，打开新查询窗口。
   - 运行以下命令：
  CREATE DATABASE literature_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3. 配置 Python 环境
   - 回到 PowerShell 窗口。
   - 进入项目文件夹：cd Desktop\literature-manager
  
   - 依次执行以下三条命令，创建并激活环境，然后安装所有依赖库：

     1. 创建虚拟环境: py -m venv venv

     2. 激活虚拟环境 (行首会出现 (venv) 字样): .\venv\Scripts\activate

     3. 安装所有需要的库: pip install -r requirements.txt
   - 注意: 如果第 2 步 `activate` 命令失败并报错，请以管理员身份打开一个新的PowerShell，运行 `Set-ExecutionPolicy RemoteSigned` (输入Y确认)，然后关闭管理员窗口，回到这个普通窗口重新尝试激活。

## 运行系统

- 恭喜您，所有准备工作都已完成！请确保您的 PowerShell 窗口仍在 literature-manager 目录下，并且行首有 (venv) 字样。
- 输入以下命令来启动程序：python app.py 
- 当终端显示 * Running on http://127.0.0.1:5000 后，请不要关闭此 PowerShell 窗口。打开您的网页浏览器（如 Chrome, Edge），在地址栏输入并访问：http://127.0.0.1:5000
- 现在，您就可以开始使用您的文献管理系统了！
  
## 日常使用提示
每次重启电脑后，如果您想再次使用本系统，只需要重复以下启动流程即可：
1. 启动 Docker Desktop。
2. 打开 PowerShell，运行 docker start grobid_service。
3. 打开另一个 PowerShell，进入项目文件夹 (cd Desktop\literature-manager)，激活环境 (.\venv\Scripts\activate)，然后运行程序 (python app.py)。

小组成员分工说明
========================================
李宏扬：负责概念模型设计与功能设计

刘新卫、麦梓谦：负责系统需求分析，前后端开发，数据库设计，测试，部署。

杨雨凝：负责项目文档与报告PPT的撰写，协调各成员的工作。