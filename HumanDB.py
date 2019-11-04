class Human:
    def human(self, name, age, birth, gender):
        pass
        self.name = name
        self.age = age
        self.birth = birth
        self.gender = gender

    class Student:
        pass
        def information(self, name, age, StdId):
            self.name = "Ward"
            self.age = 20
            self.StdId = 201732120143

    class Faculity:
        def info(self, name, age, honor):
            self.name = "Robert"
            self.age = 40
            self.honor = "C++ teacher"

        class Instructor():
            pass
            def insinfo(self, name, date, birth, gender):
                self.name = "bithany"
                self.date = "2019/10/26"
                self.birth = "1995/30/6"
                self.gender = "Male"

class Course:
        pass
        def courseinfo(self, number, name, level):
            self.number = "00256"
            self.name = "OOP"
            self.level = "Graduate"


import MySQLdb

db = MySQLdb.connect("localhost","root","","human")

c = db.cursor()

#c.execute("""CREATE TABLE IF NOT EXISTS Instructor(Id INT PRIMARY KEY, Name CHAR, Title TEXT, Sex TEXT, Country TEXT, Level TEXT, Born_in TEXT)""")

insertQuery = 'INSERT INTO Courses (221,intro to computer, undergraduate, None, spring2018, 20-211) VALUES (%s, %s, %s, %s, %s, %s)'
insertQuery = 'INSERT INTO Courses (2314,intro to OOP, undergraduate, everything is  obj, fall2018, 25-213) VALUES (%s, %s, %s, %s, %s, %s)'

insertQuery = 'INSERT INTO student (kim,201732120143, 23, M, Graduate) VALUES (%s, %s, %s, %s, %s)'
insertQuery = 'INSERT INTO Courses (20160002, Kaiya, 20, F, Undergraduate) VALUES (%s, %s, %s, %s, %s)'
insertQuery = 'INSERT INTO Courses (20160002, Wang, 19, M, Undergraduate) VALUES (%s, %s, %s, %s, %s)'

insertQuery = 'INSERT INTO Instructor(2017123, Phillips, NA, M, Canada, Master, Phillips was born in London, UK)'

print (c.execute("""SHOW DATABASES"""))
db.close()