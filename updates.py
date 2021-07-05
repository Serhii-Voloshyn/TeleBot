
from bs4 import BeautifulSoup
import requests
import os, shutil


def find_borders(groups):

    indices = [i for i, x in enumerate(groups) if x['value'] == 'All']
    return indices[1] + 1, indices[2]

def find_borders_exam(groups):

    indices = [i for i, x in enumerate(groups) if x['value'] == 'All']
    return indices[1] + 1


def delete_files_in_folder(path):
    """
    Delete all files in path folder. Example: if path is C:\\file\\folder, files in folder will be deleted 
    Noted: Copied from stackoverflow
    """
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



def update_group_schedule(group):
    url = 'https://student.lpnu.ua/students_schedule?departmentparent_abbrname_selective=All&studygroup_abbrname_selective=' + \
        group + '&semestrduration=1'
    
    #Create file
    file = open('local\\schedule\\' + group + '.html', 'x', encoding = 'utf-8')

    with open('local\\schedule\\' + group + '.html', 'w', encoding = 'utf-8') as group_file:
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        schedule = soup.find_all('div', class_ = 'view-grouping')
        
        for i in schedule:
            group_file.write(str(i) + '\n')


def update_exam_schedule(group):
    
    url = 'https://student.lpnu.ua/students_exam?departmentparent_abbrname_selective=All&studygroup_abbrname_selective=' + group
    
    #Create file
    file = open('local\\exams\\' + group + '.html', 'x', encoding = 'utf-8')

    with open('local\\exams\\' + group + '.html', 'w', encoding = 'utf-8') as group_file:

        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        schedule = soup.find_all('div', class_ = 'view-content')
        
        for i in schedule:
            group_file.write(str(i) + '\n')

#Working with groups.html
def update_schedule_groups():
    """
    Write into file groups.html tags option from website.
    """
    soup = BeautifulSoup(requests.get('https://student.lpnu.ua/students_schedule').text, 'lxml')

    #Find all option tags in soup 
    groups = soup.find_all('option')
    start, end = find_borders(groups)
    groups = groups[start:end]

    #Delete first, if not - groups will be repeated in file
    with open('local\\groups.html', 'w', encoding='utf-8') as groups_file:
        groups_file.close()

    
    #Working with file
    #Write each group to file
    with open('local\\groups.html', 'w', encoding='utf-8') as groups_file:
        for group in groups:
            groups_file.write(str(group) + '\n')



def update_exam_groups():
    """
    Write into file groups_exam.html tags option from website.
    """
    soup = BeautifulSoup(requests.get('https://student.lpnu.ua/students_exam').text, 'lxml')

    #Find all option tags in soup 
    groups = soup.find_all('option')
    
    start = find_borders_exam(groups)
    groups = groups[start:]

    #Delete first, if not - groups will be repeated in file
    with open('local\\groups_exam.html', 'w', encoding='utf-8') as groups_file:
        groups_file.close()

    #Working with file
    #Write each group to file
    with open('local\\groups_exam.html', 'w', encoding='utf-8') as groups_file:
        for group in groups:
            groups_file.write(str(group) + '\n')



def update_schedule():
    
    path = 'local\\schedule'
    delete_files_in_folder(path)

    
    with open('local\\groups.html', 'r', encoding = 'utf-8') as groups_file:

        content = groups_file.read()
        soup = BeautifulSoup(content, 'lxml')

        groups = soup.find_all('option')

        for i in groups:
            update_group_schedule(i.text)
        


def update_exams():
    path = 'local\\exams'
    delete_files_in_folder(path)

    
    with open('local\\groups_exam.html', 'r', encoding = 'utf-8') as groups_file:

        content = groups_file.read()
        soup = BeautifulSoup(content, 'lxml')

        groups = soup.find_all('option')

        for i in groups:
            update_exam_schedule(i.text)


def main():

    #Delete folder local if exists. Needed to update local files easily
    if os.path.exists('local'):
        shutil.rmtree('local')

    #Create folder local and it's child folders schedule and exams
    os.mkdir('local')
    os.mkdir('local\\schedule')
    os.mkdir('local\\exams')

    #Needed updates: groups list for simple schedules and groups list for exams,
    #Update schedule for all groups in groups.html
    update_schedule_groups()
    update_exam_groups()

    #Update exam schedule for all groups from groups_exam.html
    update_schedule()
    update_exams()


if __name__ == '__main__':
    main()