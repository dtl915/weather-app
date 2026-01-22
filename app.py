from tkinter import W
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from sqlalchemy import DATE, VARCHAR, create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Database connection configuration
DATABASE_URL = "mysql+pymysql://root:ddxdd123@localhost:3306/weather_db?charset=utf8mb4"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Define the database model
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    city = Column(VARCHAR(45),primary_key=True)
    date = Column(DATE,primary_key=True)
    morning_temp = Column(VARCHAR(45))
    night_temp = Column(VARCHAR(45))
    morning_weather=Column(VARCHAR(45))
    night_weather=Column(VARCHAR(45))
    morning_wind=Column(VARCHAR(45))
    night_wind=Column(VARCHAR(45))


def data_request(city, date):
    year,month,day=date.split('-')

    """检查数据库是否存在指定城市和日期的数据"""
    query = session.query(WeatherData).filter_by(city=city,date=date).first()

    if query:
        # Return data from database in consistent format
        return jsonify({
            'success': True,
            'city': city,
            'weather_data': {
                'date': str(query.date),
                'morning_temperature': query.morning_temp,
                'night_temperature': query.night_temp,
                'morning_weather': query.morning_weather,
                'night_weather': query.night_weather,
                'morning_wind': query.morning_wind,
                'night_wind': query.night_wind,
                'morning_wind_speed': query.morning_wind.split('级')[0] if '级' in str(query.morning_wind) else '',
                'night_wind_speed': query.night_wind.split('级')[0] if '级' in str(query.night_wind) else ''
            }
        })
        
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response=requests.get(f"https://www.tianqihoubao.com/lishi/{city}/{year}{month}{day}.html", headers=headers)

        if not response.ok:
            return jsonify({
                'success': False,
                'error': f'无法获取 {city} 在 {date} 的天气数据。'
            })
        html=response.content.decode('utf-8')
        soup=BeautifulSoup(html,'lxml')
        
        # 通过class="weather-table"的table元素获取每日天气数据
        daily_weather_ul = soup.find('table', class_='weather-table')
        if daily_weather_ul:
            daily_items = daily_weather_ul.find_all('tr')
            
            morning_weather=daily_items[1].find_all('td')[1].get_text(strip=True)
            night_weather=daily_items[1].find_all('td')[2].get_text(strip=True)

            morning_temperature=daily_items[2].find_all('td')[1].get_text(strip=True)
            night_temperature=daily_items[2].find_all('td')[2].get_text(strip=True)

            morning_wind=daily_items[3].find_all('td')[1].get_text(strip=True)
            night_wind=daily_items[3].find_all('td')[2].get_text(strip=True)

            morning_wind_speed=morning_wind.split('级')[0] if '级' in morning_wind else ''
            night_wind_speed=night_wind.split('级')[0] if '级' in night_wind else ''


            # Insert into database with cleaned data
            try:
                new_weather_data = WeatherData(
                    city=city,
                    date=date,
                    morning_temp=morning_temperature,
                    night_temp=night_temperature,
                    morning_weather=morning_weather,
                    night_weather=night_weather,
                    morning_wind=morning_wind,
                    night_wind=night_wind
                )
                session.add(new_weather_data)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Database error: {e}")
            
            # Return scraped data in consistent format
            return jsonify({
                'success': True,
                'city': city,
                'message': f'成功获取 {city} 在 {date} 的天气数据',
                'weather_data': {
                    'date': date,
                    'morning_temperature': morning_temperature,
                    'night_temperature': night_temperature,
                    'morning_weather': morning_weather,
                    'night_weather': night_weather,
                    'morning_wind': morning_wind,
                    'night_wind': night_wind,
                    'morning_wind_speed': morning_wind_speed,
                    'night_wind_speed': night_wind_speed
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'未找到 {city} 在 {date} 的天气数据，请检查日期是否正确或该日期数据是否存在'
            })




    


@app.route('/')
def index():
    """主页路由，渲染天气查询页面"""
    return render_template('home.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    """处理天气查询请求"""
    try:
        # 获取表单数据
        city = request.form.get('city', '').strip().lower()
        date = request.form.get('date', '')
        
        # 验证输入数据
        if not city:
            return jsonify({
                'success': False,
                'error': '请输入城市名称'
            })
        
        if not date:
            return jsonify({
                'success': False,
                'error': '请选择日期'
            })
        
        # 验证日期不能是未来日期
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        yesterday = (datetime.now() - timedelta(days=1)).date()
        
        if selected_date > yesterday:
            return jsonify({
                'success': False,
                'error': '不能查询未来日期的天气数据'
            })
        # if check_db(city,date):
        #     return jsonify({
        #         'success': False,
        #         'error': '该日期数据已存在'
        #     })
        
        return data_request(city,date)

        
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': '请求超时，请稍后重试'
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'网络请求错误: {str(e)}'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': '日期格式错误'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)