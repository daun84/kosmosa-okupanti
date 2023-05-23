import pickle
import model

objects = []

# aliens
for i in range(5):
    for j in range(7):
        objects.append(model.Alien(i * 2, j * 4, '\O/', 3))

for i in range(4):
    for j in range(7):
        for k in range(3):
            objects.append(model.Wall(model.Game.map_height - 5 + i, 2 + j * 7 + k, '#', 1, model.EnumTeam.NONE))

with open('starting_pos.pickle', 'wb') as file:
    pickle.dump(objects, file)
