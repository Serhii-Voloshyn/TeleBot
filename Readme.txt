--------Abstract
A schedule bot. He takes info from https://student.lpnu.ua/students_schedule (for schedule) 
and from https://student.lpnu.ua/students_exam (for exams)
User can see group schedule for each day and exams. User able to choose and change group

Notes:
Schedule - a simple student schedule for every day.
Exam(-s) - exam schedule.

--------Files
1. Local folder: contains exams and schedule folders, which contains html files of shedules. 
Each file is a div with class = view-content. Local folder is necessary, because web site usually is shutted down
groups_exam.html - contains all possible groups from exam web page
groups.html - contains all possible groups from schedule web page
Those files are different

2. Media folder: needed for future developmet, when bot can send stickers, images, video, a lot of messages.

3. bot.py: contains object Telebot and it's realization

4. config.py: contains TOKEN for bot

5. converter: contains function to convert tag to schedule and it's decomposition

6. exam_converter: contains function to convert tag to exams and it's decomposition

7. lesson.py: class Lesson

8. exam.py: class Exam

9. schedule_day: class ScheduleDay

10. updates.py: run this file to update local files. Updates all files and folders in local.