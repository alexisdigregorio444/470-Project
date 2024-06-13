import numpy as np
import statistics as stats
import random
from vpython import cone, vector, rate, color, canvas
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

np.random.seed(0)

#TODO Randomize other relay/user parameters

colors = ['blue', 'green', 'orange', 'yellow']
class Resource:
     def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.colors = ['blue', 'green'] # or orange, or yellow
        self.TxRate = 40
        self.RxRate = 35
        self.velocity = [0, 0, 0]
        self.connection = None

class Relay(Resource):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.connection = []

class House(Resource):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.connection_made = False

class Car(Resource):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

class Phone(Resource):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

class Server(Resource):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

def getImage(path, zoom):
   return OffsetImage(plt.imread(path, format="png"), zoom=zoom)

fig, ax = plt.subplots()

ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.set_box_aspect(1)

# Generate 60 Total Houses
houses = []
# city 1
nHouses = 25
hx = np.random.randint(40, 100, nHouses)
hy = np.random.randint(40, 100, nHouses)

# city 2
nHouses = 15
x = np.random.randint(540, 600, nHouses)
y = np.random.randint(280, 320, nHouses)
hx = np.append(hx, x)
hy = np.append(hy, y)

# rural
nHouses = 20
x = np.random.randint(5, 595, nHouses)
y = np.random.randint(5, 595, nHouses)
hx = np.append(hx, x)
hy = np.append(hy, y)

path = 'house.png'
for x, y in zip(hx, hy):
     house = House(x, y, 0)
     house.colors = np.random.choice(colors, 2)
     house.TxRate = 1
     house.RxRate = np.random.choice([1, 2, 5], 1) # Worker, Streamer, or Gamer
     houses.append(house)
     ab = AnnotationBbox(getImage(path, .2), (x, y), frameon=False)
     ax.add_artist(ab)

# Generate 15 Total Cars
# highway cars
cars = []
nCars = 10
city1 = np.array([70, 70])
city2 = np.array([560, 300])
d = np.linalg.norm(city2-city1)
t = np.random.randint(0, d, nCars)
slope = city2-city1
slope = slope/d
carsx = [city1[0] + slope[0]*s for s in t]
carsy = [city1[1] + slope[1]*s for s in t]

# rural cars
nCars = 5
x = np.random.randint(5, 595, nCars)
y = np.random.randint(5, 595, nCars)
carsx = np.append(carsx, x)
carsy = np.append(carsy, y)

path = 'car.png'
for x, y in zip(carsx, carsy):
     car = Car(x, y, 0)
     car.colors = np.random.choice(colors, 2)
     car.RxRate = np.random.choice([.25, .5, 1], 1) # Listener, Worker, Kid
     car.TxRate = 0
     car.velocity = np.random.rand(1, 2)*5 # 5 is max speed
     cars.append(car)
     ab = AnnotationBbox(getImage(path, .2), (x, y), frameon=False)
     ax.add_artist(ab)

# Generate 60 Total Phones
phones = []

# highway phones
nPhones = 20
t = np.random.randint(0, d, nPhones)
px = [city1[0] + slope[0]*s for s in t]
py = [city1[1] + slope[1]*s for s in t]

# city 1 phones
nPhones = 15
x = np.random.randint(40, 100, nPhones)
y = np.random.randint(40, 100, nPhones)
px = np.append(px, x)
py = np.append(py, y)

# city 2 phones
nPhones = 15
x = np.random.randint(540, 600, nPhones)
y = np.random.randint(280, 320, nPhones)
px = np.append(px, x)
py = np.append(py, y)

# rural phones
nPhones = 10
x = np.random.randint(5, 595, nPhones)
y = np.random.randint(5, 595, nPhones)
px = np.append(px, x)
py = np.append(py, y)

path = 'phone.png'
for x, y in zip(px, py):
     phone = Phone(x, y, 0)
     phone.colors = np.random.choice(colors, 2)
     phone.RxRate = np.random.choice([.5, 1, 2], 1) # Scroller, Navigator, Streamer
     phone.TxRate = np.random.choice([.5, 1], 1) # Navigator, Scroller
     phone.velocity =  np.random.rand(1, 2)*2 # 5 is max speed
     phones.append(phone)
     ab = AnnotationBbox(getImage(path, .2), (x, y), frameon=False)
     ax.add_artist(ab)

# Generate Servers
servers = []
# Rural Servers
nServers = 5
sx = np.random.randint(5, 595, nServers)
sy = np.random.randint(5, 595, nServers)
# City 1 Servers
nServers = 3
x = np.random.randint(40, 100, nServers)
y = np.random.randint(40, 100, nServers)
sx = np.append(sx, x)
sy = np.append(sy, y)

# City 2 Servers
nServers = 2
x = np.random.randint(540, 600, nServers)
y = np.random.randint(280, 320, nServers)
sx = np.append(sx, x)
sy = np.append(sy, y)

path = 'server.png'
for x, y in zip(sx, sy):
     server = Server(x, y, 0)
     server.colors = np.random.choice(colors, 2)
     server.TxRate = 100
     server.RxRate = 30
     server.velocity = [0, 0, 0]
     servers.append(server)
     ab = AnnotationBbox(getImage(path, .3), (x, y), frameon=False)
     ax.add_artist(ab)

# Generate Relays
relays = []
rx = np.arange(100, 600, 200)
ry = np.arange(100, 600, 200)
for x in rx:
    for y in ry:
        ax.add_patch(plt.Circle((x, y), 201.5, facecolor="none", edgecolor='blue'))
        relay = Relay(x, y, 100)
        relay.colors = np.random.choice(colors, 3)
        relay.TxRate = 200
        relay.RxRate = 100
        relay.velocity = [10, 10, 0]
        relays.append(relay)
        ab = AnnotationBbox(getImage('relay.png', .4), (x, y), frameon=False)
        ax.add_artist(ab)
ax.add_patch(plt.Rectangle((0, 0), 600, 600, facecolor='none', edgecolor='black'))

# Generate links between pairs and triples
np.random.shuffle(houses)
np.random.shuffle(cars)
np.random.shuffle(phones)
np.random.shuffle(servers)

# house to relay: 225  - find if the hosue is wihitn range of a rlay

for relay in relays:
    relay_Rx = 0
    for house in houses:
        if house.connection_made is False:
            relay_earth_dist = np.sqrt(255**2 - 100**2) # distance raly can be from house in x or y
            distance_house_relay_x  = np.linalg.norm(np.array(house.pos[0]) - np.array(relay.pos[0]))
            distance_house_relay_y = np.linalg.norm(np.array(house.pos[1]) - np.array(relay.pos[0]))

            if distance_house_relay_x <= relay_earth_dist and distance_house_relay_y <= relay_earth_dist:
                house.connection_made = True
                house.connection = relay
                relay.connection.append([house])
                # update server Rx 
                relay_Rx += house.TxRate
                relay.Rx = relay_Rx
                if relay.Rx >= server.RxRate: 
                    relay.full = True
                    break

# now move on to houses connecting to servers if they are not already connected to a relay

for house in houses: 
    if house.connection_made is not True:
        for server in servers:
            server_Rx = 0
            for house in houses:
                if house.connection_made is False:
                    server_earth_dist = np.sqrt(255**2 - 100**2) # this should be updated with the server dist
                    distance_house_server_x  = np.linalg.norm(np.array(house.pos[0]) - np.array(server.pos[0]))
                    distance_house_server_y = np.linalg.norm(np.array(house.pos[1]) - np.array(server.pos[0]))

                    if distance_house_server_x <= server_earth_dist and distance_house_server_y <= server_earth_dist:
                        house.connection_made = True
                        house.connection = server
                        server.connection.append([house])
                        # update server Rx 
                        server_Rx += house.TxRate
                        server.Rx = server_Rx
                        if server.Rx >= server.RxRate: 
                            server.full = True
                            break
            # connect to this server 


for i, j in zip(range(40, 60), range(0, 20)):
    houses[i].connection = phones[j]
    phones[j].connection = houses[i]

for car in cars:
    server = servers[np.random.randint(0,10)]
    car.connection = server
    server.connection = car

for p in range(20, 35):
    phones[p].connection = phones[p + 15]
    phones[p + 15].connection = phones[p]

for p in range(50, 60):
    server = servers[np.random.randint(0, 10)]
    phones[p].connection = server
    server.connection = phones[p]

for _ in houses:
    ax.plot([_.pos[0], _.connection.pos[0]], [_.pos[1], _.connection.pos[1]])

ax.autoscale()

plt.show()

# add in MBFA ):