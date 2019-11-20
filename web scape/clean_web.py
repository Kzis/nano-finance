import requests
from bs4 import BeautifulSoup
import re
import lxml
from lxml.html.clean import Cleaner

def get_content(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
    except:
        soup = None
    return soup

def clean_tag(msg):
    #remove html tag
    Tag_clean = re.compile(r'<[^>]+>')
    msg = Tag_clean.sub('', msg)
    #remove # and  “ , ”
    msg = re.sub(r'#|"|"', '', msg)
    #remove separator (\n, \t)
    msg = ''.join(msg.split())
    #remove numeric
    #msg = ''.join([i for i in msg if not i.isdigit()])
    return msg

def clean_cs_js(url):
    soup = get_content(url)
    if soup is not None:
        # remove all javascript and stylesheet code
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        #drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
    else:
        text = 'can not read this page'
    return text

url = "https://www.thairath.co.th/news/politic/1647081"
raw_content = get_content(url)
#content_no_html = clean_html(raw_content)
content_cleaned = clean_cs_js(url)

print(content_cleaned)
