#InsaniText

This is a text editor I am making for fun, and partly to get better at writing code in Python and Qt.

I am not sure yet what kind of functionality the editor will get over time. At the moment I am using it mainly as my main text editor, which effectively replaced gedit on ubuntu and notepad on windows. 

It is (at this point in time) not meant to be a replacement for my IDEs that I am using when writing code. Though I might try to give it a shot to make this a customized-to-me IDE. 

This text editor might have some quirks, but it is not aimed at a general audience. If you happen to like parts of this editor however, you are free to clone the source code and alter it further to suit your needs. 


## TODO
These features I do want to add to this editor at some point in time, in no particular order:

* Syntax highlighting 
* Preferences menu (adjustable backgroud, font, etc..)
* Menubar options (save, save as, open..)
* Add InsaniText to the open-with options under windows

## Typing measurement
While you are typing in the editor, it will calculate an average WPM and CPM. This average is calculated based on the characters that you are typing, but it is only looking at [0-9] and [aA-zZ]. Spacebar presses are also included. 

## Getting started
In order to run this program, you will need to have Python 3 installed. I have tested this on a windows and a ubuntu installation of Python 3. This also means that if you are running this on a mac, it is not tested and I can not guarantee that everything is working as inteded due to difference in the operating systems. 

Apart from python you will also need to have PyQt installed, which is used for the GUI of this project. To install PyQt, the easiest way is by using pip. `pip install PyQt5`

After installing this, you can just run `python editor.py` to launch the editor.