import requests
from bs4 import BeautifulSoup

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 获取网页内容
response = requests.get('https://lishi.tianqi.com/beijing/202401.html', headers=headers)
soup = BeautifulSoup(response.content, 'lxml')

print('页面标题:', soup.title.text if soup.title else 'None')
print('\n' + '='*60)

# 查找所有div元素，寻找天气数据容器
print('查找可能包含天气数据的div元素:')
divs_with_class = soup.find_all('div', class_=True)
for i, div in enumerate(divs_with_class[:10]):
    class_name = ' '.join(div.get('class', []))
    text_content = div.get_text(strip=True)[:100]
    if any(keyword in text_content for keyword in ['温度', '天气', '℃', '°', '晴', '雨', '云']):
        print(f'Div {i+1} - Class: {class_name}')
        print(f'内容: {text_content}...')
        print('-' * 40)

# 查找所有ul和li元素
print('\n' + '='*60)
print('查找列表元素(ul/li):')
uls = soup.find_all('ul')
for i, ul in enumerate(uls[:5]):
    class_name = ' '.join(ul.get('class', [])) if ul.get('class') else 'no-class'
    lis = ul.find_all('li')[:3]  # 只看前3个li
    print(f'UL {i+1} - Class: {class_name}, 包含 {len(ul.find_all("li"))} 个li')
    for j, li in enumerate(lis):
        li_text = li.get_text(strip=True)[:80]
        print(f'  LI {j+1}: {li_text}')
    print('-' * 40)

# 查找所有包含数字和温度符号的元素
print('\n' + '='*60)
print('查找包含温度信息的元素:')
temp_elements = soup.find_all(string=lambda text: text and ('℃' in text or '°' in text))
for i, elem in enumerate(temp_elements[:10]):
    parent_tag = elem.parent.name if elem.parent else 'None'
    parent_class = ' '.join(elem.parent.get('class', [])) if elem.parent and elem.parent.get('class') else 'no-class'
    print(f'温度元素{i+1}: "{elem.strip()}" (父元素: {parent_tag}, class: {parent_class})')

# 查找所有span元素
print('\n' + '='*60)
print('查找span元素:')
spans = soup.find_all('span')
for i, span in enumerate(spans[:10]):
    class_name = ' '.join(span.get('class', [])) if span.get('class') else 'no-class'
    text_content = span.get_text(strip=True)
    if text_content and len(text_content) < 50:  # 只显示较短的文本
        print(f'Span {i+1} - Class: {class_name}, 内容: "{text_content}"')