import sqlite3
from datetime import datetime


conn = sqlite3.connect('university.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        department TEXT NOT NULL,
        date_of_birth DATE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        department TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY,
        date DATE NOT NULL,
        course_id INTEGER NOT NULL,
        max_score INTEGER NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        exam_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (exam_id) REFERENCES exams (id)
    )
''')

def check_student_exists(id):
    cursor.execute('SELECT COUNT(*) FROM Students WHERE ID = ?', (id,))
    return cursor.fetchone()[0] > 0

def check_teacher_exists(id):
    cursor.execute('SELECT COUNT(*) FROM Teachers WHERE ID = ?', (id,))
    return cursor.fetchone()[0] > 0

def check_course_exists(id):
    cursor.execute('SELECT COUNT(*) FROM Courses WHERE ID = ?', (id,))
    return cursor.fetchone()[0] > 0

def check_exam_exists(id):
    cursor.execute('SELECT COUNT(*) FROM Exams WHERE ID = ?', (id,))
    return cursor.fetchone()[0] > 0
def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def add_student():
    name = input("Введите имя студента: ")
    surname = input("Введите фамилию студента: ")
    department = input("Введите факультет студента: ")
    date_of_birth = input("Введите дату рождения студента (YYYY-MM-DD): ")
    if not validate_date(date_of_birth):
        print("Неверная дата рождения. Нужно ГГГГ-ММ-ДД")
        return
    try:
        cursor.execute('''
            INSERT INTO students (name, surname, department, date_of_birth)
            VALUES ( ?, ?, ?, ?)
        ''', (name, surname, department, date_of_birth))
        
        conn.commit()
        print("Студент успешно добавлен!")
    except sqlite3.Error:
        print('Ошибка при добавлении студента.')

    

def add_teacher():
    name = input("Введите имя преподавателя: ")
    surname = input("Введите фамилию преподавателя: ")
    department = input("Введите кафедру преподавателя: ")
    try:
        cursor.execute('''
            INSERT INTO teachers (name, surname, department)
            VALUES (?, ?, ?)
        ''', (name, surname, department))

        conn.commit()
        print("Преподаватель успешно добавлен!")
    except sqlite3.Error:
        print("Ошибка при добавлении преподавателя")
def add_course():
    title = input("Введите название курса: ")
    description = input("Введите описание курса: ")
    teacher_id = input("Введите ID преподавателя: ")
    if not check_teacher_exists(teacher_id):
        print(f'Ошибка: Преподаватель с ID {teacher_id} не существует.')
        return
    try:
        cursor.execute('''
            INSERT INTO courses (title, description, teacher_id)
            VALUES (?, ?, ?)
        ''', (title, description, teacher_id))

        conn.commit()
        print("Курс успешно добавлен!")
    except sqlite3.Error:
        print("Ошибка при доваблении курса")
def add_exam():
    date = input("Введите дату экзамена (YYYY-MM-DD): ")
    course_id = input("Введите ID курса: ")
    max_score = input("Введите максимальный балл: ")
    if not validate_date(date):
        print('Ошибка: Неправильный формат даты. Используйте формат YYYY-MM-DD.')
        return
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return
    try:
        cursor.execute('''
            INSERT INTO exams (date, course_id, max_score)
            VALUES (?, ?, ?)
        ''', (date, course_id, max_score))
        conn.commit()
        print("Экзамен успешно добавлен!")
    except sqlite3.Error as e:
        print("Ошибка при добавлении экзамена")
        print(e)
    
def add_grade():
    student_id = input("Введите ID студента: ")
    exam_id = input("Введите ID экзамена: ")
    score = input("Введите оценку: ")
    if not check_student_exists(student_id):
        print(f'Ошибка: Студент с ID {student_id} не существует.')
        return
    if not check_exam_exists(exam_id):
        print(f'Ошибка: Экзамен с ID {exam_id} не существует.')
        return
    try:
        cursor.execute('''
            INSERT INTO grades (student_id, exam_id, score)
            VALUES (?, ?, ?)
        ''', (student_id, exam_id, score))
   
        conn.commit()
        print("Оценка успешно добавлена!")
    except sqlite3.Error:
        print("Ошибка при добавлении оценки")
def update_student():
    student_id = input("Введите ID студента для изменения: ")
    name = input("Введите новое имя студента: ")
    surname = input("Введите новую фамилию студента: ")
    department = input("Введите новый факультет студента: ")
    date_of_birth = input("Введите новую дату рождения студента (YYYY-MM-DD): ")
    if not check_student_exists(student_id):
        print(f'Ошибка: Студент с ID {student_id} не существует.')
        return
    if not validate_date(date):
        print('Ошибка: Неправильный формат даты. Используйте формат YYYY-MM-DD.')
        return
    try:
        cursor.execute('''
            UPDATE students
            SET name = ?, surname = ?, department = ?, date_of_birth = ?
            WHERE id = ?
        ''', (name, surname, department, date_of_birth, student_id))

        conn.commit()
        print("Информация о студенте успешно обновлена!")
    except sqlite3.Error:
        print("Ошибка при обновлении студдента")
def update_teacher():
    teacher_id = input("Введите ID преподавателя для изменения: ")
    name = input("Введите новое имя преподавателя: ")
    surname = input("Введите новую фамилию преподавателя: ")
    department = input("Введите новую кафедру преподавателя: ")
    if not check_teacher_exists(teacher_id):
        print(f'Ошибка: Преподаватель с ID {teacher_id} не существует.')
        return
    try:
        cursor.execute('''
            UPDATE teachers
            SET name = ?, surname = ?, department = ?
            WHERE id = ?
        ''', (name, surname, department, teacher_id))

        conn.commit()
        print("Информация о преподавателе успешно обновлена!")
    except sqlite3.Error:
        print("Ошибка про обновлении преподавателя")  
def update_course():
    course_id = input("Введите ID курса для изменения: ")
    title = input("Введите новое название курса: ")
    description = input("Введите новое описание курса: ")
    teacher_id = input("Введите новый ID преподавателя: ")
    if not check_teacher_exists(teacher_id):
        print(f'Ошибка: Преподаватель с ID {teacher_id} не существует.')
        return
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return
    try:
        cursor.execute('''
        UPDATE courses
        SET title = ?, description = ?, teacher_id = ?
        WHERE id = ?
        ''', (title, description, teacher_id, course_id))

        conn.commit()
        print("Информация о курсе успешно обновлена!")
    except sqlite3.Error:
        print("Ошибка при обновлении курса")
def delete_student():
    student_id = input("Введите ID студента для удаления: ")
    if not check_student_exists(student_id):
        print(f'Ошибка: Студент с ID {student_id} не существует.')
        return
    try:
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        if cursor.rowcount == 0:
            print(f"Студент с ID '{student_id}' не найден.")
        else:
            conn.commit()
            print(f"Студент с ID '{student_id}' успешно удалён.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении студента: {e}")

def delete_teacher():
    teacher_id = input("Введите ID преподавателя для удаления: ")
    if not check_teacher_exists(teacher_id):
        print(f'Ошибка: Преподаватель с ID {teacher_id} не существует.')
        return
    try:
        cursor.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
        if cursor.rowcount == 0:
            print(f"Преподаватель с ID '{teacher_id}' не найден.")
        else:
            conn.commit()
            print(f"Преподаватель с ID '{teacher_id}' успешно удалён.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении преподавателя: {e}")

def delete_course():
    course_id = input("Введите ID курса для удаления: ")
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return
    try:
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        if cursor.rowcount == 0:
            print(f"Курс с ID '{course_id}' не найден.")
        else:
            conn.commit()
            print(f"Курс с ID '{course_id}' успешно удалён.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении курса: {e}")

def delete_exam():
    exam_id = input("Введите ID экзамена для удаления: ")
    if not check_exam_exists(exam_id):
        print(f'Ошибка: Экзамен с ID {exam_id} не существует.')
        return
    try:
        cursor.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
        if cursor.rowcount == 0:
            print(f"Экзамен с ID '{exam_id}' не найден.")
        else:
            conn.commit()
            print(f"Экзамен с ID '{exam_id}' успешно удалён.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении экзамена: {e}")
def get_students_by_department():
    department = input("Введите название факультета: ")
    try:
        cursor.execute('''
            SELECT name, surname, date_of_birth
            FROM students
            WHERE department = ?
        ''', (department,))
        students = cursor.fetchall()
    except sqlite3.Error:
        print(f"Ошибка при поиске студентов")
        

    

    if students:
        print(f"\nСписок студентов на факультете '{department}':")
        for student in students:
            print(f"Имя: {student[0]}, Фамилия: {student[1]}, Дата рождения: {student[2]}")
    else:
        print(f"Нет студентов на факультете '{department}'.")

def get_courses_by_teacher():
    teacher_id = input("Введите ID преподавателя: ")
    if not check_teacher_exists(teacher_id):
        print(f'Ошибка: Преподаватель с ID {teacher_id} не существует.')
        return
    try:
        cursor.execute('''
            SELECT title, description
            FROM courses
            WHERE teacher_id = ?
        ''', (teacher_id,))
        courses = cursor.fetchall()
    except sqlite3.Error:
        print(f"Ошибка при поиске курсов")

    if courses:
        print(f"\nСписок курсов, читаемых преподавателем с ID '{teacher_id}':")
        for course in courses:
            print(f"Название: {course[0]}, Описание: {course[1]}")
    else:
        print(f"Нет курсов, читаемых преподавателем с ID '{teacher_id}'.")

def get_students_by_course():
    course_id = input("Введите ID курса: ")
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return 
    try:
        cursor.execute('''
            SELECT s.name, s.surname
            FROM grades e
            JOIN students s ON e.student_id = s.id
            JOIN exams ex ON ex.id=e.exam_id
            WHERE ex.course_id = ?
        ''', (course_id,))

        students = cursor.fetchall()
        if students:
            print(f"\nСписок студентов, зачисленных на курс с ID '{course_id}':")
            for student in students:
                print(f"Имя: {student[0]}, Фамилия: {student[1]}")
        else:
            print(f"Нет студентов, зачисленных на курс с ID '{course_id}'.")
    except sqlite3.Error:
        print('Ошибка при получении списка студентов по курсу.')

    

def get_grades_by_course():
    course_id = input("Введите ID курса: ")
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return []

    try:
        cursor.execute('''
            SELECT  g.score
            FROM grades g
            JOIN exams s ON g.exam_id = s.id
            WHERE s.course_id = ?
        ''', (course_id,))

        grades = cursor.fetchall()
        if grades:
            print(f"\nОценки студентов за курс с ID '{course_id}':")
            for record in grades:
                print(f" Оценка: {record[0]}")
        else:
            print(f"Нет оценок для курса с ID '{course_id}'.")
    except sqlite3.Error:
        print('Ошибка при получении списка оценок по курсу.')
    
def get_average_grade_by_student_and_course():
    student_id = input("Введите ID студента: ")
    course_id = input("Введите ID курса: ")
    if not check_course_exists(course_id):
        print(f'Ошибка: Курс с ID {course_id} не существует.')
        return
    if not check_student_exists(student_id):
        print(f'Ошибка: Студент с ID {student_id} не существует.')
        return
    
    try:
        cursor.execute('''
            SELECT AVG(g.score) as average_grade
            FROM grades g
            JOIN exams c ON g.exam_id = c.id
  
            WHERE g.student_id = ? AND c.course_id = ?
        ''', (student_id, course_id))
        
        average_grade = cursor.fetchone()
        
        if average_grade and average_grade[0] is not None:
            print(f"\nСредний балл студента с ID '{student_id}' по курсу с ID '{course_id}': {average_grade[0]}")
        else:
            print(f"Нет оценок для студента с ID '{student_id}' по курсу с ID '{course_id}'.")
    
    except sqlite3.Error as e:
        print(f"Ошибка при получении среднего балла: {e}")

def get_average_grade_by_student():
    student_id = input("Введите ID студента: ")
    if not check_student_exists(student_id):
        print(f'Ошибка: Студент с ID {student_id} не существует.')
        return

    try:
        
        cursor.execute('''
            SELECT AVG(score) as average_grade
            FROM grades
            WHERE student_id = ?
        ''', (student_id,))

        average_grade = cursor.fetchone()
        if average_grade:
            print(f"\nСредний балл студента с ID '{student_id}': {average_grade[0]}")
        else:
            print(f"Нет оценок для студента с ID '{student_id}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при получении среднего балла: {e}")
        

    

def get_average_grade_by_faculty():
    department = input("Введите название факультета: ")

    try:
        cursor.execute('''
            SELECT AVG(g.score) as average_grade
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE s.department = ?
        ''', (department,))

        average_grade = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Ошибка при получении среднего балла: {e}")

    if average_grade and average_grade[0] is not None:
        print(f"\nСредний балл студентов на факультете с ID '{department}': {average_grade[0]}")
    else:
        print(f"Нет оценок для факультета с ID '{department}'.")

print('1. Добавить студента')
print('2. Добавить преподавателя')
print('3. Добавить курс')
print('4. Добавить экзамен')
print('5. Добавить оценку')
print('6. Изменить информацию о студенте')
print('7. Изменить информацию о преподавателе')
print('8. Изменить информацию о курсе ')
print('9. Удалить студента')
print('10. Удалить преподавателя')
print('11. Удалить курс')
print('12. Удалить экзамен')
print('13. Получить список студентов по факультету')
print('14. Получить список курсов, читаемых определенным преподавателем')
print('15. Получить список студентов, зачисленных на конкретный курс')
print('16. Получить оценки студентов по определенному курсу')
print('17. Средний балл студента по определенному курсу')
print('18. Средний балл студента в целом')
print('19. Средний балл по факультету')
print('20. Завершить программу')
while True:
    print('Выберите действие:')

    a=int(input())
    if a==1:
        add_student()
    elif a==2:
        add_teacher()
    elif a==3:
        add_course()
    elif a==4:
        add_exam()
    elif a==5:
        add_grade()
    elif a==6:
        update_student()
    elif a==7:
        update_teacher()
    elif a==8:
        update_course()
    elif a==9:
        delete_student()
    elif a==10:
        delete_teacher()
    elif a==11:
        delete_course()
    elif a==12:
        delete_exam()
    elif a==13:
        get_students_by_department()
    elif a==14:
        get_courses_by_teacher()
    elif a==15:
        get_students_by_course()
    elif a==16:
        get_grades_by_course()
    elif a==17:
        get_average_grade_by_student_and_course()
    elif a==18:
        get_average_grade_by_student()
    elif a==19:
        get_average_grade_by_faculty()
    elif a==20:
        break;
    else:
        print("Неверные вводные")
conn.close()  
