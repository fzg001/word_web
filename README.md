# WordWeb - 分组别英文词汇学习系统

## 项目简介

WordWeb 是一个分组管理的英语单词学习系统，支持卡片式界面、AI自动生成单词、全局搜索、深浅主题切换、数据备份等功能。适合高效管理和学习词汇。

## 主要功能

- 单词组管理：创建、编辑、删除、排序
- 多模式学习：背诵、顺序测试、乱序测试
- AI生成单词：输入主题自动生成单词表
- 全局搜索：支持命令式快速跳转
- 主题切换：深色/浅色/自动
- 数据备份与WebDAV同步
  
### 多种动态卡片界面
![主页卡片展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/1abca16653d4bd62cddcaf75cbc1e97d.gif)

### AI生成单词
![AI生成单词功能展示](https://fzg-1324261000.cos.ap-nanjing.myqcloud.com/markdown/5afaeebac96d47115fa3e0c4512339b4.gif)

## 部署

### 传统部署

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

### Docker

```bash
# 拉取镜像
docker pull rheshyike/wordweb:latest

# 启动容器
docker run -p 5000:5000 -v wordweb_data:/app/instance rheshyike/wordweb:latest
```

访问 http://localhost:5000/ 即可使用！

## AI配置

在设置页面填写API密钥、模型等参数，保存后即可使用AI生成功能。

```json
{
    "api_key": "your_api_key",
    "model": "deepseek-ai/DeepSeek-V3",
    "temperature": 0.7,
    "max_tokens": 2000,
    "api_base_url": "https://api.xxxx.com/v3"
}
```

## 目录结构

```
wordweb/
├── app/
│   ├── blueprints/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   └── config.py
├── migrations/
├── run.py
└── requirements.txt
```

## 技术栈

- Python 3.10+, Flask 3.0+
- SQLAlchemy, Flask-Migrate
- SQLite
- HTML/CSS/JS

## 许可证

MIT License

---
更多信息请见源码或直接体验系统。

