COMP30005 - Web Information Technologies
========================================

Ganttly - a simple project management webapplication written in Python, using the Django framework.

Requirements
------------
  - Apache HTTP Server v2/2.2 - http://httpd.apache.org/
  - Python 2.7 or above - http://python.org
  - MySQL or SQLite - http://mysql.com or http://sqlite.org
  - mod_xsendfile - https://tn123.org/mod_xsendfile/
                  - http://github.com/nmaier/mod_xsendfile

All of the above (with the exception of mod_xsendfile) are included as part of the BitNami Django development stack - http://bitnami.com/stack/django

The installation instructions below are for those users who will deploy using the BitNami stack, although if you're clever enough to install the above tools manually, you're probably clever enough to install Ganttly without much instruction :)

Installation
------------
  - Install the BitNami Django stack.
  - Extract Ganttly to your BitNami projects folder.
  - Edit _COMP30005/COMP30005/settings.py_ and replace all instances of _"C:/Users/Brendan/BitNami DjangoStack projects"_ with the path to your BitNami projects folder.
  - Edit _COMP3005/COMP30005/wsgi.py_ and replace all instances of _"C:/Users/Brendan/BitNami DjangoStack projects"_ with the path to your BitNami projects folder.
  - From the _'BitNami DjangoStack'_ start menu folder, run _'Use BitNami DjangoStack'_.
  - Navigate to your BitNami projects folder.
  - Run (without quotes) _'python manage.py syncdb'_ and follow the instructions to create the Ganttly database.
  - Close the command line window.
  - From the mod_xsendfile zip file, extract mod_xsendfile.so to the Apache modules directory (the default location is _drive:/bitnami/djangostack-x.x.x-x/apache2/modules_).
  - Edit the _apache2/conf/http.conf_ file and add the following
  
    1) Under the other _'LoadModule'_ statements, add:

          LoadModule xsendfile_module modules/mod_xsendfile.so

    2) Change the _DocumentRoot_ to (replace the {...} with the actual path!):
    
          DocumentRoot "{Path to BitNami projects folder}/COMP30005"
      
    3) Change _\<Directory "xxxx"\>_ to (replace the {...} with the actual path!):
    
          <Directory "{Path to BitNami projects folder}/COMP30005">
          
    4) Find the _\<IfModule alias\_module\>_ line. In that block, add:
    
          Alias /static/ "{Path to BitNami projects folder}/COMP30005/ganttly/static/"
          
    5) Add the very end of the file, add the following:
    
          XSendFilePath "{Path to BitNami projects folder}/COMP30005/ganttly/uploads/"
          XSendFile on

          LoadModule wsgi_module modules/mod_wsgi/mod_wsgi.so
          WSGIPythonHome "{Path to BitNami Python folder}"
          WSGIScriptAlias / "{Path to BitNami projects folder}/COMP30005/COMP30005/wsgi.py"
          
  - Run Apache. In a browser, navigate to to _http://localhost/ganttly_.
