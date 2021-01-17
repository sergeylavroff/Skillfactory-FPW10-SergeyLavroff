class Volunteers:
    def __init__(self, fname, lname, city, balance, status):
        self.fname = fname
        self.lname = lname
        self.balance = balance
        self.city = city
        self.status = status
    def getName(self):
        return str( self.fname + ' ' + self.lname )
    def getBalance(self):
        return self.balance
    def getAddress(self):
        return self.city
    def getStatus(self):
        return self.status
    def strNameBal(self):
        return str( f' {self.fname} {self.lname}, баланс {self.balance} ')
    def strFullInfo(self):
        return str( f' {self.fname} {self.lname}, г. {self.city}, статус "{self.status}". ')

class Guests:
    def __init__(self, name):
        self.name = name
        self.guests = []
    def add_guest(self, VolID):
        self.guests.append(VolID)
    def print_guests(self):
        print(f"Гости на корпоративе {self.name}:")
        for guest in self.guests:
            print(guest.strFullInfo())