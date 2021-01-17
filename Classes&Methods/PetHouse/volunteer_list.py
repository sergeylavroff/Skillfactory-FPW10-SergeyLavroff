from VolunteersClass import Volunteers, Guests

vol001 = Volunteers( "Сергей", "Иванов", "Москва", 100, "Кошатник" )
vol002 = Volunteers( "Максим", "Истратов", "Москва", 200, "Собачник" )
vol003 = Volunteers( "Иван", "Васечкин", "Санкт-Петербург", 300, "Идейный вдохновитель" )
vol004 = Volunteers( "Марина", "Соколова", "Москва", 120, "Руководитель" )

print(vol004.strNameBal())

CorpMsk = Guests('Московская сходка')

CorpMsk.add_guest(vol001)
CorpMsk.add_guest(vol002)
CorpMsk.add_guest(vol004)

CorpMsk.print_guests()