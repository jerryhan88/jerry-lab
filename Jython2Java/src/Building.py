from org.jython.book.interfaces import BuildingType
# Notice the doc string that has been added after the class definition below

class Building(BuildingType):
    ''' Class to hold building objects '''

    def __init__(self):
        self.name = None
        self.address = None
        self.id = -1

    def getBuildingName(self):
        return self.name

    def setBuildingName(self, name):
        self.name = name;

    def getBuildingAddress(self):
        return self.address

    def setBuildingAddress(self, address):
        self.address = address

    def getBuildingId(self):
        return self.id

    def setBuildingId(self, id):
        self.id = id

    def getDoc(self):
        return self.__doc__