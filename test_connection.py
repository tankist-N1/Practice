import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ablomis***678",
        database="tankist"
    )
    return connection
import requests
import mysql.connector

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

def create_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ablomis***678",
        database="tankist"
    )
    return connection

def save_vacancies_to_db(connection, vacancies):
    cursor = connection.cursor()
    query_insert = "INSERT INTO vacancies (id, name, employer, url, city) VALUES (%s, %s, %s, %s, %s)"
    query_select = "SELECT id FROM vacancies WHERE id = %s"
    query = "INSERT INTO vacancies (id, name, employer, url, city) VALUES (%s, %s, %s, %s, %s)"
    for vacancy in vacancies['items']:
        data = (
            vacancy['id'],
            vacancy['name'],
            vacancy['employer']['name'],
            vacancy['alternate_url'],
            vacancy['area']['name']  # Добавляем город
        )
         # Проверяем, существует ли уже запись с таким id
        cursor.execute(query_select, (vacancy['id'],))
        existing_record = cursor.fetchone()
        
        if not existing_record:
            # Если записи нет, вставляем новую запись
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

def main():
    params = {
        'per_page': 100,
        'page': 0
    }

    connection = create_connection()

    vacancies = fetch_vacancies(params)
    if vacancies:
        save_vacancies_to_db(connection, vacancies)
        print("Vacancies:")
        for vacancy in vacancies['items']:
            print(f"ID: {vacancy['id']}, Name: {vacancy['name']}, Employer: {vacancy['employer']['name']}, City: {vacancy['area']['name']}, URL: {vacancy['alternate_url']}")

    resumes = fetch_resumes(params)
    if resumes:
        save_resumes_to_db(connection, resumes)
        print("Resumes:")
        for resume in resumes['items']:
            print(f"ID: {resume['id']}, Title: {resume['title']}, First Name: {resume['first_name']}, Last Name: {resume['last_name']}, URL: {resume['alternate_url']}")

    connection.close()

if __name__ == "__main__":
    main()


def create_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ablomis***678",
        database="tankist"
    )
    return connection


def main():
    params = {
        'per_page': 100,
        'page': 0
    }

    connection = create_connection()

    vacancies = fetch_vacancies(params)
    if vacancies:
        save_vacancies_to_db(connection, vacancies)

    resumes = fetch_resumes(params)
    if resumes:
        save_resumes_to_db(connection, resumes)

    connection.close()

if __name__ == "__main__":
    main()
