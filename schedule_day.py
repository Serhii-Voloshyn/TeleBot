class ScheduleDay:


    def __init__(self, day_name, lessons):

        self.day_name = day_name
        self.lessons = lessons


    def __str__(self):
        result = '=========================\n'
        result += self.day_name + '\n'

        if isinstance(self.lessons, list):
            for i in self.lessons:
                result += '-------------\n'
                result += str(i)
        else:
            result += str(self.lessons)

        result += '========================='
        return result

    def get_day_name(self):
        return self.day_name