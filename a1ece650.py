import sys
import re
import matplotlib.pyplot as plt

PROMPT="$ "
DEBUG=0
PLOT=1
CATCH_ALL=0

def printError(msg, out=sys.stdout):
    out.write("Error: {}\n".format(msg))

def invalidInput(out=sys.stdout):
    printError("Invalid Input", out)

def debugPrint(msg):
    if DEBUG == 1:
        print("Debug: {}".format(msg))


class invalidInputException(Exception):
    pass

class intersectException(Exception):
    pass

class duplicateException(Exception):
    pass

class nonExistException(Exception):
    pass


def checkIntersect(p1, p2, q1, q2):
    #todo input error check

    debugPrint("Check intersect")
    debugPrint("Line1: ({:.2f},{:.2f}) <-> ({:.2f},{:.2f})".format(p1.x, p1.y, p2.x, p2.y))
    debugPrint("Line2: ({:.2f},{:.2f}) <-> ({:.2f},{:.2f})".format(q1.x, q1.y, q2.x, q2.y))


    # Create a representation of the line
    # Paramaterize line 1 as:
    # (1-n)p1 + n*p2 = (x,y)
    # Paramaterize line 2 as:
    # (1-m)q1 + m*q2 = (x,y)

    # Equate the lines
    # (1-n)p1 + n*p2 = (1-m)q1 + m*q2
    # Rearage
    # (p2-p1)*n + (q1-q2)*m = q1 - p1
    # a*n + b*m = c
    a = [0] * 2
    a[0] = p2.x - p1.x
    a[1] = p2.y - p1.y

    b = [0] * 2
    b[0] = q1.x - q2.x
    b[1] = q1.y - q2.y
    
    c = [0] * 2
    c[0] = q1.x - p1.x
    c[1] = q1.y - p1.y

    # Check if lines are parallel
    # If the determinate on the 2x2 matrix is 0, they are parallel
    det = a[0]*b[1] - b[0]*a[1]

    # parallel line
    if det == 0:
        debugPrint("Parallel")
        # check if they are the same line
        # Check if q1 in p1 and p2
        s = [-1]*2
        if abs(p2.x - p1.x) > 0.0001:
            s[0] = (q1.x - p1.x) / (p2.x-p1.x)
        # elif abs(q1.x - p1.x) < 0.0001:
        #     s[0] = 0.5 # For verticl case, set s[0] somewhere valid

        if abs(p2.y - p1.y) > 0.0001:
            s[1] = (q1.y - p1.y) / (p2.y-p1.y)
        # elif abs(q1.y - p1.y) < 0.0001:
        #     s[1] = 0.5 # For verticl case, set s[0] somewhere valid

        if abs(p2.x - p1.x) < 0.0001 and abs(q1.x - p1.x) < 0.0001:
            # vertical Line
            s[0] = s[1]
        elif abs(p2.y - p1.y) < 0.0001 and abs(q1.y - p1.y) < 0.0001:
            # horizontal Line
            s[1] = s[0]

        debugPrint("Q1 s0 {:.3f} s1 {:.3f}".format(s[0], s[1]))
        if abs(s[0] - s[1]) < 0.0001 and s[0] > -0.0001 and s[0] < 1.0001 and s[1] > -0.0001 and s[1] < 1.0001:
            debugPrint("q1 in between")
            return True, vertex(vertex.V_INTERSECT, q1.x, q1.y)

        # Check if q2 in p1 and p2
        s = [-1]*2
        if abs(p2.x - p1.x) > 0.0001:
            s[0] = (q2.x - p1.x) / (p2.x-p1.x)
        # elif abs(q2.x - p1.x) < 0.0001:
        #     s[0] = 0.5 # For verticl case, set s[0] somewhere valid

        if abs(p2.y - p1.y) > 0.0001:
            s[1] = (q2.y - p1.y) / (p2.y-p1.y)
        # elif abs(q2.y - p1.y) < 0.0001:
        #     s[1] = 0.5 # For horizontal case, set s[0] somewhere valid

        if abs(p2.x - p1.x) < 0.0001 and abs(q2.x - p1.x) < 0.0001:
            # vertical Line
            s[0] = s[1]
        elif abs(p2.y - p1.y) < 0.0001 and abs(q2.y - p1.y) < 0.0001:
            # horizontal Line
            s[1] = s[0]

        

        debugPrint("Q2 s0 {:.3f} s1 {:.3f}".format(s[0], s[1]))
        if abs(s[0] - s[1]) < 0.0001 and s[0] > -0.0001 and s[0] < 1.0001 and s[1] > -0.0001 and s[1] < 1.0001:
            debugPrint("q2 in between")
            return True, vertex(vertex.V_INTERSECT, q2.x, q2.y)

        return False, vertex(vertex.V_INTERSECT, float('inf'), float('inf'))

    # Invert and evaluate the 2x2 matrix
    n = (b[1]*c[0] - b[0]*c[1]) / det
    m = (-1*a[1]*c[0] + a[0]*c[1]) / det

    # Check bounds
    if m > -0.0001 and m < 1.0001 and n > -0.0001 and n < 1.0001:
        x = (1-n)*p1.x + n*p2.x
        y = (1-n)*p1.y + n*p2.y
        return True, vertex(vertex.V_INTERSECT, x, y)

    return False, vertex(vertex.V_INTERSECT, float('inf'), float('inf'))

class vertex:
    V_NODE = 0
    V_INTERSECT = 1
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    def compareVertex(self, otherVertex):
        if abs(self.x - otherVertex.x) < 0.0001 and abs(self.y - otherVertex.y) < 0.0001:
            return True
        return False

class edge:
    def __init__(self, v1, v2, streetName):
        self.v1 = v1
        self.v2 = v2
        self.streetName = streetName

class street:
    def __init__(self, name):
        self.name = name
        self.vertexList = []
        self.edgeList = []

    def printStreet(self):
        debugPrint("Name: {}".format(self.name))
        for i, v in enumerate(self.vertexList):
            debugPrint("{}: ({:.2f},{:.2f})".format(i, v.x, v.y))

        for i, e in enumerate(self.edgeList):
            debugPrint("{}: <{},{}>".format(i, e.v1, e.v2))

    def addVertex(self, newVertex):
        # Add the new vertex to the list
        # TODO check if its not the same as the last vertex
        # Maybe dont bother as streets dont intersect themselves?
        # Or maybe check that as an error condition?
        self.vertexList.append(newVertex)
        # Add the edge
        numVertex = len(self.vertexList)
        if numVertex > 1:
            self.edgeList.append(edge(numVertex-2, numVertex-1, self.name))
            q1 = self.vertexList[numVertex-2]
            q2 = self.vertexList[numVertex-1]
            # Make sure it doesnt intersect with the same street
            for i in xrange(0, len(self.edgeList)-2):
                p1 = self.vertexList[self.edgeList[i].v1]
                p2 = self.vertexList[self.edgeList[i].v2]
                intersect, interVertex = checkIntersect(p1,p2,q1,q2)
                if intersect:
                    raise intersectException



class graph:
    def __init__(self):
        self.vertexList = []
        self.edgeList = []

    def addVertex(self, newVertex):
        debugPrint("Add vertex ({:2f},{:2f})".format(newVertex.x, newVertex.y))
        for i, oldVertex in enumerate(self.vertexList):
            if newVertex.compareVertex(oldVertex):
                # Node already in graph. No need to add
                # Promote to intersection
                oldVertex.type = vertex.V_INTERSECT
                debugPrint("FoundIndex {}".format(i))
                return i
        # Did not find the vertex, append to list
        self.vertexList.append(newVertex)
        debugPrint("newIndex {}".format(len(self.vertexList) -1))
        return len(self.vertexList) -1

    def addEdge(self, v1Index, v2Index, streetName):
        # create a list of edges that have already been checked to avoid repeating
        # since an edge can only intersect once
        #checkedList = [0] * len(self.edgeList)
        #for i, existingEdge in enumerate(self.edgeList):
        
        self.__addEgde_r(v1Index, v2Index, streetName, 0, len(self.edgeList)-1)

    def __addEgde_r(self, v1Index, v2Index, streetName, startIndex, endIndex):
        debugPrint("Add Edge: v1: {} v2: {} s: {} e: {}".format(v1Index, v2Index, startIndex, endIndex))

        if v1Index == v2Index:
            debugPrint("Zero length edge")
            return

        # if len(self.edgeList) != 0 and startIndex > endIndex:
        #     debugPrint("End of search")
        #     return

        # Check if it already exists
        for e in self.edgeList:
            if (v1Index == e.v1 and v2Index == e.v2) or (v1Index == e.v2 and v2Index == e.v1):
                #Already in set skip
                return

        
        #edgesToAdd = []
        #for i, existingEdge in enumerate(self.edgeList):
        #    if not checkedList[i]:
        for i in xrange(startIndex,endIndex+1):
            # street cant intersect itself
            if streetName != self.edgeList[i].streetName:
                p1 = self.vertexList[self.edgeList[i].v1]
                p2 = self.vertexList[self.edgeList[i].v2]
                q1 = self.vertexList[v1Index]
                q2 = self.vertexList[v2Index]
                intersect, interVertex = checkIntersect(p1,p2,q1,q2)
                if intersect:
                    debugPrint("Intersect")
                    # They intersected so add the new intersection (or promote to intersection)
                    vInterIndex = self.addVertex(interVertex)
                    # First split the existign edge into 2 new edges (if applicable)
                    if vInterIndex != self.edgeList[i].v1 and vInterIndex != self.edgeList[i].v2:
                        # Add new edge, and adjust the old one
                        temp = self.edgeList[i].v2
                        self.edgeList.append(edge(vInterIndex, self.edgeList[i].v2, self.edgeList[i].streetName))
                        self.edgeList[i].v2 = vInterIndex
                        debugPrint("--->Add split edge {} {}".format(vInterIndex, temp))
                        debugPrint("--->Shrunk edge {} {} was {} {}".format(self.edgeList[i].v1, vInterIndex, self.edgeList[i].v1, temp))
                        
                    
                    if vInterIndex != v1Index and vInterIndex != v2Index:
                        # if its not at the end of the segment
                        # break up the segment to be added separately
                        # Return after this point because the the sub edges take care of adding it
                        debugPrint("Recursive call {} {} and {} {}".format(v1Index, vInterIndex, vInterIndex, v2Index))
                        self.__addEgde_r(v1Index, vInterIndex, streetName, i+1, endIndex)
                        self.__addEgde_r(vInterIndex, v2Index, streetName, i+1, endIndex)
                        return

        # There were no intersections, so add the edge as-is
        self.edgeList.append(edge(v1Index, v2Index, streetName))
        debugPrint("--->Added non-intersect edge {} {}".format(v1Index, v2Index))

    def pruneGraph(self):
        # Prune the unwanted edges (edges that dont go to an intersection)
        end = len(self.edgeList)
        for i in xrange(end-1, -1, -1):
            if self.vertexList[self.edgeList[i].v1].type != vertex.V_INTERSECT and self.vertexList[self.edgeList[i].v2].type != vertex.V_INTERSECT:
                debugPrint("Delete edge: {}".format(i))
                del self.edgeList[i]

        # Prun any standed vertex
        end = len(self.vertexList)
        for i in xrange(end-1, -1, -1):
            found = False
            for j in xrange(0, len(self.edgeList)):
                if self.edgeList[j].v1 == i or self.edgeList[j].v2 == i:
                    found = True
                    break

            if not found:
                debugPrint("Delete vertex {}".format(i))
                del self.vertexList[i]
                for j in xrange(0, len(self.edgeList)):
                    if self.edgeList[j].v1 > i:
                        self.edgeList[j].v1 = self.edgeList[j].v1 - 1
                    if self.edgeList[j].v2 > i:
                        self.edgeList[j].v2 = self.edgeList[j].v2 - 1
    
    def printGraph(self, out=sys.stdout):
        out.write("V = {\n")
        for i, v in enumerate(self.vertexList):
            out.write("  {}: ({:.2f},{:.2f})\n".format(i, v.x,v.y))
        out.write("}\n")

        out.write("E = {\n")
        for i, e in enumerate(self.edgeList):
            out.write("  <{},{}>\n".format(e.v1,e.v2))
        out.write("}\n")

    def plotGraph(self):
        if PLOT == 1:
            plt.figure()
            xN = []
            yN = []
            xI = []
            yI = []
            for i, v in enumerate(self.vertexList):
                plt.annotate("v{}".format(i), (v.x, v.y))
                if v.type == vertex.V_NODE:
                    xN.append(v.x)
                    yN.append(v.y)
                elif v.type == vertex.V_INTERSECT:
                    xI.append(v.x)
                    yI.append(v.y)
            plt.plot(xN,yN,marker='o', linestyle = 'None', markersize=12)
            plt.plot(xI,yI,marker='*', linestyle = 'None', markersize=12)

            for i, e in enumerate(self.edgeList):
                x = []
                x.append(self.vertexList[e.v1].x)
                x.append(self.vertexList[e.v2].x)

                y = []
                y.append(self.vertexList[e.v1].y)
                y.append(self.vertexList[e.v2].y)
                plt.plot(x,y)

                xMid = sum(x)/len(x)
                yMid = sum(y)/len(y)
                plt.annotate("e{}".format(i), (xMid, yMid))


class streetDataBase:
    def __init__(self):
        self.streetDB = {}
        self.g = graph()

    def addStreet(self, newStreet):
        if self.checkStreetExists(newStreet.name):
            raise duplicateException
        self.streetDB[newStreet.name] = newStreet

    def removeStreet(self, streetName):
        if not self.checkStreetExists(streetName):
            raise nonExistException
        del self.streetDB[streetName]

    def replaceStreet(self, newStreet):
        self.removeStreet(newStreet.name)
        self.addStreet(newStreet)

    def checkStreetExists(self, streetName):
        return (streetName in self.streetDB)

    def plotStreets(self):
        if PLOT == 1:
            plt.figure()
            for streetName in self.streetDB:
                street = self.streetDB[streetName]
                x = [v.x for v in street.vertexList]
                y = [v.y for v in street.vertexList]
                plt.plot(x,y,marker='o')

    def generateGraph(self):
        self.g = graph()
        for streetName, newStreet in self.streetDB.items():
            debugPrint("***** Add street: {} *****".format(streetName))
            # Add the first vertex
            # v1Index = self.g.addVertex(newStreet.vertexList[newStreet.edgeList[0].v1])
            # for streetEdge in newStreet.edgeList:
            #     v2Index = self.g.addVertex(newStreet.vertexList[streetEdge.v2])
            #     self.g.addEdge(v1Index,v2Index)
            #     v1Index = v2Index
            
            v1Index = self.g.addVertex(newStreet.vertexList[0])
            for v in newStreet.vertexList[1:]:
                v2Index = self.g.addVertex(v)
                self.g.addEdge(v1Index, v2Index, streetName)
                v1Index = v2Index

        self.g.pruneGraph()


def parseStreetText(line, out=sys.stdout, errOut=sys.stderr):

    r = re.compile(r'^\s+"[a-zA-Z\s]+"\s+(\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)){2,}$')
    match = r.findall(line)
    #match = r.search(line)
    #if match == 'None':
    if len(match) != 1:
        raise invalidInputException("Did not match input")

    r = re.compile(r'"[a-zA-Z\s]+"')
    name = r.findall(line)[0]

    newStreet = street(name)

    r = re.compile(r'\(\s*-?\d+\s*,\s*-?\d+\s*\)')
    bracketGroups = r.findall(line)
    for b in bracketGroups:
        #b = b[1:-1]
        # b.replace(" ", "")
        #b = re.sub("\s", "", b) #Remove all white space
        pattern = re.compile(r'\s|\(|\)') #Remove all white space and brackets
        b = re.sub(pattern, '', b)
        nums = b.split(',')
        x = float(nums[0])
        y = float(nums[1])
        newStreet.addVertex(vertex(vertex.V_NODE, x, y))

    return newStreet

def tryToCreateStreet(line, out=sys.stdout, errOut=sys.stderr):

    try:
        newStreet = parseStreetText(line)
    except invalidInputException:
        invalidInput(errOut)
        return None
    except intersectException:
        printError("Streets Cannot Self Intersect", errOut)
        return None
    except duplicateException:
        printError("Street Names Must be Unique", errOut)
        return None
    except Exception as e:
        debugPrint(e)
        invalidInput(errOut)
        if not CATCH_ALL:
            raise e
        return None

    newStreet.printStreet()
    return newStreet

def parseAddCommand(streetDB, line, out=sys.stdout, errOut=sys.stderr):
    debugPrint("Add a street")

    newStreet = tryToCreateStreet(line[1:], out, errOut)
    if newStreet == None:
        return

    newStreet.printStreet()
    try:
        streetDB.addStreet(newStreet)
    except duplicateException:
        printError("Street Names Must be Unique", errOut)
        return
    except Exception as e:
        debugPrint(e)
        invalidInput(errOut)
        if not CATCH_ALL:
            raise e
        return
    


def parseChangeCommand(streetDB, line, out=sys.stdout, errOut=sys.stderr):
    debugPrint("change a specification")
    newStreet = tryToCreateStreet(line[1:], out, errOut)
    if newStreet == None:
        return

    try:
        streetDB.replaceStreet(newStreet)
    except nonExistException:
        printError("Street Does not Exist", errOut)
        return
    except Exception as e:
        debugPrint(e)
        invalidInput(errOut)
        if not CATCH_ALL:
            raise e
        return

def parseRemoveCommand(streetDB, line, out=sys.stdout, errOut=sys.stderr):
    debugPrint("remove a street")

    try:
        r = re.compile(r'^\s*r\s+"[a-zA-Z\s]+"\s*$')
        match = r.findall(line)
        if len(match) != 1:
            raise invalidInputException("Did not match input")
        
        r = re.compile(r'"[a-zA-Z\s]+"')
        streetName = r.findall(line)[0]
        streetDB.removeStreet(streetName)

    except invalidInputException:
        invalidInput(errOut)
        return
    except nonExistException:
        printError("Street Does not Exist", errOut)
        return
    except Exception as e:
        debugPrint(e)
        invalidInput(errOut)
        if not CATCH_ALL:
            raise e
        return
    

def parseGraphCommand(streetDB, line, out=sys.stdout, errOut=sys.stderr):
    debugPrint("output graph")

    streetDB.generateGraph()
    streetDB.g.printGraph(out)

    streetDB.plotStreets()
    streetDB.g.plotGraph()
    plt.show()


def main():

    streetDB = streetDataBase()

    while True:
        sys.stdout.write(PROMPT)
        line = sys.stdin.readline()

        if line == '':
            break

        line = line.strip()
        cmd = line[0]
        if cmd == 'a':
            # Add street
            parseAddCommand(streetDB, line)

        elif cmd == 'c':
            # change specification
            parseChangeCommand(streetDB, line)
        elif cmd == 'r':
            # remove street
            parseRemoveCommand(streetDB, line)
        elif cmd == 'g':
            # output graph
            parseGraphCommand(streetDB, line)
        else:
            printError("Unknown command")

    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
