# Interactive Narrator
**Developed @ Utrecht University**

**IMPORTANT: This project is not maintained nor functional at the moment. If you are interested in maintaining it, please contact Fabiano Dalpiaz at f.dalpiaz@uu.nl**

Visualize your user stories to improve understanding of the project, inspect system functionality 
and improve communication among stakeholders.

This application uses the Visual Narrator (https://github.com/marcelrobeer/visualnarrator) to generate a conceptual model which is then
visualized using Vis.js and is presented to the user in the browser from where the visualization can be adapted to cater to the 
user's needs.

![alt tag](https://github.com/Gionimo/InteractiveNarrator/blob/master/Screenshot%20Interactive%20Narrator2.png)


**License**

This product is free to use for commercial and non-commercial purposes.

**How To Start Developing**
1. create a ubuntu virtual machine
open a terminal in /Documents and run:
2. apt install python-pip
3. apt-get install python3-dev
4. apt install virtualenv
5. virtualenv -p python3 inarrator (this will create a separate dev. environment with the name inarrator)
6. in the newly created directory open a terminal and activate 
the virtual enironment with `source bin/activate` (do this everytime you need to install/update something)
7. pip install git
8. pip install -r requirements.txt (this will install all the required packages)
9. python -m spacy download en_core_web_md (download the spacy NLP language model)
 

**Telling Python interpreter where to look for packages**
Open a Linux terminal and navigate to your root directory with `~` and then type `sudo nano .profile`
which should open a file with some lines after which you add to the bottom of this file:

`export PYTHONPATH=$PYTHONPATH:/home/path/on/your/computer/yourvirtualenvironment/:/home/path/on/your/computer/yourvirtualenvironment/VisualNarrator`

If after this Python throws import errors it might not be able to find the packages.
A workaround is to add this line after line 22 in app.py and after line 6 in post.py:
   
   `sys.path.append('/path/on/your/computer/yourvirtualenvironment/VisualNarrator')`
   
   **and**
   
Add after line 6 in app.py:
 
   `# sys.path.append('/home/path/on/your/computer/inarrator')`
    
To tell Python where to look for de VisualNarrator package on your computer.

Notes:
- the project has been prepared for using Flask-Security but isn doing so yet. This is why
some commented code is present.
- message flashing is not working, although some code to start working with it is present
- deleting per sprint is ready to be implemented (see method in app.py) but needs looking into as currently 
deleting entities from one sprint also deletes them while they are actually in other sprints too.
solution: only delete entity (concept) when it is in a use story that is in only one sprints
- downloading the PNG of the network now gives a transparent image. This should be reworked to contain a white 
background. Some experimental code exists in visualization.js
- various print statements exist to help logging during development

TO DO LIST:
- improve rendering performance on mobile devices (change settings for algorithm)
- add clustering (method already in place)
- increase security for users (flask_security module already in place but not in use)
- enable delete per sprint (code already present, just needs tweaking. see app.py delete_sprint())
- add progress bar and hide rendering of the visualization until it's done
- add ceiling AND bottom to the weight filter
- add support for themes and epics
- improve support for touch events
- add more succes confirmations
- add a tutorial
- enable drawing on the visualization on touch devices
- enable downloading of the reports VN generates.
- add detection mechanism for redundencies/inconsistencies/dependencies such as color alerts
