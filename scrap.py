from bs4 import BeautifulSoup
import requests

def get_group_schedule_address(group):
    """
    Get group like string (example CA-32), then return schedule web address for that group. 
    Schedule address of different groups has different group in web address like in return below.
    """
    return 'https://student.lpnu.ua/students_schedule?departmentparent_abbrname_selective=All&studygroup_abbrname_selective=' + \
        group + '&semestrduration=1'

def connect_to_schedule():
    """
    Return html of schedule page withut any group.
    Needed to take all possible groups.
    """
    return requests.get('https://student.lpnu.ua/students_schedule').text
    
def is_valid_group(group):
    """
    Return True, if group is in groups.html
    """

    #Take group list from local file. It's easier to save these groups as html, not list like
    with open('local\\groups.html', 'r', encoding = 'utf-8') as groups:
        content = groups.read()
        soup = BeautifulSoup(content, 'lxml')

        tag = soup.find('option', value = group)
        
        if(tag == None):
            return False
        else:
            return True

    #If impossible to open file
    return False

def main(group, sub_group, week_color):

    soup = BeautifulSoup(connect_to_schedule(), 'lxml')

    #update_groups(soup)

    if is_valid_group(group):
        
        soup = BeautifulSoup(requests.get(get_group_schedule_address(group)).text, 'lxml')
    

    

    

    
main("СА-32", 1, 1)
