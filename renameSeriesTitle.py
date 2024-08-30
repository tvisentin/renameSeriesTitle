import sys, re, os, shutil, subprocess
from pathlib import Path

pathToMove = ["/Users/Transmetropolitan/Movies/Thomas/", "/Users/Transmetropolitan/Movies/Lilly/"]
ignore = ["Neatsubs", "Capcom", "Fansub", "Definitelynotme", "Godotaku", "Despair", "Paradise", "Nofun", "Marvels", "Tyrannosaure", "Episode", "Dcs"] # Add more subteam here
extension = ["mp4", "mkv", "avi", "ass"]
toExcept = ["911"]
toRemove = ["Shin Sekai", "StreamAnime", "Final Series", "Sekai Raws", "2nd", "Fan-Kai"]
toLower = []
renameAndSend = False
yesAll = False
noAll = False
new = []
prev = []
pattern = re.compile("([s|S]?\d+)?([e|E]|Ep|X)?\d+$")
for arg in sys.argv[1:]:
    prev.append(arg)
    toSave = ""
    for remove in toRemove:
        arg = arg.replace(remove, "")
    if arg[0] == '[':
        delete = arg.find(']')
        arg = arg[delete+2:]
    elif arg[0] == '(':
        delete = arg.find(')')
        arg = arg[delete+2:]
    if arg.find('/'):
        delete = arg.rfind('/')
        arg = arg[delete+1:]
    ex = arg.rfind(".")
    if arg[ex + 1:] not in extension:
        prev.pop()
        continue
    else:
        arg = list(filter(None, arg.lower().title().replace('.', ' ').replace('_', ' ').replace('-', ' ').split(' ')))
        if arg[0] == '9' and arg[1] == '1' and arg[2] == '1':
            del arg[2]
            del arg[1]
            del arg[0]
            arg.insert(0, "911")
        if arg[0] == 'Room' and arg[1] == '104':
            del arg[1]
            del arg[0]
            arg.insert(0, "Room 104")
        if arg[0] == 'Station' and arg[1] == '19':
            del arg[1]
            del arg[0]
            arg.insert(0, "Station 19")
        if arg[1] == 'Iii':
            del arg[1]
            arg.insert(1, "III")
        for idx, string in enumerate(arg):
            if (idx != 0) and ((len(string) <= 2) or (string in toLower)):
                string = string.lower()
            match = pattern.match(string)
            if (string in ignore) or (string.isdigit() and int(string) > 1900 and int(string) < 2100):
                continue
            elif string in toExcept and (string == arg[0] or string == arg[1] or string == arg[2]):
                toSave += string + ' '
            elif match and string != arg[0]:
                string.upper()
                toSave += "- " + string + "." + arg[-1].lower()
                break
            elif string == arg[-1]:
                toSave += "." + arg[-1].lower()
                break
            else:
                toSave += string + ' '
        new.append(toSave)

if not new:
    print ("Nothing to change.")
    exit(1)
if len(new) > 1:
    print("----- All files -----")
    for string in new:
        if string.find('.') == -1 :
            string = string[0:len(string) - 5] + "." + string[len(string) - 4:].lower()
        print (string)
    print("----- --------- -----")
print ("If you want to change type [y]/[n]/[Y] (Y/N will change every file): ")
i = 0
while i < len(new):
    if new[i].find('.') == -1 :
        new[i] = new[i][:len(new[i]) - 5] + "." + new[i][len(new[i]) - 4:].lower()
    print ("Prev: " + (prev[i]))
    print ("New : " + (new[i]))
    if yesAll != True and noAll != True:
        char = input("$> ")
    if char == 'Y' or char == '1':
        if char == '1':
            renameAndSend = True
        yesAll = True
        os.rename(prev[i], new[i])
        print ("Files are changed")
    elif char == 'y':
        os.rename(prev[i], new[i])
        if yesAll != True:
            print ("File is changed")
    elif char == 'N':
        noAll = True
        print ("Files aren't changed")
        exit(1)
    else:
        del new[i]
        del prev[i]
        i -= 1
        print ("File isn't changed")
    i += 1

if len(pathToMove) == 0 or len(new) == 0:
    print ("This is the end ! :)")
    exit(1)
print ("Where do you want to move your files ?")
print ("0 -> Don't move")
for idx, folder in enumerate(pathToMove, start=1):
    print (str(idx) + " -> " + folder)
print ("Take the number corresponding to the right folder.")
if renameAndSend == True:
    idx = 1
else:
    idx = input("$> ")
if renameAndSend == True or (idx.isdigit() and int(idx) <= int(len(pathToMove)) and int(idx) > 0):
    for toMove in new:
        myFile = Path(toMove)
        if myFile.is_file():
            shutil.move(toMove, pathToMove[int(idx) - 1] + toMove)
    if len(new) == 1:
        print ("File is moved ! :)")
    else:
        print ("Files are moved ! :)")
else:
    if len(new) == 1:
        print ("File remain ! :)")
    else:
        print ("Files remain ! :)")
if renameAndSend == True:
    subprocess.Popen(["open", pathToMove[0]])
    subprocess.call(['osascript', '-e', 'tell application "iTerm" to quit'])
