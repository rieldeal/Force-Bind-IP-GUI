from os import system, startfile
from appJar import gui
import configparser

config = configparser.ConfigParser()
app = gui()

#function to open the program using ForceBindIP
def OPEN(self):
    
    forcebindIP = 'cd "' + config['DEFAULT'].get('location') + '" && forcebindip64.exe ' + config['DEFAULT'].get('IP') + ' '
    #checks which button you clicked, if other asks for location
    if self == 'Other':               
        file = app.openBox(title='Select program to start')
        ADD = app.yesNoBox('Save?', 'Add to config file?\nThis will reload the program.')
        #adds location of new program to config file, then opens a new instance of the this program, and closes the existing one
        if ADD:
            ButtonName = app.textBox('Button name', 'Enter the name for the new button:')
            
        if ADD and ButtonName != None:
            config[ButtonName] = {}
            config[ButtonName]['file'] = file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            startfile(__file__)
            app.stop()
        
        system(forcebindIP + file)
    else:
        system(forcebindIP + config[self].get('file'))

configExist = config.read('config.ini')

#checks if the config file exists, if not, prompts to build it
if configExist == []:
    app.errorBox('Error', 'Press OK to select location for ForceBindIP64.exe')

    FBLocation = app.directoryBox(title='Select location for ForceBindIP64.exe')
    IPAdd = app.textBox('IP Address', 'Enter the IP address for the connection you want to use:')
    config['DEFAULT'] = {}
    config['DEFAULT']['location'] = FBLocation
    config['DEFAULT']['IP'] = IPAdd
    with open('config.ini', 'w') as configfile:
            config.write(configfile)
    startfile(__file__)
    app.stop()
#builds the GUI
else:
    for section in config.sections():
        if section != 'DEFAULT':
            app.addButton(section, OPEN)

    app.addButton('Other', OPEN)
    
app.go()
