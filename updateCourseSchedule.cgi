#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()

# Required header that tells the browser how to render the text.
# First line, *first character*, must have header 
# "Content-Type: text/html" followed by blank line
print "Content-Type: text/html"
print

# You can copy and paste html code from Dreamweaver 
print '''
<link type="text/css" rel="stylesheet" href="stylesheetCG.css" />
    <TITLE>Update Davidson Course Schedule</TITLE>
    <H1 id="header">Update Course Schedule    <img class="resize" align="right" src="http://logonoid.com/images/davidson-college-logo.png"/></H1>
'''


try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

password = form.getvalue('password')

if password != 'bacteria':
    print '''
    <p>Incorrect password. Please try again.</p>
    <form class="nogrey" action="Login.html"> <input type="submit" value="Go back"></form> 
    <form class="nogrey" action="coursefinder.html"> <input type="submit" value="Go to Course Finder"></form>
    '''
    
    
fileitem = form['file']

# Change password: Replace the word in quotes on the next line
if password == 'bacteria':
    
    # Test if the file was uploaded
    if fileitem.filename:
    
        #delete the current inventory
        if form['Semester'].value == 'spring':
            path = 'spring_schedule'
        if form['Semester'].value == 'fall':
            path = 'fall_schedule'
            
        if len(os.listdir(path)) != 0:
            for file in os.listdir(path):
                old_schedule = file
                os.remove(path + '/' + file)
                
        # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        open(path + '/'  + fn, 'wb').write(fileitem.file.read())
        message = 'The old file was "' + old_schedule + '". The file "' + fn + '" was uploaded successfully.'
        
    else:
        message = 'No file was uploaded.'
        
   
    print '''
    <p>%s</p>
    ''' % (message)
    print '''
    <form class="nogrey" action="Login.html"> <input type="submit" value="Go back"></form> 
    <form class="nogrey" action="coursefinder.html"> <input type="submit" value="Go to Course Finder"></form>
    '''
    
