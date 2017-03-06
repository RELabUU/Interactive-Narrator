# Interactive Narrator
**Developed @ Utrecht University**

Visualize your user stories to improve understanding of the project, inspect system functionality 
and imporve communication among stakeholders.

This application uses the Visual Narrator (https://github.com/marcelrobeer/visualnarrator)to generate a conceptual model which is then
visualized using Vis.js and is presented to the user in the browser from where the visualization can be modified to cater to the 
user's needs.

**Dependencies**

The main dependency for the program is Visual Narrator (https://github.com/marcelrobeer/visualnarrator). 
To run the program, you need to install Visual Narrator in the same directory as the Interactive Narrator Project Folder (/inwebapp):
Other depencies can be found in requirements.txt

**Installation**

Currently, Interactive Narrator needs to be run from your local machine. The preferred method is to
create a virtual Python environment using virtualenv. Note that Interactive Narrator's python files
are configured to be used in a virtual environment because of the shebang #!/usr/bin/env python

In the virtual environment you have created you should have the following file/folder structure:

```
your_virtualenvironment
│____bin
│____lib  
|____include
│____share
└───inwebapp
│   │
│   └───app
│       │   app.py
│       │   example_stories.txt
│       │   form.py
|       |   ....
│   
└───VisualNarrator
    │   run.py
    │
```
Note that you should place the Visual Narrator folder in the same directory as your
Interactive Narrator (inwebapp) folder.

Change this line(21) in app.py:
sys.path.append('/home/gjslob/Documents/environments/inarrator/VisualNarrator')
to:
sys.path.append('/path/on/your/computer/yourvirtualenvironment/VisualNarrator')
To tell Python where to look for de VisualNarrator package on your computer.


**Running the Project**

Each time you run the project, change line 70:
data = run.program('CMSCompany.csv')
to contain the filename of your user story set located in the inwebapp folder

1. open a terminal in your virtual environment directory
2. activate your virtual environment with 'source bin/activate'
3. change directory to the inwebapp folder with 'cd inwebapp'
4. run app.py with 'python app.py'
5. open your webbrowser and browse to http://127.0.0.1:5000/form
6. add identifiers for your company, company id, sprint name and sprint number(id)
7. submit the data and wait for the visualization to appear
