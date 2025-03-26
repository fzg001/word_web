import re

def validate_word_input(line):
    # 去除空行
    if not line or line.isspace():
        return None, None
    
    # 去除行首的数字序号（如 "1.", "2. ", "3、"）
    line = re.sub(r'^\d+[.、\s]+', '', line.strip())
    
    # 处理多种分隔符：中文破折号、英文短横线、空格等
    match = re.split(r'[-—－\s]+', line, maxsplit=1)
    if len(match) == 2:
        eng, chn = match[0].strip(), match[1].strip()
        
        # 去除英文周围的星号、加粗符号等格式标记
        eng = re.sub(r'[*_\[\]<>"\']+', '', eng)
        
        # 去除中文周围可能的引号、括号等
        chn = re.sub(r'[""''<>《》()（）[\]]+', '', chn)
        
        return eng.strip(), chn.strip()
    
    return None, None