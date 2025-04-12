# 🚀 WordWeb - 分组别英文词汇学习系统

<div align="center">



[![Docker Hub Pulls](https://img.shields.io/docker/pulls/rheshyike/wordweb?style=plastic&logo=docker&logoColor=white&color=2496ED)](https://hub.docker.com/r/rheshyike/wordweb) 
[![Python](https://img.shields.io/badge/Python-3.10+-14354C.svg?style=plastic&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg?style=plastic&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=plastic&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=plastic)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=plastic)](http://makeapullrequest.com)
[![Made with ❤](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg?style=plastic)](https://github.com/fzg001)

</div>

## ✨ 项目特点

WordWeb 不仅仅是一个单词学习工具，它是一个**智能词汇管理系统**，帮助你高效、智能地管理和学习单词。告别传统枯燥的单词记忆方式，体验全新交互式学习体验！

- 🎨 **优雅的卡片式界面** - 视觉化管理单词组
- 🤖 **AI驱动生成** - 自动创建主题词汇
- 🔍 **全局智能搜索** - 快速定位与进入学习模式
- 🌓 **深浅主题切换** - 保护视力，日夜不同体验
- 📱 **响应式设计** - 完美支持各种设备与备份同步

## 🖼️ 界面展示

<div align="center">

### 多种动态卡片界面
![主页卡片展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/1abca16653d4bd62cddcaf75cbc1e97d.gif)

### AI生成单词
![AI生成单词功能展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/5afaeebac96d47115fa3e0c4512339b4.gif)



</div>

## 🔥 进化中的功能特性

### 核心功能 (v1.0)

- ⚡ **高效单词组管理** - 创建、编辑、删除、排序，一气呵成
- 🧪 **多模式测试** - 顺序/随机测试，实时反馈，精准评估学习效果
- 🛡️ **数据验证** - 确保单词数据格式正确，杜绝错误输入

### 智能升级 (v1.1)

- 🤖 **AI词汇生成** - 接入大语言模型，输入主题即可自动生成相关单词表
- ⚙️ **可定制AI参数** - 温度、最大token等参数可调，满足个性化需求

### 超越进化 (v1.2)

- 🔖 **智能单词标记** - 一键标记重要词汇，快速删除无用单词
- 💎 **特殊收藏组** - 黑曜石收藏功能，自动整合所有标记词汇
- 🔍 **全局聚焦搜索** - `Ctrl+Q`一键激活，支持命令式快速导航
- 🎨 **深色/浅色主题** - 智能切换，呵护眼睛，提升体验

## ⚙️ 极速部署

### 方法1：传统部署

```bash
# 克隆仓库
git clone https://github.com/fzg001/wordweb.git
cd wordweb

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
flask db init  # 如已有数据库文件则跳过
flask db migrate
flask db upgrade

# 启动应用
python run.py
```

### 方法2：Docker一键部署 (推荐)

```bash
# 拉取镜像
docker pull rheshyike/wordweb:latest

# 启动容器
docker run -p 5000:5000 -v wordweb_data:/app/instance rheshyike/wordweb:latest
```

现在访问 http://localhost:5000/ 即可开始使用WordWeb！

## 🧠 AI配置指南

想要使用AI生成单词功能？只需简单几步：

1. 在设置页面中配置您的API密钥和模型
2. 点击"测试连接"确认配置无误
3. 在创建单词组页面，输入主题并点击"AI生成"


```json
// 示例AI配置
{
    "api_key": "your_api_key",
    "model": "deepseek-ai/DeepSeek-V3",
    "temperature": 0.7,
    "max_tokens": 2000,
    "api_base_url": "https://api.openai.com/v1"
}
```

## 🧩 项目架构

```
wordweb/
├── 📁 app/                         # 应用核心
│   ├── 📁 blueprints/              # 功能模块路由
│   ├── 📁 templates/               # 前端模板
│   ├── 📁 static/                  # 静态资源
│   │   ├── 📄 style.css            # 全局样式
│   │   └── 📁 js/                  # 交互脚本
│   ├── 📄 models.py                # 数据模型
│   └── 📄 config.py                # 应用配置
├── 📁 migrations/                  # 数据库迁移
├── 📄 run.py                       # 启动入口
└── 📄 requirements.txt             # 项目依赖
```

## 🛠️ 技术栈

- **后端**: Python 3.10+, Flask 3.0+
- **ORM**: SQLAlchemy, Flask-Migrate
- **数据库**: SQLite 
- **前端**: 响应式HTML/CSS/JS
- **AI接入**: 支持多种大型语言模型API

## 🤝 参与贡献

我们欢迎所有形式的贡献，无论是新功能、文档改进还是Bug修复！

```bash
# Fork并克隆项目
git clone https://github.com/YOUR-USERNAME/wordweb.git

# 创建特性分支
git checkout -b feature/amazing-feature

# 提交更改
git commit -m '添加了-X新功能'

# 推送分支
git push origin feature/amazing-feature

# 打开Pull Request
```

## 📜 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT) - 自由使用、修改和分发。

## 🐞 已知问题与优化计划

- 🔄 **UI闪烁问题** - 默认紧凑切换偶尔需要刷新才能生效
- ⚡ **性能优化** - 首页筛选后刷新有筛选前的残影闪过
- ⚠️ **WSL运行异常** -在WSl上运行本项目会有时会导致页面空白

---

<div align="center">
  
**WordWeb** - 让单词学习成为一种享受

⭐ 如果您喜欢这个项目，别忘了给它加个星标！

</div>

