class Lesson:

    def __init__(self, num, settings, name, teacher, type = None, location = None):
        """num - int like, lesson number in schedule
            name - string, lesson name
            teacher - string, teacher
            type - string, lesson type (Labratory, Practice, Lecture etc)
            location - string, lesson location. Could be room or URL. If URL, then it could be a list of URLs. 
            URLS form is html <a></a> tag

            Some lessons don't have location, or contain it in teacher field, same for type. Because of NULP schedule web site
        """
        self.num = num
        self.name = name
        self.teacher = teacher
        self.type = type
        self.location = location
        self.settings = settings

    def __str__(self):
        """Overloading for easy printing. Print all attributes separated by \\n
        """
        #Required fields
        result = "Харки: " + self.settings + '\n'
        result += "№ " + str(self.num) + '\n'
        result += "Назва предмету: " + self.name + '\n'
        result += "Викладач: " + self.teacher + '\n'

        if self.type != None:
            result += "Тип: " + self.type + '\n'

        #If location isn't in teacher field
        if self.location != None:

            #If location contain list of URLS. For NULP sake, that's why
            if isinstance(self.location, list):
                #Add all urls as html <a></a>
                for i in self.location:
                    result += str(i) + '\n'
            else:
                #If contain one URL
                result += str(self.location) + '\n'

        return result