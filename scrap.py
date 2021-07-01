from bs4 import BeautifulSoup
import requests

from updates import update_groups, update_schedule

def get_group_schedule_address(group):
    return 'https://student.lpnu.ua/students_schedule?departmentparent_abbrname_selective=All&studygroup_abbrname_selective=' + \
        group + '&semestrduration=1'

def connect_to_schedule():

    return requests.get('https://student.lpnu.ua/students_schedule').text
    
def is_valid_group(group):

    with open('groups.html', 'r', encoding = 'utf-8') as groups:
        content = groups.read()
        soup = BeautifulSoup(content, 'lxml')

        tag = soup.find('option', value = group)
        
        if(tag == None):
            return False
        else:
            return True

    return False

def main(group, sub_group, week_color):

    soup = BeautifulSoup(connect_to_schedule(), 'lxml')

    #update_groups(soup)

    if is_valid_group(group):
        
        soup = BeautifulSoup(requests.get(get_group_schedule_address(group)).text, 'lxml')

        schedule_class = "view view-students-schedule view-id-students_schedule view-display-id-new_students_schedule view-dom-id-e06f026ccca0e51e2cfd1a98f93530c1"

        schedule = soup.find_all('div', class_ = 'view-grouping')
        
        for i in schedule:
            pass
            #print(i.find('div', class_ = 'view-grouping-header').text)

    update_schedule()


    
    

    

    

    
main("СА-32", 1, 1)
