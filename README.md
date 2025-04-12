# WordWeb - 单词学习管理系统


![Docker Hub Pulls](https://img.shields.io/docker/pulls/rheshyike/wordweb?) ![Python](https://img.shields.io/badge/Python-14354C.svg?logo=python&logoColor=white)  ![Flask](https://img.shields.io/badge/Flask-000.svg?logo=flask&logoColor=white)  

## 项目简介

WordWeb 是一个基于 Flask 框架开发的单词学习管理系统，旨在帮助用户高效地管理单词组、进行单词背诵和测试。用户可以创建、编辑和删除单词组，在背诵模式下逐个学习单词，还能通过顺序或乱序测试检验学习效果。系统会记录每个单词组的学习统计信息，如背诵次数、测试正确率等。在 v1.1.0 版本中，新增了 AI 大模型生成单词的功能，让用户可以更便捷地获取所需单词。

## v1.0.0 功能特性

- **单词组管理**：支持创建、编辑和删除单词组，方便用户组织和整理单词。
- **背诵模式**：提供分页浏览单词的功能，支持使用键盘方向键快速导航，完成背诵后自动记录背诵次数。
- **测试模式**：包括顺序和乱序两种测试模式，自动计算正确率并记录在数据库中。
- **数据验证**：在创建和编辑单词组时，对输入的单词进行格式验证，确保数据的准确性。

### **新增重要特性**

#### v1.1.0：AI 大模型生成单词

- 在创建新单词组时，用户可以利用 AI 大模型根据指定主题生成单词列表。只需输入想要的单词主题，点击“AI 生成”按钮，系统将自动调用大模型生成相关单词，为用户节省手动输入单词的时间和精力。可在设置界面进行配置，配置完成后，请点击测试连接进行测试，测试无误后即可使用AI生成单词。


#### v1.2.0：单词标记、黑曜石特殊卡片、全局聚焦搜索

- 目前背诵模式可以标记单词，按W 标记（在结束背诵后，将该单词复制到黑曜石收藏中）按S添加删除标记，在结束背诵模式的时候可以根据提示选择是否删除带有删除标记的单词。具体可以从单词卡片的边框和右上角的标签观察标记状态

- 筛选栏新增特殊卡片，黑曜石为其中之一的特殊卡片，可以把所有在背诵模式标记的单词自动收入黑曜石收藏中。

- 此外新增聚焦搜索功能，在任意界面按下Ctrl + Q的快捷键即刻出发，可以快速进入学习模式，如输入黑曜石收藏:1 即可进入其背诵模式。  


### **功能展示**

 

![主页卡片展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/1abca16653d4bd62cddcaf75cbc1e97d.gif)


![AI生成单词功能展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/5afaeebac96d47115fa3e0c4512339b4.gif)

![全局搜索展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/539be41f6e2b561d6521df774cd3aff1.gif)

## 安装与运行

### 1. 克隆项目

```Bash
git clone https://github.com/fzg001/wordweb.git
cd wordweb
```

### 2. 创建并激活虚拟环境（非必须）

```Bash
python -m venv venv
source venv/bin/activate  # 对于 Windows 用户，使用 `venv\Scripts\activate`
```

### 3. 安装依赖

```Bash
pip install -r requirements.txt
```

### 4. 配置环境变量（非必须）

在项目根目录下创建一个 `.env` 文件，并添加以下内容：

```Plain
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///wordweb.db
```

### 5. 配置 AI 设置（非必须）

在 `app/config` 目录下创建 `ai_settings.json` 文件，并添加以下内容：

```Plain
{
    "api_key": "your_api_key",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 2000,
    "api_base_url": "https://api.openai.com/v1"
}
```

### 6. 初始化数据库

```Bash
flask db init #如已经有数据库文件，则跳过该步骤
flask db migrate 
flask db upgrade
```

### 7. 运行项目

```Bash
python run.py
```

打开浏览器，访问 http://localhost:5000/即可开始使用。

### 8. 使用 Docker 部署

#### 8.1 拉取 Docker 镜像

你可以从 Docker Hub 拉取预构建的 WordWeb 镜像。[rheshyike/wordweb Tags | Docker Hub](https://hub.docker.com/repository/docker/rheshyike/wordweb/tags)

请确保你已经安装了 Docker，然后运行以下命令：

```bash
docker pull rheshyike/wordweb:latest
```

#### 8.2 运行 Docker 容器

拉取镜像后，使用以下命令来运行 Docker 容器：

```bash
docker run -p 5000:5000 rheshyike/wordweb:latest
```

## 项目结构 V1.0

```Plain
wordweb/                                     # 项目根目录
├── app/                                     # 应用程序主目录
│   ├── blueprints/                          # 包含不同功能模块
│   │   ├── main.py                          # 主页面路由处理，显示单词组列表
│   │   ├── groups.py                        # 单词组管理相关路由（创建、编辑、删除等）
│   │   └── practice.py						 # 学习功能路由（背诵模式、测试模式）
│   ├── templates/                           # HTML模板文件目录
│   │   ├── base.html                        # 基础模板，提供通用页面结构和导航
│   │   ├── index.html                       # 主页模板，显示所有单词组卡片
│   │   ├── create_group.html                # 创建新单词组的页面
│   │   ├── edit_group.html                  # 编辑现有单词组的页面
│   │   ├── manage_groups.html               # 管理单词组的页面
│   │   ├── group_detail.html                # 单词组详情页面，查看组内单词
│   │   ├── study_mode.html                  # 背诵模式页面
│   │   └── quiz_mode.html                   # 测试模式页面，用于测验单词
│   ├── models.py                            # 数据库模型定义（WordGroup, Word, GroupStats等）
│   ├── __init__.py
│   ├── config.py
│   └── utils/                               # 工具函数目录
│       └── validation.py
├── migrations/                              # 数据库迁移相关文件
│   ├── env.py
│   └── alembic.ini
├── static/                                  # 静态资源文件目录
│   └── style.css
├── run.py                                   # 应用程序入口点，启动Flask服务器
└── requirements.txt                         # 项目依赖包列表
```

## 技术栈

- **后端**：Python 3.10.16、Flask 3.0.2、Flask - SQLAlchemy 3.1.1、Flask - Migrate 4.0.5
- **前端**：HTML、CSS、JavaScript
- **数据库**：SQLite

## 贡献指南

如果你想为这个项目做出贡献，请遵循以下步骤：

1. Fork 这个仓库。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 打开一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。


## 已知问题
1. 默认紧凑切换偶尔需要刷新才能生效
2. 首页筛选后刷新有筛选前的残影闪过

