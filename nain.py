from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import requests


app = Flask(__name__)



def create_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ablomis***678",
        database="tankist"
    )
    return connection

def fetch_vacancies(params):
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_resumes(params):
    response = requests.get('https://api.hh.ru/resumes', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_vacancies_to_db(connection, vacancies):
    cursor = connection.cursor()
    query_insert = "INSERT INTO vacancies (id, name, employer, url, city) VALUES (%s, %s, %s, %s, %s)"
    query_select = "SELECT id FROM vacancies WHERE id = %s"
    for vacancy in vacancies['items']:
        data = (
            vacancy['id'],
            vacancy['name'],
            vacancy['employer']['name'],
            vacancy['alternate_url'],
            vacancy['area']['name']
        )
        cursor.execute(query_select, (vacancy['id'],))
        existing_record = cursor.fetchone()
        if not existing_record:
            cursor.execute(query_insert, data)
        else:
            print(f"Vacancy with id {vacancy['id']} already exists. Skipping insertion.")
    connection.commit()
    cursor.close()

def save_resumes_to_db(connection, resumes):
    cursor = connection.cursor()
    query = "INSERT INTO resumes (id, title, first_name, last_name, url) VALUES (%s, %s, %s, %s, %s)"
    for resume in resumes['items']:
        data = (
            resume['id'],
            resume['title'],
            resume['first_name'],
            resume['last_name'],
            resume['alternate_url']
        )
        cursor.execute(query, data)
    connection.commit()
    cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    company = request.form.get('company')
    city = request.form.get('city')
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM vacancies WHERE employer LIKE %s AND city LIKE %s"
    cursor.execute(query, (f"%{company}%", f"%{city}%"))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
