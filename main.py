import mysql.connector as mysqLtor
import os
import platform
import datetime
import re
import random

def isPresent(obj,data):
    ans = False
    for row in data:
        if obj in row:
            ans = True
            break
    return ans

def grade_entry():
    print("10.EX")
    print("9. A")
    print("8. B")
    print("7. C")
    print("6. D")
    print("5. P")
    print("4. F")

    while True:
        try:
            grade = int(input("Enter your grade:"))
            if grade<4 or grade>10:
                raise InvalidChoice("")
            return grade
        except ValueError:
            print("Invalid Choice!!!")
        except InvalidChoice:
            print("Invalid Choice!!!")


        
def email_verification(receiver_email):
    email_check1 = ["gmail","hotmail","yahoo","outlook"]
    email_check2 = [".com",".in",".org",".edu",".co.in"]
    count = 0

    for domain in email_check1:
        if domain in receiver_email:
            count+=1
    for site in email_check2:
        if site in receiver_email:
            count+=1

    if "@" not in receiver_email or count!=2:
        print("invalid email id")
        return None
    
    return receiver_email
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class InvalidId(Exception):
    pass

class InvalidMailId(Exception):
    pass

class UnauthEntry(Exception):
    pass
class InvalidNumber(Exception):
    pass

class InvalidChoice(Exception):
    pass

def Department_Choice():
    departments = [
    "Computer Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Bioengineering",
    "Aerospace Engineering",
    "Materials Science and Engineering",
    "Industrial Engineering",
    "Nuclear Engineering",
    "Environmental Engineering"]
    i = 1
    for dept in departments:
        print(i,". {}".format(dept))
        i += 1
    try:
        choice = int(input("Enter the choice:"))
        if choice < 1 or choice >= i:
            raise InvalidChoice("")
        return departments[choice-1]
    except ValueError:
        print("Invalid Choice!!!")
    except InvalidChoice:
        print("Invalid Choice!!!")
    return None



def insert_new_record(cursor):
    cursor.execute("select * from students")
    records = cursor.fetchall()
    try: 
        student_id = int(input("Enter the new student id:"))
        if isPresent(student_id,records):
            raise InvalidId("")
        name = input("Enter the student name:")
        department = Department_Choice()
        if department == None:
            raise InvalidChoice("")
        print("Enter Student's DOB:")
        year = int(input("Enter the year:"))
        month = int(input("Enter the month:"))
        day = int(input("Enter the date:"))
        date = datetime.date(year,month,day)
        date = date.strftime("%Y-%m-%d")
        print(date)
        email = input("Enter the email address:")
        if email_verification(email) == None:
            raise InvalidMailId("")
        st = "Insert into students Values({},'{}','{}','{}','{}')".format(student_id,name,department,date,email)
        cursor.execute(st)


    except InvalidMailId:
        return 
    except UnauthEntry:
        print("Unauthorised Entry!!!")
    except ValueError:
        print("Invalid Entry!!!")
    except InvalidId:
        print("Student Id already exists!!!")
    except InvalidChoice:
        return
    
def register_courses(cursor):
    try:
        course_id = int(input("Enter the course id:"))
        cursor.execute("select * from courses")
        courses = cursor.fetchall()
        if isPresent(course_id,courses):
            raise InvalidId("")
        department = Department_Choice()
        if department == None:
            raise InvalidChoice("")
        credits = int(input("Enter no of credits for the course(1/2/3/4/5/6):"))
        if credits<1 or credits>6:
            print("Chosen credits out of range!!!")
            raise InvalidChoice("")
        st = "Insert into courses values ({},{},'{}')".format(course_id,credits,department)
        cursor.execute(st)
    except ValueError:
        print("Invalid Entry!!!")
    except InvalidId:
        print("Id already exists!!!")
    except InvalidChoice:
        return

def enroll_students(cursor):
    while True:
        try:
            print("Choices: 1.To enroll ,0. To quit")
            choice = int(input("Enter the choice:"))
            clear_screen()
            if choice == 0:
                break
            elif choice == 1:
                try:
                    student_id = int(input("Enter the student_id:"))
                    cursor.execute('select * from students')
                    students = cursor.fetchall()
                    if not isPresent(student_id,students):
                        raise InvalidId("")
                    course_id = int(input("Enter the course_id:"))
                    cursor.execute('select * from courses')
                    courses = cursor.fetchall()
                    if not isPresent(course_id,courses):
                        raise InvalidId("")
                    grade = None
                    while True:
                        ch = input("Do you want to enter the grade(y/n):")
                        ch = ch.lower()
                        if ch=='y':
                            grade = grade_entry()
                            break
                        elif ch=='n':
                            break
                        else:
                            print("Enter the right choice!!!")
                    cursor.execute("select * from grades")
                    grades = cursor.fetchall()
                    for row in grades:
                        if row[0]==student_id and row[1]==course_id:
                            print("Record already exists!!!")
                            continue
                    st = ''
                    if grade != None:
                        st = "Insert into grades(student_id,course_id,grade) values ({},{},{})".format(student_id,course_id,grade)
                    else:
                        st = "Insert into grades(student_id,course_id) values ({},{})".format(student_id,course_id)
                    cursor.execute(st)


                except ValueError:
                    print("Invalid Id!!!")
                except InvalidId:
                    print("Id is not present!!!")
                
            else:
                raise InvalidChoice("")
        except ValueError:
            print("Invalid Choice!!!")
        except InvalidChoice:
            print("Invalid Choice!!!")


def view_student_info(cursor):
    cursor.execute("select * from students")
    print("Student_id\t\tName\t\tDepartment\t\tDate of Birth\t\tEmail")
    data = cursor.fetchall()
    for row in data:
        for item in row:
            print(item,end="\t\t")
        print()
    return

def record_grades(cursor):
    cursor.execute('select * from grades')
    grades = cursor.fetchall()
    for row in grades:
        student_id = row[0]
        cursor.execute('select * from students where student_id = {}'.format(student_id))
        stu_details = cursor.fetchone()
        course_id = row[1]
        cursor.execute('select * from courses where course_id = {}'.format(course_id))
        course_details = cursor.fetchone()
        print("Details of the student and course:")
        print("Student Id\t\tName\t\tDepartment\t\tCourse_Id\t\tCourse dept")
        print(stu_details[0],stu_details[1],stu_details[2],sep='\t\t',end='\t\t')
        print(course_details[0],course_details[1],sep='\t\t')
        if row[2] == None:
            grade = grade_entry()
            st = "Update grades set grade = {} where student_id = {} and course_id = {}".format(grade,row[0],row[1])
            cursor.execute(st)
        else:
            ch = 'n'
            while True:
                ch = input("Do you want to re-enter the grade of student(y/n)?")
                if ch == 'n':
                    break
                elif ch == 'y':
                    grade = grade_entry()
                    st = "Update grades set grade = {} where student_id = {} and course_id = {}".format(grade,row[0],row[1])
                    cursor.execute(st)
                    break
                else:
                    clear_screen()
                    print("Incorrect Choice!!!")
        
    return

def sort_by_first(element):
  return element[0]  # Access the first element

def generate_reports(cursor):
    cursor.execute('select students.student_id,name,students.department,grades.course_id,grade,credits from students,grades,courses where students.student_id = grades.student_id and grades.course_id = courses.course_id')
    data = cursor.fetchall()
    data = sorted(data,key=sort_by_first)
    print("Student_ID\t\tName\t\tDepartment\t\tCourse_Id\t\tGrade\t\tCredits")
    i = 0
    while i < len(data):
        student_id = data[i][0]
        total_points = 0.0
        total_validated_credits = 0

        while i < len(data) and student_id == data[i][0]:
            for item in data[i]:
                print(item,end='\t\t')
            print()
            if data[i][4] is not None:
                total_points += data[i][4]*data[i][5]
                total_validated_credits += data[i][5]
            i += 1

        if total_validated_credits!= 0:
            print('\nTotal CGPA(for validated subjects):{}\n\n'.format(total_points/total_validated_credits))

def print_choices():
        print("Choices:")
        print("0. Exit")
        print("1. Change name")
        print("2. Change department")
        print("3. Date of Birth")
        print("4. Email")


def update_details(cursor):
    try:
        student_id = int(input("Enter the student_id:"))
        cursor.execute('select * from students')
        students = cursor.fetchall()
        if not isPresent(student_id,students):
            raise InvalidId("")
        while True:
            try:
                print_choices()
                ch = int(input("Enter your choice:"))
                clear_screen()
                if ch==1 :
                    name = input("Enter the new name:")
                    st = "Update students set name = '{}' where student_id = {}".format(name,student_id)
                    cursor.execute(st)
                elif ch==2:
                    print("Enter the choice for new dept")
                    dept = Department_Choice()
                    st = "Update students set department = '{}' where student_id = {}".format(dept,student_id)
                    cursor.execute(st)
                elif ch==3:
                    try:
                        print("Enter new DoB")
                        year = int(input("Enter the year:"))
                        month = int(input("Enter the month:"))
                        day = int(input("Enter the date:"))
                        date = datetime.date(year,month,day)
                        st = "Update students set date_of_birth = '{}' where student_id = {}".format(date,student_id)
                        cursor.execute(st)
                    except ValueError:
                        print("Invalid Date Entry!!!")
                elif ch==4:
                    new_mail = input("Enter new mail id:")
                    if email_verification(new_mail) is not None:
                        st = "Update students set email = '{}' where student_id = {}".format(new_mail,student_id)
                        cursor.execute(st)
                    else:
                        print("Invalid mail id entered!!!")
                elif ch==0:
                    break
                else:
                    raise InvalidChoice("")           
            except ValueError:
                clear_screen()
                print("Invalid Choice!!!")
            except InvalidChoice:
                clear_screen()
                print("Invalid Choice!!!")  

            
    except ValueError:
        print("Invalid Id!!!")
    except InvalidId(""):
        print("Invalid Id!!!")


def delete_records(cursor):
    try:
        print("Do you want to delete (1.student or 2. Course)??")
        ch = int(input("Enter the choice:"))
        if ch==1:
            try:
                student_id = int(input("Enter the student id:"))
                st = 'delete from grades where student_id = {}'.format(student_id)
                cursor.execute(st)
                st = 'delete from students where student_id = {}'.format(student_id)
                print("Successfully deleted!!!")
            except ValueError:
                print("Invalid Student Id!!!")
        elif ch==2:
            try:
                course_id = int(input("Enter the course id:"))
                st = 'delete from grades where course_id = {}'.format(course_id)
                cursor.execute(st)
                st = 'delete from courses where course_id = {}'.format(course_id)
                print("Successfully deleted!!!")
            except ValueError:
                print("Invalid Course Id!!!")
        else:
            raise InvalidChoice("")
    except ValueError:
        print("Invalid Choice!!!")
    except InvalidChoice:
        print("Invalid Choice!!!")





def choiceMenu():
    print("0. Exit the program")
    print("1. Insert a new student")
    print("2. Enroll students into courses")
    print("3. Record Grades for students in enrolled courses")
    print("4. View Student Information")
    print("5. Generate Reports")
    print("6. Update Student Details")
    print("7. Delete records")
    print("8. Register courses")

def main():
    mycon = mysqLtor.connect(host="localhost",user='root',passwd="Dhanu123@")
    cursor = mycon.cursor()
    cursor.execute("show databases")
    databases = cursor.fetchall()
    if ('student_management_system',) not in databases:
        print(databases)
        cursor.execute("Create database student_management_system;")
    cursor.execute("use student_management_system")
    cursor.execute("show tables")
    tables = cursor.fetchall()
    if ('students',) not in tables:
        cursor.execute("""create table students (
                            student_id int Primary key,
                            name varchar(100),
                            department varchar(255),
                            date_of_birth Date,
                            email varchar(100))""")
    if ('courses',) not in tables:
        cursor.execute("""create table courses (
                            course_id int Primary key,
                            credits int not NULL,
                            department varchar(255))""")
    if ('grades',) not in tables:
        cursor.execute("""create table grades (
                            student_id int ,
                            foreign key(student_id) references students(student_id),
                            course_id int ,
                            foreign key(course_id) references courses(course_id),
                            grade smallint
                        )""")
    print("All tables are setup!!!")

    while True:
        try:
            choiceMenu()
            choice = int(input("Enter the choice:"))
            clear_screen()
            if choice==0:
                break
            elif choice==1:
                insert_new_record(cursor)
                mycon.commit()
            elif choice==2:
                enroll_students(cursor)
                mycon.commit()
            elif choice == 3:
                record_grades(cursor)
                mycon.commit()
            elif choice==4:
                view_student_info(cursor)
            elif choice==5:
                generate_reports(cursor)
            elif choice==6:
                update_details(cursor)
                mycon.commit()
            elif choice==7:
                delete_records(cursor)
                mycon.commit()
            elif choice==8:
                register_courses(cursor)
                mycon.commit()
            else:
                print("Invalid Choice Entered!!!")
        except ValueError:
            print("Incorrect Choice Entered!!!")

    cursor.close()
        
if __name__=="__main__":
    main()