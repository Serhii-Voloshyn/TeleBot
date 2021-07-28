from lesson import Lesson
from schedule_day import ScheduleDay
from bs4 import BeautifulSoup

#Needed to make flatten list of lesson settings
from collections.abc import Iterable



def replace_urls(current, urls, url_counter):
    """Replace element in current by <a></a> tag, needed to send schedule as message. 
    Returns tuple of updated list and unpdated counter
    current - list of strings
    urls - list of <a> tags
    url_counter - integer, needed to count through urls"""
    result = current
    updated_counter = url_counter
    #Through all urls. Even if there is only 1
    for n, i in enumerate(result):
        
        if i == 'URL онлайн заняття':
            result[n] = urls[updated_counter]
            updated_counter += 1

    return result, updated_counter


def remove_garabage_lessons(lessons):
    """Remove specific characters from strings
    lessons - list of strings
    """
    result = (lessons.get_text(';')).split(';')
    #Scraped lessons have strange characters, which must be deleted
    result = [i.replace('\xa0', '') for i in result]
    result = [i.replace(',', '') for i in result]
    return result

def flatten(lis):
    """Make nested list into 1-d list
    lis - list needed to flatten
    """
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
            yield item


def get_aviable_day(tag):
    """Get name day of current tag class = view-grouping, returns string"""
    return tag.find('div', class_ = 'view-grouping-header').getText()


def get_lessons_urls(tag):
    """Returns list of utls in tag
    tag - soup. Div with class = view-grouping.
    """
    return [a for a in tag.find_all('a', href = True)]


def get_lessons_numbers(tag):
    """Find and return list of lesson numbers. Multiple numbers = there are several lesson settings 
    (First and second group have that lesson, but have different location etc.)
    tag - soup. Div with class = view-grouping.
    """
    lessons_numbers = [i.getText() for i in tag.find_all('h3')]
    lessons_counter = [len(i.findChildren('div', recursive = False)) for i in tag.find_all('div', class_ = 'stud_schedule')]

    lessons_numbers = list(''.join([i * j for i, j in zip(lessons_numbers, lessons_counter)]))

    #print([i for i in tag.find_all('h3') for _ in tag.find_all('div', class_ = 'stud_schedule')])
    return lessons_numbers


def get_lessons_settings(tag):
    """Forms lesson settings using dict below
    tag - Div with class = view-grouping.
    """
    translated = {'group_full': 'Для всіх', 
                    'group_chys': 'Чисельник', 
                    'group_znam': 'Знаменник', 
                    'sub_1_full': 'І підгрупа',
                    'sub_2_full': 'ІІ підгрупа',
                    'sub_1_chys': 'І підгрупа, чисельник',
                    'sub_1_znam': 'І підгрупа, знаменник',
                    'sub_2_chys': 'ІІ підгрупа, чисельник',
                    'sub_2_znam': 'ІІ підгрупа, знаменник'}

    #Create list of settings, settings is 'id' of div, which is chield of div with class = stud_schedule
    #Create list of children, if have multiple children(findChildren returned a list) create list os settings
    #else create setting
    settings = [[j.get('id') for j in i.findChildren('div', recursive = False)] 
                if isinstance(i.findChildren('div', recursive = False), list)
                else (i.findChildren('div', recursive = False)).get('id') 
                for i in tag.find_all('div', class_ = 'stud_schedule')]

    #Make list 1-d
    settings = list(flatten(settings))

    #Translate settings using dict above
    settings = [translated[i] for i in settings]

    return settings



def list_to_lesson(data):
    """Convert list to Lesson object
    data - list of elements, each element is each attribute of Lesson
    """
    #If there is only 4 (5 or 6) given lesson attributes
    if len(data) == 5:
        return Lesson(data[0], data[1], data[2], data[3], data[4])
    elif len(data) == 6:
        return Lesson(data[0], data[1], data[2], data[3], data[4], data[5])
    else:
        return Lesson(data[0], data[1], data[2], data[3], data[4], [data[5], data[6]])



def form_lessons(tag):
    """Forms lesson for printing
    tag - soup, with div class = view-grouping
    """
    #Needed to itarate through urls. Not all lessons have URL, or have multiple
    url_counter = 0

    #Form urls which are in tag
    urls = get_lessons_urls(tag)
    #Because lesson number is ouside of tag, that contains all lessons in specific day
    lessons_num = get_lessons_numbers(tag)
    lessons_settings = get_lessons_settings(tag)

    #lessons is a list of Lesson objects
    lessons = []

    #Itarate through all lessons in tag and lesson_num

    for i, j, k in zip(tag.find_all('div', class_ = 'group_content'), lessons_num, lessons_settings):
            #Current lesson in list from, which is forming
            current = remove_garabage_lessons(i)

            lesson_settings = k
            #Lesson number insert first
            current.insert(0, lesson_settings)
            current.insert(0, j)

            #If contain URL
            if current.count('URL онлайн заняття') > 0:
                #Replace 'URL онлайн заняття' to <a></a> tag. Because telebot can print it easily
                #And increment url_counter
                current, url_counter = replace_urls(current, urls, url_counter)

            lessons.append(list_to_lesson(current))

    return lessons


def form_day(tag):
    """Creates ScheduleDay object by tag
    tag - soup, div class = view-grouping
    """
    return ScheduleDay(get_aviable_day(tag), form_lessons(tag))


def html_to_ScheduleDays(soup):
    """Convert html from local file to list of ScheduleDay objects
    soup - soup, local\\schedule file content 
    """
    tag = soup.find_all('div', class_ = 'view-grouping')
    return [form_day(i) for i in tag]


def get_ScheduleDays_by_group(group):
    """Finds schedule file, returns list of ScheduleDay objects
    group - string, name of group, encoding utf-8
    """
    with open('local\\schedule\\' + group + '.html', 'r', encoding = 'utf-8') as file:
        
        content = file.read()
        #Get all file content (html tag)
        soup = BeautifulSoup(content, 'lxml')

        #Returns list of ScheduleDay objects
        return html_to_ScheduleDays(soup)