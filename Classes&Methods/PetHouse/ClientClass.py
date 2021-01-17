class Volunteers:
    def __init__(self, fname, lname, address, balance, status):
        self.fname = fname
        self.lname = lname
        self.balance = balance
        self.address = address
    def getName(self):
        return str( self.fname + ' ' + self.lname )
    def getBalance(self):
        return self.balance
    def getAddress(self):
        return self.address
    def getStatus(self):
        return self.status

