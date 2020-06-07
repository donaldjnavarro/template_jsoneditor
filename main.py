import cmd
import json
from datetime import datetime

class prompt(cmd.Cmd):
    """Global prompt. This class creates the default prompt interface. All menus should inherit this class"""
    # Methods in this class should never return True. In this root prompt that would be the equivalent of restarting the app
    prompt = "\n: "
    def cmdloop(self, intro=None):
        """aka the PREpreloop"""
        return cmd.Cmd.cmdloop(self, intro)

    def preloop(self):
        """When first arriving at this this class, or any inheriting class"""

    def do_quit(self, arg):
        """Close the program"""
        quit()
    
    def emptyline(self):
        # return cmd.Cmd.emptyline(self) # this will repeat the last entered command
        return False

    def precmd(self, line):
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        return cmd.Cmd.postcmd(self, stop, line)

    def do_save(self, arg):
        """Save current changes to a JSON file in the output/ folder"""
        # Identify save location for jsonWip
        if arg:
            filename = arg
        else:
            filename = "untitled-"+datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = "output/"+filename+".json"

        # Save jsonWip as JSON file
        json_output = open(filename, "w")
        json.dump(jsonWip, json_output, indent = 6) 
        json_output.close()
        print("jsonWip saved to",filename)

    def do_load(self, arg):
        """Load a JSON from the input/ folder for editing."""
        global jsonWip
        jsonWip = {} # Purge jsonWip before loading the new one
        filename = arg
        if not arg:
            print("You need to specify a filename of which JSON file in the input folder you want to load.")
            return False
        try:
            filename = "input/"+arg+".json"
            with open(filename) as json_file:
                jsonWip = json.load(json_file)
            printDict(jsonWip)
        except:
            print(filename)
            print("No such file found in the /input folder, or invalid JSON format.")
            print("Please specify a valid filename. Do not include the .json extension.")
            return False

    def do_clear(self, arg):
        """End the current jsonWip and restart from scratch."""
        print("You purge your current work, and save nothing further.")
        return True

    def do_look(self, arg):
        global here
        printHere()
        if not arg:
            # Display the full JSON currently in progress
            if not here:
                printDict(jsonWip)
            else:
                printDict(locationValue(jsonWip, here))

    def do_go(self, arg):
        """Navigate into one of the keys in the current level you are viewing of the JSON"""
        global here
        here.append(arg)
        print("Moving to "+locationString(here))
        printDict(locationValue(jsonWip, here))
        
    def do_back(self, arg):
        """Go back one level from your current location"""
        global here
        here.pop()
        print("Back to "+locationString(here))
        printDict(locationValue(jsonWip, here))

def printDict(toPrint):
    """Print a dictionary with indents"""
    if type(toPrint) == dict:
        print(json.dumps(toPrint, indent=4))
    else:
        print(toPrint)

def printHere():
    """Print the current active location within the jsonWip"""
    global here, jsonWip
    if not here:
        # Top level
        print("Currently viewing the top of JSON")
    else:
        print("Currently viewing "+locationString(here))

def locationValue(dataDict, location):    
    """Return a dictionary call based on provided location[]"""
    for k in location: dataDict = dataDict[k]
    return dataDict

def locationString(location):
    """return a stringified version of the location[] that maps a place within the dictionary"""
    return ".".join(location)

if __name__ == '__main__':
    existance = True
    while existance == True:
        jsonWip = {} # A dictionary to collect everything that is created
        here = [] # Track how deep into the json we move by maintaining a list of keys
        print("Current JSON:")
        printDict(jsonWip)
        print("Use load to start editing a local JSON file.")
        prompt().cmdloop()
