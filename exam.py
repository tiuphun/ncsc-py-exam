import requests 
import html 
import argparse
import sys
import os
import re
import io
 
path = './exploit-db' 
 
def exploit_func(input):
    match = re.search(r'(\d+)$', input)
    if match:
        id = match.group(1)
    else:
        print("Invalid input. Please provide either an ID or a full URL.")
        return

    filename = os.path.join(path, f'{id}.txt')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        os.startfile(filename)
    else:
        url = 'https://exploit-db.com/exploits/{}'.format(id) 
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} 
        res= requests.get(url, headers = headers) 
    
        if res.status_code == 404:
            print(f"Exploit {id} does not exist.")
            return

        exploit = res.text[res.text.find('<code') : res.text.find('</code>')] 
        exploit = html.unescape(exploit[exploit.find('">') +2 :]) 

        with open(filename, 'w') as file:
            file.write(exploit)
        os.startfile(filename)

def page_func(page): 
    page = int(page)
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    files.sort(key=lambda f: int(re.search(r'(\d+)', f).group(1)))

    # Divide the files into pages of 5
    pages = [files[i:i+5] for i in range(0, len(files), 5)]

    if page < len(pages):
        for file in pages[page]:
            id = re.search(r'(\d+)', file).group(1)
            print(id)
    else:
        print("Invalid page number.")


def search_func(keyword): 
    words = re.split(r'\s+', keyword)

    # Create a regex pattern that matches any of the words
    # pattern = re.compile('|'.join(words))

    # If case insensitive
    pattern = re.compile('|'.join(words), re.IGNORECASE)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename, 'r') as f:
                content = f.read()
                if pattern.search(content):
                    print(filename.replace('\\', '/')) 


if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Python Exam')
    # group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--exploit', type=str, help='exploit ID')
    parser.add_argument('--page', type=str, help='get page')
    parser.add_argument('--search', type=str, help='Search keyword')

    # error_io = io.StringIO()
    # parser.error = lambda message: error_io.write(message)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    if args.exploit:
        exploit_func(args.exploit)
    elif args.page:
        page_func(args.page)
    elif args.search:
        search_func(args.search)