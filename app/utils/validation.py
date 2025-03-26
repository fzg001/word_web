import re

def validate_word_input(line):
    # 处理多种分隔符：中文破折号、英文短横线、空格等
    match = re.split(r'[-—－\s]+', line.strip(), maxsplit=1)
    if len(match) == 2:
        return match[0].strip(), match[1].strip()
    return None, None