import mysql.connector as mysql

#************************PART I ---CREATE TABLES, ADDING DATA, SETTING CONSTRAINTS**********************
mydb = mysql.connect(host="127.0.0.1",  user="root", passwd="123456")
print(mydb)
print("--------Start--------")
cursor = mydb.cursor()
cursor.execute("SHOW DATABASES")
print(cursor.fetchall())

# #Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS school_db")

#Use scholl_db database
cursor.execute("USE school_db")

# Delete tables
cursor.execute("DROP TABLE IF EXISTS student,subject,professor,course,grade")

# # Create Tables
cursor.execute("CREATE TABLE IF NOT EXISTS SUBJECT (subject_id VARCHAR(15) NOT NULL PRIMARY KEY, "
               "subject_name VARCHAR(25) NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT (student_id VARCHAR(15) NOT NULL PRIMARY KEY, "
               "account_name VARCHAR(15) NOT NULL UNIQUE,"
               "password VARCHAR(20) NOT NULL, f_name VARCHAR(20) NOT NULL, l_name VARCHAR(20) NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS PROFESSOR (professor_id VARCHAR(15) NOT NULL PRIMARY KEY, "
               "account_name VARCHAR(15) NOT NULL UNIQUE,"
               "password VARCHAR(20) NOT NULL, f_name VARCHAR(20) NOT NULL, l_name VARCHAR(20) NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS COURSE (course_id VARCHAR(15) NOT NULL PRIMARY KEY, professor_id VARCHAR(15), "
               "subject_id VARCHAR(15) NOT NULL, "
               "CONSTRAINT FK_professor FOREIGN KEY(professor_id) REFERENCES professor(professor_id), "
               "CONSTRAINT FK_subject FOREIGN KEY(subject_id) REFERENCES subject(subject_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS GRADE (course_id VARCHAR(15), student_id VARCHAR(15),grade INT(3) DEFAULT -1,"
               "PRIMARY KEY(course_id,student_id),"
               "CONSTRAINT CHK_grade CHECK (grade >= 0 && grade <=100),"
               "CONSTRAINT FK_class FOREIGN KEY(course_id) REFERENCES course(course_id),"
               "CONSTRAINT FK_student FOREIGN KEY(student_id) REFERENCES student(student_id))")

# Show tables
cursor.execute("SHOW TABLES")
print(cursor.fetchall())


cursor.execute("DELETE FROM student")
cursor.execute("DELETE FROM subject")
cursor.execute("DELETE FROM professor")
cursor.execute("DELETE FROM course")
cursor.execute("DELETE FROM grade")


# Show columns in student table
cursor.execute("DESC grade")
print(cursor.fetchall())



# Insert data to table subject
insertQuerySubject = "INSERT INTO SUBJECT(subject_id, subject_name) VALUES(%s,%s)"
subjectValues = [("CSD1233","Python Programming"),
                 ("CSD2214","Web Technology II")]
cursor.executemany(insertQuerySubject,subjectValues)
mydb.commit() #confirm to insert to mysql tables
print(cursor.rowcount, "records inserted")

# Insert data to table professor
insertQueryProfessor = "INSERT INTO PROFESSOR(professor_id, account_name, password, f_name, l_name) " \
                       "VALUES(%s,%s,%s,%s,%s)"
professorValues = [("P0123777","123777","abcdef","Mavel","Stefen"),
                   ("P0123888","123888","abcdef","Diana","Hoodward")]
cursor.executemany(insertQueryProfessor, professorValues)
mydb.commit() #confirm to insert to mysql tables
print(cursor.rowcount, "records inserted")

# Insert data to table student
insertQueryStudent = "INSERT INTO STUDENT(student_id, account_name, password, f_name, l_name) " \
                       "VALUES(%s,%s,%s,%s,%s)"
studentValues = [("S01238989","1238989","abcdef","Stepfano","Alexandra"),
                 ("S01233838","1233838","abcdef","Alisa","Lixus"),
                 ("S01237777","1237777","abcdef","Time","Normand")]
cursor.executemany(insertQueryStudent, studentValues)
mydb.commit()
print(cursor.rowcount, "records inserted")


# Insert data to table class
insertQueryCourse = "INSERT INTO COURSE(course_id, professor_id, subject_id) VALUES(%s,%s,%s)"
courseValues = [("CSD1233_4","P0123777","CSD1233"),
                ("CSD2214_5","P0123777","CSD2214"),
                ("CSD2214_7","P0123777","CSD2214")]
cursor.executemany(insertQueryCourse, courseValues)
mydb.commit()
print(cursor.rowcount, "records inserted")


#Insert data to table grade
insertQueryGrade = "INSERT INTO GRADE(course_id, student_id, grade) VALUES(%s,%s,%s)"
gradeValues = [("CSD1233_4","S01238989",89),
               ("CSD2214_5","S01238989",90),
               ("CSD1233_4","S01233838",98)]
cursor.executemany(insertQueryGrade,gradeValues)
mydb.commit()
print(cursor.rowcount, "records inserted")



#************************PART II ---FUNCTIONS TO WORK WITH INTERFACE**********************
class account:
    def __init__(self, id, fname, lname):
        self.__id = id
        self.__fname = fname
        self.__lname = lname

    def setId(self,id):
        self.__id = id

    def setFName(self,fname):
        self.__fname = fname

    def setLName(self,lname):
        self.__lname = lname

    def getId(self):
        return self.__id

    def getFName(self):
        return self.__fname

    def getLName(self):
        return  self.__lname

    def __str__(self):
        return "User_ID: "+self.getId()+"\nFirst Name: "+ self.getFName()+"\nLast Name: " + self.getLName()

    def gainDetail(self,type,name,password):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()
            try:
                q = ""
                if type == "Student":
                    q = "SELECT student_id,f_name,l_name FROM STUDENT WHERE account_name = %s AND password = %s"
                elif type == "Professor":
                    q = "SELECT professor_id,f_name,l_name FROM PROFESSOR WHERE account_name = %s AND password = %s"
                elif type == "Admin":
                    q = ""
                    if name == "root" and password == "123456": #for now, there is one 1 admin
                        self.setId("001")
                        self.setFName("Admin")
                        self.setLName("Admin")
                        return 1

                value = (name, password)
                try:
                    cursor.execute(q,value)
                    data = cursor.fetchone()
                    print(data) #for debugging
                    self.setId(data[0])
                    self.setFName(data[1])
                    self.setLName(data[2])
                    return 1
                except:#Data not found
                    return -3
            except: # failed to execute query
                return -2
        except: #Cant connect to database
            return -1


class Professor:
    @staticmethod
    def addGrade(professor_id,student_id,course_id,grade):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                check_q = "SELECT professor_id FROM COURSE WHERE course_id =%s"
                cursor.execute(check_q, (course_id,))
                check = cursor.fetchone()
                if check[0] != professor_id:
                    return -5  # professor doesnt have right to add grade for this course

                q = """INSERT INTO GRADE(course_id,student_id,grade) 
                VALUES(%s,%s,%s)"""
                cursor.execute(q, (course_id,student_id,grade))
                mydb.commit()
                print(cursor.rowcount, "records inserted")
                # print(grades)  # for debugging
                return 1 #Insert succeeded
            except:  # Failed to insert
                return -4
        except:  # Cant connect to database
            return -1

class Show:
    @staticmethod
    def grade(id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()
            try:
                q = """SELECT COURSE.course_id, SUBJECT.subject_name, GRADE.grade FROM COURSE 
                    INNER JOIN SUBJECT ON COURSE.subject_id = SUBJECT.subject_id
                    INNER JOIN GRADE ON COURSE.course_id = GRADE.course_id
                    WHERE GRADE.student_id = %s """
                cursor.execute(q, (id,))
                grades = cursor.fetchall()
                # print(grades)  # for debugging
                return grades
            except: # Data not found
                return -3
        except: #Cant connect to database
            return -1


class Login:
    @staticmethod
    def validate(type, name, password):
        result = 0
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()
            try:
                q = ""
                if type == "Student":
                    q = "SELECT account_name,password FROM STUDENT WHERE account_name = %s AND password = %s"
                elif type == "Professor":
                    q = "SELECT account_name,password FROM PROFESSOR WHERE account_name = %s AND password = %s"
                elif type == "Admin":
                    q = ""
                    if name == "root" and password == "123456": #for now, there is one 1 admin
                        return 1

                value = (name, password)
                try:
                    cursor.execute(q,value)
                    data = cursor.fetchone()
                    print(data) #for debugging
                    if data[0] == name and data[1] == password:
                        result = 1
                except:#Data not found
                    result = -3
            except: # failed to execute query
                result = -2
        except: #Cant connect to database
            result = -1
        return result

class Admin:
    @staticmethod
    def createAccount(user,password,fname,lname,type,id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                if type.lower() == "student":
                    q = """INSERT INTO STUDENT(student_id, account_name, password, f_name, l_name) 
                    VALUES(%s,%s,%s,%s,%s)"""
                elif type.lower() =="professor":
                    q = """INSERT INTO PROFESSOR(professor_id, account_name, password, f_name, l_name) 
                    VALUES(%s,%s,%s,%s,%s)"""
                cursor.execute(q, (id,user,password,fname,lname))
                mydb.commit()
                print(cursor.rowcount, "records inserted")
                return 1 # succeeded
            except:  # Failed to create
                return -4
        except:  # Cant connect to database
            return -1

    @staticmethod
    def deleteAccount(user, type, id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                if type.lower() == "student":
                    q = """DELETE FROM STUDENT WHERE student_id = %s && account_name = %s"""
                elif type.lower() == "professor":
                    q = """DELETE FROM PROFESSOR WHERE professor_id = %s && account_name = %s"""

                cursor.execute(q,(id,user,))
                mydb.commit()
                print(cursor.rowcount, "records deleted")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4 #failed
            except:  # query string problem
                return -2
        except:  # Cant connect to database
            return -1

    @staticmethod
    def updateAccount(user,password,fname,lname,type,id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                changes = ""
                values = []
                if user != "":
                    changes += "account_name = '%s',"
                    values.append(user)
                if password != "":
                    changes += "password = '%s',"
                    values.append(password)
                if fname != "":
                    changes += "f_name = '%s',"
                    values.append(fname)
                if lname != "":
                    changes += "l_name = '%s',"
                    values.append(lname)
                changes = changes.rstrip(',')
                changes = changes % (tuple(values))
                print(changes)

                if type.lower() == "student":
                    q = ("UPDATE STUDENT "
                         "SET %s "
                         "WHERE student_id = '%s'")
                    q = q % (changes, id)
                    # print(q)
                elif type.lower() =="professor":
                    q = ("UPDATE PROFESSOR "
                         "SET %s "
                         "WHERE professor_id = '%s'")
                    q = q % (changes, id)
                    # print(q)

                cursor.execute(q)
                mydb.commit()
                print(cursor.rowcount, "records updated")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4  # failed
            except Exception as e:  # query string problem
                print(e)
                return -2
        except:  # Cant connect to database
            return -1

    @staticmethod
    def createCourse(course_id,professor_id,subject_id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                q = """INSERT INTO COURSE(course_id, professor_id, subject_id) 
                        VALUES(%s,%s,%s)"""
                cursor.execute(q, (course_id,professor_id,subject_id))
                mydb.commit()
                print(cursor.rowcount, "records inserted")
                return 1  # succeeded
            except:  # Failed to create
                return -4
        except:  # Cant connect to database
            return -1

    @staticmethod
    def deleteCourse(course_id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                q = """DELETE FROM COURSE WHERE course_id = %s"""
                cursor.execute(q,(course_id,))
                mydb.commit()
                print(cursor.rowcount, "records deleted")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4 #failed
            except Exception as e:  # query string problem
                print(e)
                return -2
        except:  # Cant connect to database
            return -1

    @staticmethod
    def updateCourse(course_id,professor_id,subject_id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                changes = ""
                values = []
                if professor_id != "":
                    changes += "professor_id = '%s',"
                    values.append(professor_id)
                if subject_id != "":
                    changes += "subject_id = '%s',"
                    values.append(subject_id)

                changes = changes.rstrip(',')
                changes = changes % (tuple(values))
                print(changes)

                q = ("UPDATE COURSE "
                     "SET %s "
                     "WHERE course_id = '%s'")
                q = q % (changes, course_id)
                print(q)
                cursor.execute(q)
                mydb.commit()
                print(cursor.rowcount, "records updated")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4  # failed
            except Exception as e:  # query string problem
                print(e)
                return -2
        except:  # Cant connect to database
            return -1

    @staticmethod
    def createSubject(subject_id,subject_name):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                q = """INSERT INTO SUBJECT(subject_id, subject_name) 
                        VALUES(%s,%s)"""
                cursor.execute(q, (subject_id,subject_name))
                mydb.commit()
                print(cursor.rowcount, "records inserted")
                return 1  # succeeded
            except:  # Failed to create
                return -4
        except:  # Cant connect to database
            return -1

    @staticmethod
    def updateSubject(subject_id,subject_name):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                changes = ""
                values = []
                if subject_name != "":
                    changes += "subject_name = '%s'"
                    values.append(subject_name)

                changes = changes % (tuple(values))
                print(changes)

                q = ("UPDATE SUBJECT "
                     "SET %s "
                     "WHERE subject_id = '%s'")
                q = q % (changes, subject_id)
                print(q)
                cursor.execute(q)
                mydb.commit()
                print(cursor.rowcount, "records updated")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4  # failed
            except Exception as e:  # query string problem
                print(e)
                return -2
        except:  # Cant connect to database
            return -1

    @staticmethod
    def deleteSubject(subject_id):
        try:
            mydb = mysql.connect(host="127.0.0.1", user="root", passwd="123456", database="school_db")
            print(mydb)
            print("--------Start--------")
            cursor = mydb.cursor()

            try:
                q = """DELETE FROM SUBJECT WHERE subject_id = %s"""
                cursor.execute(q,(subject_id,))
                mydb.commit()
                print(cursor.rowcount, "records deleted")
                if cursor.rowcount == 1:
                    return 1  # succeeded
                elif cursor.rowcount == 0:
                    return -4 #failed
            except Exception as e:  # query string problem
                print(e)
                return -2
        except:  # Cant connect to database
            return -1



# print(Admin.updateSubject("CSD1233","Python I"))
# print(Admin.createSubject("CSD9999","Java EE"))
# print(Admin.deleteSubject("CSD9999"))
# print(Admin.updateCourse("CSD2214_5","P0123888","CSD2214"))
# print(Admin.deleteCourse("CSD2214_7"))
# print(Admin.createCourse("CSD2214_6","P0123888","CSD2214"))
# print(Admin.updateAccount("1233838","ABCDEF","Alisa","Lixus","Student","S01233838"))
# print(Admin.deleteAccount("1237777","Student","S01237777"))
# print((Admin.createAccount("1239999","abcdef","Phuong","Ly","Student","S01239999")))
# print(Professor.addGrade("P0123777","S01233838","CSD2214_5",88))
# print(Show.grade("S01238989"))
# print(Login.validate("Student","1238989", "abcdef"))



