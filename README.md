# WordWeb - 单词学习管理系统

## 项目简介

WordWeb 是一个基于 Flask 框架开发的单词学习管理系统，旨在帮助用户高效地管理单词组、进行单词背诵和测试。用户可以创建、编辑和删除单词组，在背诵模式下逐个学习单词，还能通过顺序或乱序测试检验学习效果。系统会记录每个单词组的学习统计信息，如背诵次数、测试正确率等。

## 功能特性

- **单词组管理**：支持创建、编辑和删除单词组，方便用户组织和整理单词。
- **背诵模式**：提供分页浏览单词的功能，支持使用键盘方向键快速导航，完成背诵后自动记录背诵次数。
- **测试模式**：包括顺序和乱序两种测试模式，自动计算正确率并记录在数据库中。
- **数据验证**：在创建和编辑单词组时，对输入的单词进行格式验证，确保数据的准确性。

## 技术栈

- **后端**：Python 3.12.9、Flask 3.0.2、Flask-SQLAlchemy 3.1.1、Flask-Migrate 4.0.5
- **前端**：HTML、CSS、JavaScript
- **数据库**：SQLite

## 安装与运行

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/wordweb.git
cd wordweb
```

### 2. 创建并激活虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # 对于 Windows 用户，使用 `venv\Scripts\activate`
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并添加以下内容：

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///wordweb.db
```

### 5. 初始化数据库

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. 运行项目

```bash
python run.py
```

打开浏览器，访问 `http://0.0.0.0:5000` 即可开始使用。

## 项目结构

```plaintext
wordweb/
├── app/
│   ├── blueprints/
│   │   ├── main.py
│   │   ├── groups.py
│   │   └── practice.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── create_group.html
│   │   ├── edit_group.html
│   │   ├── manage_groups.html
│   │   ├── group_detail.html
│   │   ├── study_mode.html
│   │   └── quiz_mode.html
│   ├── models.py
│   ├── __init__.py
│   ├── config.py
│   └── utils/
│       └── validation.py
├── migrations/
│   ├── env.py
│   └── alembic.ini
├── static/
│   └── style.css
├── run.py
└── requirements.txt
```

## 贡献指南

如果你想为这个项目做出贡献，请遵循以下步骤：

1. Fork 这个仓库。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature-name`。
5. 打开一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。