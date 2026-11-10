#players

p1 = []
p2 = []
p3 = []
p4 = []
p5 = []
p6 = []
p7 = []
p8 = []


#How mnay players are playing?
players = int(input())


#create cards and decks

class BabyCorns:
    def __init__(self, type, name, amount):
        self.name = name
        self.type = type
        self.amount = amount

class BasicCorns:
    def __init__(self, type, name, amount):
        self.name = name
        self.type = type
        self.amount = amount

class MagicCorns:
    def __init__(self, type, name, amount, ability):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability

class MagicSpell:
    def __init__(self, type, name, amount, ability):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability


class Interrupts:
    def __init__(self, type, name, amount, ability):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability


class Upgrades:
    def __init__(self, type, name, amount, ability):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability


class Downgrades:
    def __init__(self, type, name, amount, ability):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability

#nursery cards
red = BabyCorns("bby", "Baby Unicorn", 1)
pink = BabyCorns("bby", "Baby Unicorn", 1)
orange = BabyCorns("bby", "Baby Unicorn", 1)
yellow = BabyCorns("bby", "Baby Unicorn", 1)
green = BabyCorns("bby", "Baby Unicorn", 1)
blue = BabyCorns("bby", "Baby Unicorn", 1)
purple = BabyCorns("bby", "Baby Unicorn", 1)
black = BabyCorns("bby", "Baby Unicorn", 1)
white = BabyCorns("bby", "Baby Unicorn", 1)
brown = BabyCorns("bby", "Baby Unicorn", 1)
rainbow = BabyCorns("bby", "Baby Unicorn", 1)
death = BabyCorns("bby", "Baby Unicorn", 1)
narwhal = BabyCorns("bby", "Baby Unicorn", 1)


#main deck

#basics
Red = BasicCorns("bsc", "Basic Unicorn", 3)
Orange BasicCorns("bsc", "Basic Unicorn", 3)
Yellow = BasicCorns("bsc", "Basic Unicorn", 3)
Green = BasicCorns("bsc", "Basic Unicorn", 3)
Blue = BasicCorns("bsc", "Basic Unicorn", 3)
Indigo = BasicCorns("bsc", "Basic Unicorn", 3)
Purple = BasicCorns("bsc", "Basic Unicorn", 3)
Narwhal = BasicCorns("bsc", "Basic Unicorn", 3)


#magics
Rhinocorn = MagicCorns("bsc", "Basic Unicorn", 3, )