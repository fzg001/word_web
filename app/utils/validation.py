import re

def validate_word_input(line):
    """验证并解析单词输入行"""
    # 移除序号和前导空格
    # 例如 "1. Word - 单词" => "Word - 单词"
    line = re.sub(r'^\s*\d+[\.\)、]\s*', '', line.strip())
    
    # 移除标签 <strong>, <em> 等
    line = re.sub(r'<[^>]+>', '', line)
    
    # 识别常见分隔符
    separators = [' - ', ':', '：', '-', '—', '–', ' : ']
    separator_found = None
    
    for sep in separators:
        if sep in line:
            separator_found = sep
            break
    
    if separator_found:
        # 分割英文和中文部分
        parts = line.split(separator_found, 1)  # 限制只分割一次
        eng = parts[0].strip()
        chn = parts[1].strip() if len(parts) > 1 else ''
        
        # 清理英文和中文部分中可能存在的标点符号
        eng = re.sub(r'[""''<>《》()（）[\]]+', '', eng)
        chn = re.sub(r'[""''<>《》()（）[\]]+', '', chn)
        
        # 确保两部分都非空
        if eng and chn:
            return eng.strip(), chn.strip()
    
    return None, None