class Exam:

    def __init__(self, date, num, name, teacher, location = None):
        """Constructor
        date - string, example: 2016-08-08
        num - string, exam number
        name - string, exam name
        teacher - string, teacher name
        location - bs4 tag, contains URL tag, some exams don't have it"""
        self.date = date
        self.num = num
        self.name = name
        self.teacher = teacher
        self.location = location

    def __str__(self):
        """Overloading for easy printing. Print all attributes separated by \\n
        """
        #Required fields
        result = 'Дата: ' + self.date + '\n'
        result += "Пара № " + self.num + '\n'
        
        result += "Назва предмету: " + self.name + '\n'
        result += "Викладач: " + self.teacher + '\n'

        #If location isn't in teacher field
        if self.location != None:
            result += str(self.location) + '\n'

        return result