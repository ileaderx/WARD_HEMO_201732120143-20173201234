class Human:
    def human(self, name, age, birth, gender):
        self.name = name
        self.age = age
        self.birth = birth
        self.gender = gender

    class Student(Human):
        def information(self, name, age, StdId):
            self.name = "Ward"
            self.age = 20
            self.StdId = 201732120143

    class Faculity(Human):
        def info(self, name, age, honor):
            self.name = "Robert"
            self.age = 40
            self.honor = "C++ teacher"

        class Instructor(Faculity):
            def insinfo(self, name, date, birth, gender):
                self.name = "bithany"
                self.date = "2019/10/26"
                self.birth = "1995/30/6"
                self.gender = "Male"

    class Course:
        def courseinfo(self, number, name, level):
            self.number = "00256"
            self.name = "OOP"
            self.level = "Graduate"
        print(courseinfo)