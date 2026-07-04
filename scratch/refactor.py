import re

def refactor_test_parser():
    with open('tests/test_parser.py', 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer_src(match):
        prefix = match.group(1) # e.g. "    src = "
        quote_type = match.group(2) # " or '
        inner_text = match.group(3)
        
        # If it's already a triple quote, skip
        if quote_type == '\"\"\"' or quote_type == "'''":
            return match.group(0)
            
        # Only refactor if it contains \n
        if '\\n' not in inner_text:
            return match.group(0)

        unescaped = inner_text.replace('\\n', '\n').replace('\\t', '    ').replace('\\"', '"').replace("\\'", "'")
        
        lines = unescaped.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip() == "":
                indented_lines.append("")
            else:
                indented_lines.append("        " + line)
                
        new_text = '\n'.join(indented_lines)
        return f'{prefix}"""\n{new_text}\n    """'

    def replacer_assert(match):
        prefix = match.group(1) # e.g. "    assert Parser.parse("
        quote_type = match.group(2)
        inner_text = match.group(3)
        suffix = match.group(4) # e.g. ") == ..."
        
        if quote_type == '\"\"\"' or quote_type == "'''":
            return match.group(0)
            
        if '\\n' not in inner_text:
            return match.group(0)

        unescaped = inner_text.replace('\\n', '\n').replace('\\t', '    ').replace('\\"', '"').replace("\\'", "'")
        
        lines = unescaped.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip() == "":
                indented_lines.append("")
            else:
                indented_lines.append("        " + line)
                
        new_text = '\n'.join(indented_lines)
        return f'{prefix}"""\n{new_text}\n    """{suffix}'

    # Regex to find src = "..." or src = '...'
    pattern_src = r'(^[ \t]*src\s*=\s*)([\"\'])(.*?)(?<!\\)\2'
    content = re.sub(pattern_src, replacer_src, content, flags=re.MULTILINE)
    
    # Regex to find assert Parser.parse("...")
    pattern_assert = r'(^[ \t]*assert\s+Parser\.parse\()([\"\'])(.*?)(?<!\\)\2(\).*)'
    content = re.sub(pattern_assert, replacer_assert, content, flags=re.MULTILINE)
    
    with open('tests/test_parser.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    refactor_test_parser()
    print("Done refactoring tests/test_parser.py")
