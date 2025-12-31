# BeautifulSoup使用指南 - 从HTML中提取所需信息
# 本文件展示了如何使用BeautifulSoup解析HTML并提取特定信息

import requests
from bs4 import BeautifulSoup
import re

def demonstrate_beautifulsoup_usage():
    """
    演示BeautifulSoup的各种用法
    """
    
    # 1. 获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get('https://lishi.tianqi.com/beijing/202401.html', headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    
    print("=" * 60)
    print("BeautifulSoup 使用方法演示")
    print("=" * 60)
    
    # 2. 基本查找方法
    print("\n1. 基本查找方法:")
    print("-" * 30)
    
    # 2.1 通过标签名查找
    title = soup.find('title')
    print(f"页面标题: {title.text if title else 'None'}")
    
    # 2.2 通过class属性查找
    weather_ul = soup.find('ul', class_='thrui')
    print(f"找到天气列表: {'是' if weather_ul else '否'}")
    
    # 2.3 通过多个属性查找
    divs_with_temp = soup.find_all('div', class_='th140')
    print(f"找到温度div数量: {len(divs_with_temp)}")
    
    # 3. CSS选择器
    print("\n2. CSS选择器方法:")
    print("-" * 30)
    
    # 3.1 类选择器
    temp_elements = soup.select('.th140')
    print(f"通过CSS类选择器找到元素: {len(temp_elements)}个")
    
    # 3.2 属性选择器
    ul_elements = soup.select('ul[class*="tian"]')
    print(f"通过属性选择器找到ul元素: {len(ul_elements)}个")
    
    # 3.3 后代选择器
    li_in_thrui = soup.select('ul.thrui li')
    print(f"thrui类ul下的li元素: {len(li_in_thrui)}个")
    
    # 4. 文本内容提取
    print("\n3. 文本内容提取:")
    print("-" * 30)
    
    if weather_ul:
        first_li = weather_ul.find('li')
        if first_li:
            print(f"第一个天气项原始文本: {first_li.get_text()}")
            print(f"第一个天气项清理后文本: {first_li.get_text(strip=True)}")
    
    # 5. 使用正则表达式提取信息
    print("\n4. 正则表达式提取:")
    print("-" * 30)
    
    # 查找所有包含温度的文本
    temp_pattern = re.compile(r'-?\d+℃')
    all_text = soup.get_text()
    temperatures = temp_pattern.findall(all_text)
    print(f"找到的所有温度: {temperatures[:10]}...")  # 只显示前10个
    
    # 6. 实际数据提取示例
    print("\n5. 实际天气数据提取:")
    print("-" * 30)
    
    weather_data = extract_weather_data(soup)
    
    if weather_data:
        print(f"成功提取 {len(weather_data)} 天的天气数据")
        print("前3天数据:")
        for i, day in enumerate(weather_data[:3]):
            print(f"  {i+1}. {day['date']} - {day['weather']} - {day['high_temp']}~{day['low_temp']}")
    
    # 7. 月度统计数据提取
    monthly_stats = extract_monthly_stats(soup)
    if monthly_stats:
        print("\n月度统计:")
        for key, value in monthly_stats.items():
            print(f"  {key}: {value}")
    
    return weather_data, monthly_stats

def extract_weather_data(soup):
    """
    从soup对象中提取每日天气数据
    """
    weather_data = []
    
    # 查找包含每日天气的ul元素
    daily_weather_ul = soup.find('ul', class_='thrui')
    if not daily_weather_ul:
        return weather_data
    
    # 获取所有li元素
    daily_items = daily_weather_ul.find_all('li')
    
    for item in daily_items:
        item_text = item.get_text(strip=True)
        
        # 使用正则表达式解析数据
        # 格式: "2024-01-01 星期一2℃-7℃多云西风 1级"
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', item_text)
        temp_match = re.search(r'(-?\d+)℃(-?\d+)℃', item_text)
        weather_match = re.search(r'℃([^\d\s]+)', item_text)
        
        if date_match and temp_match:
            date = date_match.group(1)
            high_temp = temp_match.group(1) + '℃'
            low_temp = temp_match.group(2) + '℃'
            weather = weather_match.group(1) if weather_match else ''
            
            # 清理天气描述，只保留中文字符
            weather_clean = re.sub(r'[^\u4e00-\u9fff]', '', weather)
            
            weather_data.append({
                'date': date,
                'high_temp': high_temp,
                'low_temp': low_temp,
                'weather': weather_clean,
                'raw_text': item_text
            })
    
    return weather_data

def extract_monthly_stats(soup):
    """
    提取月度统计数据
    """
    monthly_stats = {}
    
    # 查找统计数据的ul元素
    stats_ul = soup.find('ul', class_='tian_two')
    if not stats_ul:
        return monthly_stats
    
    stats_items = stats_ul.find_all('li')
    for item in stats_items:
        text = item.get_text(strip=True)
        
        if '平均高温' in text:
            monthly_stats['平均高温'] = text
        elif '平均低温' in text:
            monthly_stats['平均低温'] = text
        elif '极端高温' in text:
            monthly_stats['极端高温'] = text
        elif '极端低温' in text:
            monthly_stats['极端低温'] = text
    
    return monthly_stats

def advanced_parsing_techniques():
    """
    演示高级解析技巧
    """
    print("\n" + "=" * 60)
    print("高级BeautifulSoup技巧")
    print("=" * 60)
    
    # 模拟一些HTML内容
    html_content = """
    <div class="weather-container">
        <div class="day" data-date="2024-01-01">
            <span class="temp-high">5℃</span>
            <span class="temp-low">-3℃</span>
            <span class="condition">晴</span>
        </div>
        <div class="day" data-date="2024-01-02">
            <span class="temp-high">7℃</span>
            <span class="temp-low">-1℃</span>
            <span class="condition">多云</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    print("\n1. 使用属性选择器:")
    print("-" * 30)
    
    # 通过data属性查找
    day_elements = soup.find_all('div', {'data-date': True})
    for day in day_elements:
        date = day.get('data-date')
        high_temp = day.find('span', class_='temp-high').text
        low_temp = day.find('span', class_='temp-low').text
        condition = day.find('span', class_='condition').text
        print(f"日期: {date}, 高温: {high_temp}, 低温: {low_temp}, 天气: {condition}")
    
    print("\n2. 使用lambda函数进行复杂查找:")
    print("-" * 30)
    
    # 查找包含特定文本的元素
    temp_elements = soup.find_all(lambda tag: tag.name == 'span' and '℃' in tag.get_text())
    print(f"找到包含温度的span元素: {len(temp_elements)}个")
    
    print("\n3. 遍历和导航:")
    print("-" * 30)
    
    # 遍历兄弟元素
    first_day = soup.find('div', class_='day')
    if first_day:
        print(f"第一天: {first_day.get('data-date')}")
        next_day = first_day.find_next_sibling('div', class_='day')
        if next_day:
            print(f"下一天: {next_day.get('data-date')}")
    
    print("\n4. 文本处理技巧:")
    print("-" * 30)
    
    # 获取纯文本，去除HTML标签
    container = soup.find('div', class_='weather-container')
    if container:
        # 获取所有文本
        all_text = container.get_text()
        print(f"所有文本: {all_text.strip()}")
        
        # 获取文本并用分隔符连接
        separated_text = container.get_text(separator=' | ', strip=True)
        print(f"分隔文本: {separated_text}")

if __name__ == "__main__":
    # 运行演示
    try:
        weather_data, monthly_stats = demonstrate_beautifulsoup_usage()
        advanced_parsing_techniques()
        
        print("\n" + "=" * 60)
        print("总结: BeautifulSoup主要方法")
        print("=" * 60)
        print("""
1. 基本查找:
   - soup.find('tag')           # 查找第一个标签
   - soup.find_all('tag')       # 查找所有标签
   - soup.find('tag', class_='class-name')  # 通过class查找
   - soup.find('tag', {'attr': 'value'})    # 通过属性查找

2. CSS选择器:
   - soup.select('.class-name')     # 类选择器
   - soup.select('#id-name')        # ID选择器
   - soup.select('tag.class')       # 标签+类选择器
   - soup.select('parent > child')  # 直接子元素
   - soup.select('parent child')    # 后代元素

3. 文本提取:
   - element.text               # 获取文本内容
   - element.get_text()         # 获取文本内容（更多选项）
   - element.get_text(strip=True)  # 去除首尾空白
   - element.get('attribute')   # 获取属性值

4. 高级技巧:
   - 使用正则表达式匹配
   - lambda函数进行复杂查找
   - 元素导航（parent, next_sibling等）
   - 条件查找和过滤
        """)
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("请确保网络连接正常，或者检查目标网站是否可访问。")