from exam import Exam
from bs4 import BeautifulSoup

def list_to_exam(li):
    """Converts list to Exam object and returns it
    li - list of elements"""
    #If doesn't contain URL (location)
    if len(li) == 4:
        return Exam(li[0], li[1], li[2], li[3])
    #If contains URL
    else:
        return Exam(li[0], li[1], li[2], li[3], li[4])


def get_location_url(tag):
    """Returns list of utls in tag
    tag - soup. Div with class = view-grouping.
    """
    return tag.find('a', href = True)


def remove_garbage(exam):
    """Exam is a tag contains useless characters, function removes them and return updated list of string"""
    #Convert exam tag to list of strings
    result = (exam.get_text(';')).split(';')
    #Replace characters
    return [i.replace(',', '') for i in result]

def form_exam(soup):
    """Converts tag to exam"""
    date = soup.find('div', class_ = 'view-grouping-header').getText()
    num = soup.find('h3').getText()

    #Div 'class = group_content', which contains name, teacher (and location if exists)
    raw = remove_garbage(soup.find('div', class_ = 'group_content'))

    #Current exam
    current = [date, num] + raw

    if current.count('URL онлайн заняття') > 0:
        location = get_location_url(soup)
        current[current.index('URL онлайн заняття')] = location

    return list_to_exam(current)


def html_to_exams(soup):
    """Convert html from local file to list of ScheduleDay objects
    soup - soup, local\\schedule file content
    """
    tag = soup.find_all('div', class_ = 'view-grouping')
    return [form_exam(i) for i in tag if i]

def get_exams_by_group(group):
    """Finds schedule file, returns list of ScheduleDay objects
    group - string, name of group, encoding utf-8
    """
    with open('local\\exams\\' + group + '.html', 'r', encoding = 'utf-8') as file:
        content = file.read()
        #Get all file content (html tag)
        soup = BeautifulSoup(content, 'lxml')

        #Returns list of ScheduleDay objects
        return html_to_exams(soup)