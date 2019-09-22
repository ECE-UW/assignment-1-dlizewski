import unittest
from a1ece650 import *
from StringIO import StringIO

ERROR_INVALID = 'Error: Invalid Input\n'
ERROR_SELF_INTERSECT = 'Error: Streets Cannot Self Intersect\n'
COMMAND_ACCEPTED = ''

class testAll(unittest.TestCase):

    def setUp(self):
        self.streetDB = streetDataBase()

    def sendCmd(self, cmd, line):
        out = StringIO()
        cmd(self.streetDB, line, out, out)
        return out.getvalue()

    def sendCheckResponse(self, cmd, line, error):
        output = self.sendCmd(cmd, line)
        self.assertEqual(output, error)

    def test_invalidAddStreetNames(self):
        line = 'a "" (1,2) (3,4)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a"test" (1,2) (3,4)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a "test"(1,2) (3,4)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a "te9st" (1,2) (3,4)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

    def test_invalidAddStreet(self):
        line = 'a "test" (1,2)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a "test" (1,2) (3 3,4)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a "test" (1,2) (1s,32)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_INVALID)

        line = 'a "test" (0,0) (0,1) (2,2) (-1,0)'
        self.sendCheckResponse(parseAddCommand, line, ERROR_SELF_INTERSECT)

        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)


    def test_assignmentExample(self):
        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "King Street S" (4,2) (4,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "Davenport Road" (1,4) (5,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)


        output = self.sendCmd(parseGraphCommand, 'g')
        print(output)

    def test_assignmentExample(self):
        line = 'a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "King Street S" (4,2) (4,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "Davenport Road" (1,4) (5,8)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)


        output = self.sendCmd(parseGraphCommand, 'g')
        print(output)

    def test_colinear(self):
        line = 'a "street one" (-2,2) (-2,-1) (2,-1) (2,-3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street two" (-3,1) (-2,1) (-2,0) (-3,0)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street three" (0,0) (0,-1) (5,-1) (5,0)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street four" (2,5) (5,2)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street five" (2,6) (3,4) (4,3) (6,2)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)

        output = self.sendCmd(parseGraphCommand, 'g')
        print(output)

    def test_parallel(self):
        line = 'a "street one" (-3, -3) (3,3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street two" (-2,-3) (4,3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street three" (-1,-3) (5,3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street four" (0,-3) (6,3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street five" (-3,6) (6,-3)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)

        output = self.sendCmd(parseGraphCommand, 'g')
        print(output)

    def test_non_intersect(self):
        # two parallel ones
        line = 'a "street one" (-3, -3) (-2,-2)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street two" (-2, -3) (-1,-2)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)


        line = 'a "street three" (0,0) (1,1)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)
        line = 'a "street four" (3,1) (4,0)'
        self.sendCheckResponse(parseAddCommand, line, COMMAND_ACCEPTED)

        output = self.sendCmd(parseGraphCommand, 'g')
        print(output)


if __name__ == '__main__':
    unittest.main()