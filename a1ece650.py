import sys
import re
import matplotlib.pyplot as plt

PROMPT="$ "
DEBUG=1

def printError(msg):
    print("Error: {}".format(msg))

def debugPrint(msg):
    if DEBUG == 1:
        print("Debug: {}".format(msg))

class street:
    def __init__(self, name):
        self.name = name
        self.intersections = []

    def printStreet(self):
        debugPrint("Name: {}".format(self.name))
        for i, vertex in enumerate(self.intersections):
            debugPrint("{}: {}".format(i, vertex))

class streetDataBase:
    def __init__(self):
        self.streetDB = {}

    def addStreet(self, newStreet):
        self.streetDB[newStreet.name] = newStreet

    def removeStreet(self, newStreet):
        del self.streetDB[newStreet.name]

    def checkStreetExists(self, newStreet):
        return (newStreet.name in self.streetDB)

    def plotStreets(self):
        plt.figure(1)
        for streetName in self.streetDB:
            street = self.streetDB[streetName]
            x = [val[0] for val in street.intersections]
            y = [val[1] for val in street.intersections]
            plt.plot(x,y,marker='o')    #for()
        plt.show()


def parseStreetText(line):

    r = re.compile(r'("[a-zA-Z\s]+")')
    name = r.findall(line)[0]

    newStreet = street(name)

    r = re.compile(r'(\(-?\w*,-?\w*\))')
    bracketGroups = r.findall(line)
    for b in bracketGroups:
        b = b[1:-1]
        b.replace(" ", "")
        pattern = re.compile(r'\s|\(|\)')
        b = re.sub(pattern, '', b)
        nums = b.split(',')
        x = float(nums[0])
        y = float(nums[1])
        newStreet.intersections.append([x,y])

    return newStreet

def parseAddCommand(line):
    debugPrint("Add a street")
    try:
        newStreet = parseStreetText(line)
    except Exception as e:
        debugPrint(e)
        printError("Invalid Input")
        return

    newStreet.printStreet()
    streetDB.addStreet(newStreet)


def parseChangeCommand(line):
    debugPrint("change a specification")
    try:
        newStreet = parseStreetText(line)
    except Exception as e:
        debugPrint(e)
        printError("Invalid Input")
        return

    newStreet.printStreet()

def parseRemoveCommand(line):
    debugPrint("remove a street")

def parseGraphCommand(line):
    debugPrint("output graph")
    streetDB.plotStreets()

streetDB = streetDataBase()

def main():

    while True:
        sys.stdout.write(PROMPT)
        line = sys.stdin.readline()
        if line == '':
            continue

        cmd = line[0]
        if cmd == 'a':
            # Add street
            parseAddCommand(line)

        elif cmd == 'c':
            # change specification
            parseChangeCommand(line)
        elif cmd == 'r':
            # remove street
            parseRemoveCommand(line)
        elif cmd == 'g':
            # output graph
            parseGraphCommand(line)
        else:
            printError("Unknown command")

    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
