import unittest
from a1ece650 import *
from StringIO import StringIO

ERROR_INVALID = 'Error: Invalid Input\n'
ERROR_SELF_INTERSECT = 'Error: Streets Cannot Self Intersect\n'
NON_EXIST_ERROR = 'Error: Street Does not Exist\n'
DUPLICATE_ERROR = 'Error: Street Names Must be Unique\n'
COMMAND_ACCEPTED = ''

NULL_GRAPH = "V = {\n\
}\n\
E = {\n\
}"


ASSIGN_EX_1 = "V = {\n\
1: (2,2)\n\
2: (4,2)\n\
3: (4,4)\n\
4: (5,5)\n\
5: (1,4)\n\
6: (4,7)\n\
7: (5,6)\n\
8: (5,8)\n\
9: (3,8)\n\
10: (4,8)\n\
}\n\
E = {\n\
<1,3>,\n\
<2,3>,\n\
<3,4>,\n\
<3,6>,\n\
<7,6>,\n\
<6,5>,\n\
<9,6>,\n\
<6,8>,\n\
<6,10>\n\
}"

ASSIGN_EX_2 = "V = {\n\
2: (4,2)\n\
5: (1,4)\n\
6: (4,7)\n\
8: (5,8)\n\
10: (4,8)\n\
}\n\
E = {\n\
<2,6>,\n\
<6,5>,\n\
<6,8>,\n\
<6,10>\n\
}"

def createGraphFromStr(gStr):
    g = graph()
    vertexNames = {}

    groups = re.split('}|{',gStr)
    vertexLines = groups[1].split('\n')[1:-1]
    # print(vertexLines)

    for i, line in enumerate(vertexLines):
        v, point = line.split(':')
        v = v.strip()

        r = re.compile(r'\s|\(|\)') #Remove all white space and brackets
        b = r.sub('',point)

        nums = b.split(',')
        x = float(nums[0])
        y = float(nums[1])
        vertexNames[v] = i
        g.vertexList.append(vertex(vertex.V_NODE, x, y))

    edgeLines = groups[3].split('\n')[1:-1]
    for line in edgeLines:
        r = re.compile(r'\s|<|>') #Remove all white space and brackets
        b = r.sub('',line)
        edges = b.split(',')
        v1 = vertexNames[edges[0]]
        v2 = vertexNames[edges[1]]
        g.edgeList.append(edge(v1,v2, 'n/a'))

    return g



def compareGraphs(str1, str2):
    g1 = createGraphFromStr(str1)
    # g1.printGraph()

    g2 = createGraphFromStr(str2)

    return g1.compare(g2)
    

class testAll(unittest.TestCase):

    def setUp(self):
        self.streetDB = streetDataBase()

    def sendCmd(self, line):
        out = StringIO()
        parseInput(self.streetDB, line, out, out)
        return out.getvalue()

    def sendCheckResponse(self, line, error):
        output = self.sendCmd(line)
        self.assertEqual(output, error)

    def test_invalidAddStreetNames(self):
        line = 'a "" (1,2) (3,4)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a"test" (1,2) (3,4)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a "test"(1,2) (3,4)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a "te9st" (1,2) (3,4)'
        self.sendCheckResponse(line, ERROR_INVALID)

    def test_invalidAddStreet(self):
        line = 'a "test" (1,2)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a "test" (1,2) (3 3,4)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a "test" (1,2) (1s,32)'
        self.sendCheckResponse(line, ERROR_INVALID)
        line = 'a "test" (0,0) (0,1) (2,2) (-1,0)'
        self.sendCheckResponse(line, ERROR_SELF_INTERSECT)
        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        line = 'a "Weber Street" (2,-1) (2,3)'
        self.sendCheckResponse(line, DUPLICATE_ERROR)

        line = 'a "Weber STREET" (2,-1) (2,3)'
        self.sendCheckResponse(line, DUPLICATE_ERROR)
        


    def test_streetChange(self):

        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'c "Weber Street" (2,-1) (2,2) (5,5) (6,6) (3,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        line = 'c "Street" (2,-1) (2,2) (5,5) (6,6) (3,8)'
        self.sendCheckResponse(line, NON_EXIST_ERROR)

        line = 'r "test"'
        self.sendCheckResponse(line, NON_EXIST_ERROR)

        line = 'r "Weber Street"'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        self.assertTrue(compareGraphs(output, NULL_GRAPH));

    def test_assignmentExample(self):
        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "King Street S" (4,2) (4,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "Davenport Road" (1,4) (5,8)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        self.assertTrue(compareGraphs(output, ASSIGN_EX_1));

        line = 'c "Weber Street" (2,1) (2,2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        self.assertTrue(compareGraphs(output, ASSIGN_EX_2));

        line = 'r "King Street S"'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        self.assertTrue(compareGraphs(output, NULL_GRAPH));

    def test_colinear(self):
        line = 'a "street one" (-2,2) (-2,-1) (2,-1) (2,-3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street two" (-3,1) (-2,1) (-2,0) (-3,0)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street three" (0,0) (0,-1) (5,-1) (5,0)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street four" (2,5) (5,2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street five" (2,6) (3,4) (4,3) (6,2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        line = 'a "street six" (2,4) (5,1)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street seven" (3,3) (4,2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)


        output = self.sendCmd('g')
        print(output)

    def test_parallel(self):
        line = 'a "street one" (-3, -3) (3,3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street two" (-2,-3) (4,3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street three" (-1,-3) (5,3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street four" (0,-3) (6,3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street five" (-3,6) (6,-3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        print(output)

    def test_non_intersect(self):
        # two parallel ones
        line = 'a "street one" (-3, -3) (-2,-2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street two" (-2, -3) (-1,-2)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)


        line = 'a "street three" (0,0) (1,1)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "street four" (3,1) (4,0)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        print(output)

    def test_total_overlap(self):
        line = 'a "a" (1,1)(5,5)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)
        line = 'a "b" (2,2)(3,3)'
        self.sendCheckResponse(line, COMMAND_ACCEPTED)

        output = self.sendCmd('g')
        print(output)


if __name__ == '__main__':
    unittest.main()