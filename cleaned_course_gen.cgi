#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()

# Table Header indices
ACADEMIC_PERIOD = 0 #SKIP
SUBJECT = 1
COURSE_NUMBER = 2
SEQ_NUMBER = 3
CRN = 4
COURSE_TITLE = 5
MEET_DAYS = 6
CLASS_TIME = 7
BLDG_CODE = 8
ROOM_CODE = 9
INSTRUCTOR = 10
COURSE_ATTRIBUTES = 11

# Dictionary with the prefix of department as a key and the full name of department as values
department = {
    'AFR': 'Africana Studies',
    'ANT': 'Anthropology',
    'ARB': 'Arabic Studies',
    'ART': 'Art',
    'BIO': 'Biology',
    'CHE': 'Chemistry',
    'CHI': 'Chinese',
    'CLA': 'Classics',
    'COM': 'Communication Studies',
    'CSC': 'Computer Science',
    'DAN': 'Dance',
    'DIG': 'Digital Studies',
    'ECO': 'Economics',
    'ENG': 'English',
    'EDU': 'Educational Studies',
    'ECO': 'Economics',
    'ENV': 'Environmental Studies',
    'ETH': 'Ethics',
    'FMS': 'Film and Media Studies',
    'GSS': 'Gender and Sexuality Studies',
    'FRE': 'French Studies',
    'GER': 'German Studies',
    'GRE': 'Greek',
    'SPA': 'Hispanic Studies',
    'HIS': 'History',
    'HUM': 'Humanities',
    'LAT': 'Latin',
    'LAS': 'Latin American Studies',
    'MAT': 'Mathematics',
    'MHU': 'Medical Humanities',
    'MIL': 'Military Science',
    'MUS': 'Music',
    'PHI': 'Philosophy',
    'PHY': 'Physics',
    'POL': 'Politics',
    'PSY': 'Psychology',
    'REL': 'Religion',
    'RUS': 'Russian Studies',
    'SOC': 'Sociology',
    'THE': 'Theatre',
    'WRI': 'Writing 101'
    }  

# Dictionary of requirement acronym keys and requirement name values

requirement_names = {
    'HTRQ':'Historical Thought',
    'MQRQ':'Mathematical and Quantitative Thought', 
    'LTRQ':'Literary Studies, Creative Writing, and Rhetoric', 
    'NSRQ':'Natural Science', 
    'PRRQ':'Philosophical and Religious Perspectives',     
    'SSRQ':'Social-Scientific Thought', 
    'VPRQ':'Visual and Performing Arts', 
    'LBRQ':'Liberal Studies', 
    'CULT':'Cultural Diversity', 
    'COMP':'Composition',
    'NONE':'No Requirement Fulfilled'
    }
    





def read_csv(course_file, semester):
    """
    Reads in course_file (a .csv file) and makes a dictionary with the
    distirubtion/graduation requirements as keys and the courses
    that fulfill each requirment as a list for the values.
    
    Input: 
    course_file - a csv file of the courses for the current semester
    
    Return: 
    req_dict - a dictionary with requirements as keys and the courses
    that fulfill that requirement in a list as the value.
    """
    import csv
    
    courses = []
    
    if semester == "spring":
        path = "spring_schedule/"
    if semester == "fall":
        path = "fall_schedule/"
    
    with open(path + course_file, 'rU') as cf:
        cfReader = csv.reader(cf, quotechar = '"', delimiter = ',')
        header = True
        for line in cfReader:
            
            if header:
                header = False
                pass
            
            elif 'TBA ' not in line: 
                
                #Remove extra whitespace
                line[MEET_DAYS] = line[MEET_DAYS].replace(' ', '')
                line[CLASS_TIME] = line[CLASS_TIME].replace(' ', '')
                line[COURSE_ATTRIBUTES] = line[COURSE_ATTRIBUTES].replace(
                    '\r\n', '')   
                courses.append(line)
        
        # Call the make_requirement_dict method       
        req_dict = make_requirement_dict(courses)       
        return req_dict





def make_requirement_dict(courses):
    """
    Make a dictionary with requirements as keys and list of
    courses as values.
    
    Input:
    courses - a list of classes where each element is a list of
    the details of that class (course title, CRN, time, etc.).
    
    Return:
    req_dict - a dictionary with requirements as keys and the courses
    that fulfill that requirement in a list as the value.
    """
    
    req_dict = {'HTRQ':[], 'MQRQ':[], 'LTRQ':[], 'NSRQ':[], 'PRRQ':[], 
                'SSRQ':[], 'VPRQ':[], 'LBRQ':[], 'CULT':[], 'COMP':[], 'NONE':[]}
        
    for course in courses:
        course_reqs = course[COURSE_ATTRIBUTES]
        course_reqs = course_reqs.split(' ')
        
        for requirement in course_reqs:
            condition1 = len(requirement) != 0
            condition2 = requirement in req_dict.keys()
                        
            if condition1 and condition2:
                req_dict[requirement].append(course)
            
    return req_dict






def adjust_time(time):
    """
    Function adjusts a time to 24-hr for all times after 12PM and 
    returns the 24-hr time
    
    Input:
    time - A string that represents the time
    
    Return:
    A time in 24-hr format for a time between 8AM and 12PM
    """
    
    if (time >= '0800') and (time <= '1259'):
        return time
    else:
        return str(int(time[0:2]) + 12) + time[2::]



def check_time(early, late):
    
    if early > late:
        print '''
        <p>'Earliest' time is later than 'Latest' time, 
        please adjust the selected times. </p>
        <form action="http://mcs3.davidson.edu/coursepicker/coursefinder.html">
        <input type="submit" value="Go back"></form> 
        '''
    else:
        return True



def choices(course_dict, req, early, late, days):
    """
    Examines all of the available courses to determine which courses
    fit the user-selected parameters.
    
    Input: 
    course_dict - a dictionary with requirements as keys and the courses
    that fulfill that requirement in a list as the value.
    req - the list of requirements the user would like to fulfill.
    early - a string representing the earliest time the user would like
    to start class.
    late - a string representing the latest time the user would like to
    start class.
    days - a string representing the days of the week the user would
    like to have a class.
    
    Return:
    all_desired - a list of courses (a list) that fit all of the parameters.
    
    """
    all_desired = []
    desired_CRN = []
    desired_time= []
    
    # If user selects all courses within time frame
    if req == ['ALL']:
        req = ['HTRQ', 'MQRQ', 'LTRQ', 'NSRQ', 'PRRQ', 'SSRQ', 'VPRQ',
               'LBRQ', 'CULT', 'COMP', 'NONE']    
               
    # Go through one time to find the courses that work
    
    for single_req in req:              
        for course in course_dict[single_req]:
            time = adjust_time(str(course[CLASS_TIME][0:4]))
            cond_early = (time >= early)
            cond_late = (time <= late)
            cond_days = (course[MEET_DAYS] in days)
            cond_non_lab = (len(course[MEET_DAYS]) > 1)
            
            if single_req == 'NSRQ':
                if cond_early and cond_late and cond_days and cond_non_lab:
                    if course not in all_desired:
                        all_desired.append(course)                    
                        desired_CRN.append(course[CRN])
                        desired_time.append(time)                            
                   
            elif cond_early and cond_late and cond_days:
                if course not in all_desired:
                    all_desired.append(course)                    
                    desired_CRN.append(course[CRN])
                    desired_time.append(time)    
    
    # Lab        
    for single_req in req:
        for course in course_dict[single_req]:
            
            time_early = adjust_time(str(course[CLASS_TIME][0:4]))
            
            cond_CRN = course[CRN] in desired_CRN
            cond_not_desired = course not in all_desired
            
            if cond_CRN and cond_not_desired:
                all_desired.append(course)
                course[COURSE_TITLE] = course[COURSE_TITLE] + " LAB"
                
    all_desired.sort(key=lambda x: x[CRN]) 
    all_desired.sort(key=lambda x: x[COURSE_NUMBER]) 
    
    return all_desired




    

def sort(optimal):
    """
    Sorts the list of optimal classes by subject (BIO, ANT, etc.)
    
    Input:
    optimal - a list of courses (a list) that fit all of the parameters.
    
    Return: 
    results - a dictionary of the classes, with the subjects as the keys and
    a list of the classes as the values.
    """
    results = {}
    for course in optimal:
        if course[SUBJECT] not in results.keys():
            results[course[SUBJECT]] = []
        results[course[SUBJECT]].append(course)
        
    return results




def pretty_print(results):
    """
    Formats the acceptable classes into HTML tables by subject.
    
    Input:
    results - a dictionary of the classes, with the subjects as the keys and
    a list of the classes as the values.
    """
    
    for key in results:
        alternator = 0
        print ''' 
        <table border="3px black solid">                     
            <thead>
                <tr>
                <th>Subject</th>
                <th>Course</th>
                <th>Section</th>
                <th>CRN</th>
                <th>Title</th>
                <th>Days</th>
                <th>Time</th>
                <th>Building</th>
                <th>Room</th>
                <th>Professor</th>
                <th>Distribution</th>
                </tr>
            </thead>
            <tbody>
        '''
        for result in results[key]:
            
            if (alternator % 2) == 1:
                print '''
                <tr class="alt">
                '''
            if (alternator % 2) == 0:
                print '''
                <tr class="not">
                '''
            for output in result[1:]:
                print '''
                    <td>%s</td>
                    '''% (output)
            print '''
            </tr>
            '''
            alternator += 1
        print'''
        <h2>%s</h2>
        ''' %(department[key])        
            

    




def main():
    #!/usr/bin/python
    import os
    import cgi
    import cgitb
    cgitb.enable()
    
    print "Content-Type: text/html"
    print
    print '''
    <link type="text/css" rel="stylesheet" href="stylesheetCG.css" />
        <TITLE>Davidson Course Finder</TITLE>
        <H1>Course Finder</H1>
    '''
    form = cgi.FieldStorage()
    
    # Obtaining value from HTML
    req = form.getlist('req')
    days = form['days'].value
    early = form['early'].value
    late = form['late'].value
    semester = form['semester'].value

    
    
    if semester == "spring":
        course_file = os.listdir("spring_schedule")[0] 
    if semester == "fall":
        course_file = os.listdir("fall_schedule")[0] 
    course_dict = read_csv(course_file, semester)
        
    #if 'CULT' in req:
        #print '''
        #<h2> Cultural Diversity (Graduation Requirement) </h2>
        #'''          
    if 'COMP' in req:
        print '''
        <h2> Composition (Graduation Requirement) </h2>
        <p>Note: Composition requirement must be satisfied by the
        student before entering sophomore year. A student may 
        fulfill the requirement only by taking a course 
        designated as doing so. Such courses will be listed under 
        the writing program and numbered 101 - e.g., each 
        section, whatever the thematic topic, will be designated 
        WRI 101. </p>
        <p>The second semester (151W) in the humanities sequence 
        is an exception; the first two semesters, taken together, 
        also satisfy the composition requirement. With the 
        exception of the multi-semester humanities program, no 
        writing course fulfills any distribution requirement, 
        only the composition requirement.</p>
        '''  
                  
    early = adjust_time(early)
    late = adjust_time(late)
    
    if check_time(early, late):
        
        optimal_classes = choices(course_dict, req, early, late, days)
        
        if len(optimal_classes) == 0:
            print'''
             <h2>No classes found, please go back and try again.<h2>
             <form action="http://mcs3.davidson.edu/coursepicker/coursefinder.html"> 
             <input type="submit" value="Go back"></form> 
            '''
        else:
            print '''
            <form action="http://mcs3.davidson.edu/coursepicker/coursefinder.html"> 
            <input type="submit" value="Go back"></form> 
             '''
            sorted_classes = sort(optimal_classes)
            pretty_print(sorted_classes)
            
            
    
    
if __name__ == "__main__":
    main()