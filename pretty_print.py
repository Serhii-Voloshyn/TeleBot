from bs4 import BeautifulSoup
from lesson import Lesson


def get_lesson_settings(tag):
    
    settings = [i.get('id') for i in tag.find_all('div', class_ = 'week_color')]
    print('=======')
    print(settings)
    print('=======')

    return 'FULL'

def list_to_lesson(data):
    """Convert list to Lesson object
    data - list of values
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
    tag - Tag, from schedule site
    """
    #Form urls which are in tag
    urls = [a for a in tag.find_all('a', href = True)]
    #Needed to itarate through urls. Not all lessons have URL
    url_counter = 0

    #Because lesson number is ouside of tag, that contains all lessons in specific day
    lessons_num = [i.getText() for i in tag.find_all('h3')]
    #lessons is a list of Lesson objects
    lessons = []

    #Itarate through all lessons in tag and lesson_num
    for i, j in zip(tag.find_all('div', class_ = 'group_content'), lessons_num):
            
            #Current lesson in list from, which is forming
            current = (pretty_lessons((i.get_text(';')).split(';')))

            lesson_settings = get_lesson_settings(tag)

            #Lesson number insert first
            current.insert(0, lesson_settings)
            current.insert(0, j)

            #If contain URL
            if current.count('URL онлайн заняття') > 0:
                #Through all urls. Even if there is only 1
                for n, i in enumerate(current):
                    
                    if i == 'URL онлайн заняття':
                        
                        #Replace 'URL онлайн заняття' to <a></a> tag. Because telebot can print it easily
                        current[n] = urls[url_counter]
                        url_counter += 1
            lessons.append(list_to_lesson(current))

    return lessons


def pretty_lessons(lessons):
    """Remove specific characters from strings
    """
    #Because I won't return input parameters
    result = lessons

    #Scraped lessons have strange characters, which must be deleted
    result = [i.replace('\xa0', '') for i in result]
    result = [i.replace(',', '') for i in result]

    return result


def pretty_schedule_day(tag):

    days = [tag.find('div', class_ = 'view-grouping-header').getText()]

    result = ''

    for k in days:

        result = '=========================\n'
        result += k + '\n'

        for i in form_lessons(tag):
            result += '-------------\n'
            result += str(i) + '\n'
            
        result += '========================='
        
    return result

def pretty_schedule_week(soup):
    
    tag = soup.find_all('div', class_ = 'view-grouping')
    return [pretty_schedule_day(i) for i in tag if i]

def pretty_schedule_for_group(group):

    with open('local\\schedule\\' + group + '.html', 'r', encoding = 'utf-8') as file:
        
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')

        return pretty_schedule_week(soup)

pretty_schedule_for_group('СА-32')