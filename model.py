from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class EnumPlayerTurns(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    FIRE = 3

class EnumTeam(Enum):
    NONE = 0
    PLAYER = 1
    ALIENS = 2

class Object(ABC):
    def __init__(self, y, x, body, color, team):
        self.y = y
        self.x = x
        self.body: str = body
        self.color = color
        self.team = EnumTeam(team)
        self.direction = (0, 0) # (y, x)
        self.move_rate = 1 # frames count between each move()

    @abstractmethod
    def move(self):
        pass

class Player(Object):
    def __init__(self, y, x, body, color, team):
        super().__init__(y, x, body, color, team)

    def move(self):
        _, x = self.direction
        self.x = max(0, min(self.x + x, Game.map_width - len(self.body)))
        direction = (0, 0)

    def change_direction(self, turn: EnumPlayerTurns):
        if turn == EnumPlayerTurns.LEFT:
            self.direction = (0, -1)
        elif turn == EnumPlayerTurns.RIGHT:
            self.direction = (0, 1)
        else:
            self.direction = (0, 0)

    def fire(self):
        Game.create_object(self.y - 1, self.x + 1, "|", 2, EnumTeam.PLAYER, Rocket)    
    
class Wall(Object):
    def move(self):
        pass

class Alien(Object):
    def __init__(self, y, x, body, color):
        self.move_rate = 1
        super().__init__(y, x, body, color, EnumTeam.ALIENS)

    def animate(self, index):
        #skins = ["uwu", "UwU", "owo", "OwO"]
        skins = ["\O/", "-O-", "/O\\"]
        self.body = skins[index]

    def change_direction(self, pair):
        self.direction = pair

    def move(self):
        self.y += self.direction[0]
        self.x += self.direction[1]
        self.direction = (0, 0)

    def fire(self):
        Game.create_object(self.y + 1, self.x + 1, "|", 3, EnumTeam.ALIENS, Rocket)

class Rocket(Object):
    def __init__(self, y, x, body, color, team):
        super().__init__(y, x, body, color, team)
        if team == EnumTeam.PLAYER:
            self.direction = (-1, 0)
        else:
            self.direction = (1, 0)

        self.move_rate = 1

    def move(self):
        y, _ = self.direction
        self.y = max(0, min(self.y + y, Game.map_height))

class Game:
    objects: List[Object] = []
    player: Player
    map_width: int = 49 # 49
    map_height: int = 20 # 20 
    time: int = 0
    alien_moves = []
    highscore = 0
    health = 3

    @classmethod
    def create_object(cls, y, x, body, color, team, type):
        cls.objects.append(type(y, x, body, color, team))

    @classmethod
    def get_starting_position(cls):
        # player
        cls.create_object(cls.map_height, cls.map_width // 2 - 1, "/^\\", 2, EnumTeam.PLAYER, Player)
        cls.player = cls.objects[0]
        # aliens
        for i in range(5):
            for j in range(7):
                cls.objects.append(Alien(i * 2, j * 4, '\O/', 3))
        # walls
        for i in range(4):
            for j in range(7):
                for k in range(3):
                    cls.objects.append(Wall(Game.map_height - 5 + i, 2 + j * 7 + k, '#', 1, EnumTeam.NONE))
        # moves for aliens
        with open('alien_moves.txt', 'r') as file:
            for line in file:
                values = line.strip().split()
                y, x = int(values[0]), int(values[1])
                cls.alien_moves.append((y, x))

        
    @classmethod
    def invoke_alien_attack(cls):
        aliens: List[Alien] = []
        for obj in cls.objects:
            if type(obj) == Alien:
                aliens.append(obj)

        aliens.sort(key=lambda obj: (obj.x, -obj.y))

        x = -1
        for obj in aliens:
            if x != obj.x:
                x = obj.x
                obj.fire()

    @classmethod
    def destroy_object(cls, obj: Object):
        if type(obj) == Alien:
            cls.highscore += 100
        if type(obj) == Player:
            cls.health -= 1
        else:
            cls.objects.remove(obj)

    @classmethod
    def handle_collision(cls, target: Object):
        for obj in cls.objects:
            if obj == target:
                continue
            same_x = (obj.x <= target.x + len(target.body) - 1 and (target.x <= len(obj.body) + obj.x - 1))
            if obj.y == target.y and same_x:
                cls.destroy_object(obj)
                cls.destroy_object(target)
                if type(target) != Player:
                    return
        if type(target) == Rocket and (target.y == 0 or target.y == cls.map_height):
            cls.destroy_object(target)

    @classmethod
    def update(cls, turn: EnumPlayerTurns):
        cls.player.change_direction(turn)

        if cls.time % 10 == 0:
            for obj in cls.objects:
                if type(obj) == Alien:
                    obj.change_direction(cls.alien_moves[cls.time // 10])

        if cls.time % 5 == 0:
            for obj in cls.objects:
                if type(obj) == Alien:
                    obj.animate((cls.time // 5) % 3)

        for obj in cls.objects:
            cls.handle_collision(obj)
            if cls.time % obj.move_rate == 0:
                obj.move()

        if cls.time % 15 == 0:
            cls.invoke_alien_attack()

        if turn == EnumPlayerTurns.FIRE:
            cls.player.fire()

        cls.time += 1
        
        game_result = 0
        if cls.health <= 0 or (cls.time + 1) // 10 == 97:
            game_result = -1
        else:
            check = True
            for obj in cls.objects:
                if type(obj) == Alien:
                    check = False
            if check:
                game_result = 1   
               


        return game_result
