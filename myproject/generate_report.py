import requests
import pandas as pd
import plotly.express as px
import re
from datetime import datetime

# 1. Настройки API
BASE_URL = "http://localhost:8000/"
AUTH_CREDENTIALS = {
    'username': 'admin',  # Или 'email' если используете email для входа
    'password': 'admin'   # Ваш пароль админа
}

def get_auth_token():
    """Получение JWT токена"""
    try:
        response = requests.post(
            f"{BASE_URL}api/token/",
            data=AUTH_CREDENTIALS,  # Обратите внимание на data вместо json
            timeout=5
        )
        response.raise_for_status()
        return response.json().get('access')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка аутентификации: {str(e)}")
        print(f"Response: {response.text if 'response' in locals() else ''}")
        return None

def fetch_api_data(endpoint, token):
    """Получение данных из API"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}api/{endpoint}/",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения данных {endpoint}: {str(e)}")
        return []

def generate_report():
    """Основная функция генерации отчета"""
    print("Начало генерации отчета...")
    
    # 1. Получаем токен
    token = get_auth_token()
    if not token:
        print("Не удалось получить токен доступа. Проверьте:")
        print("- Запущен ли сервер Django")
        print("- Правильность учетных данных в AUTH_CREDENTIALS")
        print("- Доступность эндпоинта /api/token/")
        return
    
    # 2. Получаем данные
    people_data = fetch_api_data("people", token)
    additional_data = fetch_api_data("additional-data", token)
    
    if not people_data:
        print("Нет данных для генерации отчета")
        return
    
    # 3. Подготавливаем данные
    df = pd.DataFrame(people_data)
    
    # 4. Создаем графики
    figures = []
    
    # График 1: Распределение по типам жилья
    if 'type_house' in df.columns:
        fig1 = px.pie(
            df,
            names='type_house',
            title='Распределение по типам жилья',
            hole=0.3
        )
        figures.append(fig1)
    
    # График 2: Количество техники
    if 'electrical_appliances' in df.columns:
        df['appliance_count'] = df['electrical_appliances'].apply(
            lambda x: len(x.split(',')) if x else 0
        )
        fig2 = px.histogram(
            df,
            x='appliance_count',
            title='Количество техники на пользователя',
            labels={'appliance_count': 'Количество приборов'}
        )
        figures.append(fig2)
    
    # 5. Генерируем отчет
    if figures:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Отчет пользователей</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .plot {{ margin: 20px auto; max-width: 900px; }}
            </style>
        </head>
        <body>
            <h1>Аналитический отчет</h1>
            <p>Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        """
        
        for fig in figures:
            html_content += f"""
            <div class="plot">
                {fig.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            """
        
        html_content += "</body></html>"
        
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Отчет сохранен как: {filename}")
    else:
        print("Нет данных для визуализации")

if __name__ == "__main__":
    generate_report()