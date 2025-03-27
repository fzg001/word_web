# WordWeb - 单词学习管理系统

## 项目简介

WordWeb 是一个基于 Flask 框架开发的单词学习管理系统，旨在帮助用户高效地管理单词组、进行单词背诵和测试。用户可以创建、编辑和删除单词组，在背诵模式下逐个学习单词，还能通过顺序或乱序测试检验学习效果。系统会记录每个单词组的学习统计信息，如背诵次数、测试正确率等。在 v1.1.0 版本中，新增了 AI 大模型生成单词的功能，让用户可以更便捷地获取所需单词。

## v1.0.0 功能特性

- **单词组管理**：支持创建、编辑和删除单词组，方便用户组织和整理单词。
- **背诵模式**：提供分页浏览单词的功能，支持使用键盘方向键快速导航，完成背诵后自动记录背诵次数。
- **测试模式**：包括顺序和乱序两种测试模式，自动计算正确率并记录在数据库中。
- **数据验证**：在创建和编辑单词组时，对输入的单词进行格式验证，确保数据的准确性。

![image-20250327133003018](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327133003018.png)

![image-20250327133015326](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327133015326.png)

![image-20250327133029748](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327133029748.png)

## v1.1.0 新增特性

### AI 大模型生成单词

在创建新单词组时，用户可以利用 AI 大模型根据指定主题生成单词列表。只需输入想要的单词主题，点击“AI 生成”按钮，系统将自动调用大模型生成相关单词，为用户节省手动输入单词的时间和精力。

![image-20250327150909251](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327150909251.png)

可在设置界面进行配置，配置完成后，请点击测试连接进行测试，测试无误后即可使用AI生成单词。

![image-20250327150945288](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327150945288.png)

## 技术栈

- **后端**：Python 3.12.9、Flask 3.0.2、Flask - SQLAlchemy 3.1.1、Flask - Migrate 4.0.5
- **前端**：HTML、CSS、JavaScript
- **数据库**：SQLite

## 安装与运行

### 1. 克隆项目

```Bash
git clone https://github.com/yourusername/wordweb.git
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

### 5. 配置 AI 设置（非必须，后续可从应用的设置界面进行配置）

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

请将 `your_api_key` 替换为你自己的 OpenAI API 密钥。

### 6. 初始化数据库

```Bash
flask db init
flask db migrate
flask db upgrade
```

### 7. 运行项目

```Bash
python run.py
```

打开浏览器，访问 `http://0.0.0.0:5000` 即可开始使用。

## 使用步骤

### 1. 创建新单词组

- 打开浏览器，访问 `http://0.0.0.0:5000`，进入系统首页。
- 点击新建组别的链接，进入创建页面。![image-20250327151113066](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151113066.png)
- 在“组别名称”输入框中输入单词组的名称，例如“生物学基础词汇”。
- 若想手动输入单词，在“单词列表”输入框中按照“英文 - 中文”的格式逐行输入单词，支持带序号和格式标记的输入，如: "1. **Word** - 单词"。
- 若想使用 AI 生成单词，在输入“组别名称”后，点击“🤖 AI 生成”按钮。
- 系统将调用 AI 大模型生成相关单词列表，并自动填充到“单词列表”输入框中。
- 检查生成的单词列表，如有需要可进行手动修改。
- ![image-20250327151253174](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151253174.png)
- 点击“提交”按钮，系统将验证输入的单词格式，并创建新的单词组。

### 2. 编辑单词组

- 在系统首页或单词组管理页面，找到需要编辑的单词组，点击“编辑”链接。
- 在编辑页面，可以修改“组别名称”和“单词列表”。
- ![image-20250327151339120](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151339120.png)
- 完成修改后，点击“提交”按钮，系统将更新单词组信息。

### 3. 删除单词组

- 在系统首页或单词组管理页面，找到需要删除的单词组，点击“删除”按钮。
- 系统将提示确认删除操作，确认后将删除该单词组及其包含的所有单词。![image-20250327151413903](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151413903.png)

### 4. 背诵单词

- 在系统首页，找到想要背诵的单词组，点击“背诵”链接。![image-20250327151501164](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151501164.png)
- 进入背诵模式，系统将分页显示单词，支持使用键盘方向键快速导航。![image-20250327151510421](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151510421.png)
- 完成所有单词的背诵后，系统将自动记录背诵次数。![image-20250327151520523](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151520523.png)

### 5. 测试单词

- 在系统首页，找到想要测试的单词组。
- 选择顺序或乱序测试模式，开始测试。
- 系统将逐个显示英文单词，用户需要输入对应的中文释义。
- 提交答案后，系统将自动判断对错，并计算正确率。
- 测试完成后，系统将记录测试结果，包括测试次数和正确率。![image-20250327151602350](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/image-20250327151602350.png)

## 项目结构

```Plain
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