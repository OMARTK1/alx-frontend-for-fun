#!/usr/bin/python3
"""
Script coding Markdown to HTML
"""
import sys
import os
import hashlib

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r') as infile:
        markdown_lines = infile.readlines()

    html_lines = convert_markdown_to_html(markdown_lines)

    with open(output_file, 'w') as outfile:
        outfile.writelines(html_lines)

def convert_markdown_to_html(markdown_lines):
    html_lines = []
    in_list = False
    in_ordered_list = False

    for line in markdown_lines:
        line = line.rstrip()
        # Part Headings
        if line.startswith('#'):
            level = len(line.split()[0])
            content = line[level+1:].strip()
            content = convert_bold_and_emphasis(content)
            content = convert_special_markdown(content)
            html_lines.append(f"<h{level}>{content}</h{level}>\n")

        # Part Unordered lists
        elif line.startswith('- '):
            if not in_list:
                in_list = True
                html_lines.append("<ul>\n")
            content = line[2:].strip()
            content = convert_bold_and_emphasis(content)
            content = convert_special_markdown(content)
            html_lines.append(f"  <li>{content}</li>\n")

        # Part Ordered lists
        elif line.startswith('* '):
            if not in_ordered_list:
                in_ordered_list = True
                html_lines.append("<ol>\n")
            content = line[2:].strip()
            content = convert_bold_and_emphasis(content)
            content = convert_special_markdown(content)
            html_lines.append(f"  <li>{content}</li>\n")

        # Part Paragraphs
        else:
            if in_list:
                in_list = False
                html_lines.append("</ul>\n")
            if in_ordered_list:
                in_ordered_list = False
                html_lines.append("</ol>\n")
            if line.strip():
                content = line.strip()
                content = convert_bold_and_emphasis(content)
                content = convert_special_markdown(content)
                html_lines.append(f"<p>{content}</p>\n")

    if in_list:
        html_lines.append("</ul>\n")
    if in_ordered_list:
        html_lines.append("</ol>\n")

    return html_lines

def convert_bold_and_emphasis(line):
    line = line.replace("**", "<b>").replace("__", "<em>")
    line = line.replace("**", "</b>").replace("__", "</em>")
    return line

def convert_special_markdown(line):
    if '[[' in line and ']]' in line:
        start = line.find('[[') + 2
        end = line.find(']]')
        content = line[start:end]
        md5_hash = hashlib.md5(content.encode()).hexdigest()
        line = line.replace(f'[[{content}]]', md5_hash)
    if '((' in line and '))' in line:
        start = line.find('((') + 2
        end = line.find('))')
        content = line[start:end]
        line = line.replace(f'(({content}))', content.replace('c', '').replace('C', ''))
    return line

if __name__ == "__main__":
    main()
