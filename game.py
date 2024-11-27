import enum
from os import system,name, get_terminal_size
from random import randrange, choice
from enum import Enum
from termcolor import colored
from time import sleep
from ansio import ansi_input, application_keypad, mouse_input
from ansio.input import InputEvent, get_input_event

COL, ROW = get_terminal_size()

quotes:list[str] = ['the random game dev','(not a very good coder)','why are you reading this','beep boop bap','10101110010001000100101001']
logo = [
f'{'a game by'.center(COL)}\n\n\n\n\n\n\n',
f'''{'a game by'.center(COL)}‎
 _____                  ‎
|  _  |                 ‎
|     |                 ‎
|__|__|                 ‎


''',
f'''{'a game by'.center(COL)}‎
 _____                  ‎
|  _  |___              ‎
|     |  _|             ‎
|__|__|_|               ‎


''',
f'''{'a game by'.center(COL)}‎
 _____     _            ‎
|  _  |___| |_          ‎
|     |  _|  _|         ‎
|__|__|_| |_|           ‎


''',
f'''{'a game by'.center(COL)}‎
 _____     _            ‎
|  _  |___| |_ _ _      ‎
|     |  _|  _| | |     ‎
|__|__|_| |_| |_  |     ‎
              |___|     ‎

''',
f'''{'a game by'.center(COL)}‎
 _____     _            ‎
|  _  |___| |_ _ _ _ _  ‎
|     |  _|  _| | | | | ‎
|__|__|_| |_| |_  |___| ‎
              |___|     ‎

''',
f'''{'a game by'.center(COL)}‎
 _____     _           _‎
|  _  |___| |_ _ _ _ _|_|
|     |  _|  _| | | | | |
|__|__|_| |_| |_  |___|_|
              |___|     ‎

''',
f'''{'a game by'.center(COL)}‎
 _____     _           _‎
|  _  |___| |_ _ _ _ _|_|
|     |  _|  _| | | | | |
|__|__|_| |_| |_  |___|_|
              |___|     ‎
{choice(quotes).center(COL)}
''',
]

displaylogo = True

def chance(procent: int) -> bool:
    rand = randrange(0,100)
    if rand <= procent:
        return True
    else:
        return False

def clear() -> None:
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def print_in_center(strings: list) -> None:
    for index, string in enumerate(strings):
        space_before_str = " " * ((COL - len(string)) // 2)
        if index == 0:
            center_row = "\n" * (ROW // 2 - len(strings))
            print(center_row + space_before_str + string)
        else:
            print(space_before_str + string)

clear()
if displaylogo:
    for i, text in enumerate(logo):
        print_in_center(text.splitlines())
        if i != len(logo) - 1:
            sleep(0.5)
        else:
            sleep(1.0)
        clear()

class Array2d:
    def __init__(self, x: int, y: int, z) -> None:
        self.l = []
        self.x = x
        self.y = y
        for j in range(y):
            self.l.append([])
            for _ in range(x):
                self.l[j].append(z)

    def set(self, x:int, y:int, z):
        self.l[y][x] = z

    def get(self, x:int, y:int):
        return self.l[y][x]

    def print(self):
        for ly in range(self.y):
            for lx in range(self.x):
                print(self.l[ly][lx],end='')
            print()

class GameObject:
    def __init__(self):
        self.glyph        = ''
        self.name         = 'empty'
        self.interactable = False
        self.passable     = False
        self.hp           = -1
        self.pickup       = False

    def interact(self):
        if not self.interactable:
            return
        print(f"interacted with: {self.name}")

    def __str__(self):
        return self.glyph

class Wall(GameObject):
    def __init__(self):
        super().__init__()
        self.glyph = '#'
        self.name  = 'wall'

class Floor(GameObject):
    def __init__(self):
        super().__init__()
        self.glyph    = colored('.', 'blue')
        self.name     = 'floor'
        self.passable = True

class Key(GameObject):
    def __init__(self):
        super().__init__()
        self.passable = True
        self.name     = 'key'
        self.glyph    = colored('k', 'light_grey')

class Player(GameObject):
    def __init__(self,x,y):
        super().__init__()
        self.passable = True
        self.name     = 'player'
        self.glyph    = colored('@', 'green')
        self.x        = x
        self.y        = y

class EnemySpawner(GameObject):
    def __init__(self):
        super().__init__()
        self.passable = True
        self.name     = 'EnemySpawner'
        self.glyph    = colored('E','light_blue')

class Chest(GameObject):
    def __init__(self):
        super().__init__()
        self.name  = 'chest'
        self.glyph = colored('c','light_red')

class RoomTypes(Enum):
    KeyDoor = { 'DoorLocked': True, 'Enemies': chance(50), 'Chest': False, 'Boss': False, 'BestNext': ['Chest', 'Boss'], 'DeadEnemySpawn': [['Key', chance(50)], ] }
    Enemy   = 2
    Boss    = 3
    Chest   = 4

def set_amount_random(array: Array2d, amount: int, z):
    tcoordinates = []
    coordinates  = []
    for y in range(array.y):
        for x in range(array.x):
            tcoordinates.append((x,y))
    for i in tcoordinates:
        if i[0] in (array.x-1,0):
            pass
        elif i[1] in (array.y-1,0):
            pass
        else:
            coordinates.append(i)
    while amount != 0:
        c = choice(coordinates)
        array.set(c[0],c[1],z)
        amount -= 1

def CreateBase(x,y,difficulty = 1):
    x += 2
    y += 2
    base = Array2d(x,y,Floor())

    spawners = difficulty
    chests   = difficulty // 3 % 3 if difficulty >= 3 else 0

    for ly in range(y):
        if ly in (y-1,0):
            for lx in range(x):
                base.set(lx,ly,Wall())
        else:
            for lx in range(x):
                if lx in (x-1,0):
                    base.set(lx,ly,Wall())
    set_amount_random(base,spawners,EnemySpawner())
    set_amount_random(base,chests,Chest())
    return base

class Room:
    def __init__(self, base: Array2d, roomtype: RoomTypes):
        self.room = base
        self.roomtype = roomtype

    def add_object(self, x: int, y: int, z: GameObject):
        self.room.set(x,y,z)

    def print(self):
        self.room.print()

x = 5 #randrange(1,30)
y = 5 #randrange(1,30)
base = CreateBase(x,y)
room = Room(base, RoomTypes.Chest)
player = Player(x // 2, y // 2)
room.add_object(x // 2, y // 2, player)
room.print()
underplayer = Floor()

with ansi_input, application_keypad, mouse_input:
    while True:
        event: InputEvent = get_input_event()
        if event.shortcut in ('up','down','left','right'):
            room.add_object(player.x,player.y,underplayer)
            match event.shortcut:
                case 'up':
                    player.y -= 1
                case 'down':
                    player.y += 1
                case 'left':
                    player.x -= 1
                case 'right':
                    player.x += 1
            underplayer = room.room.get(player.x,player.y)
            room.add_object(player.x,player.y,player)
        if player.x == room.room.x | player.y == room.room.y:
            clear()
        print(f'\033[{room.room.y + 2}A',end='')
        room.print()
