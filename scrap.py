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
    
