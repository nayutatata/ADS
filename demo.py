import carla
import random
import numpy as np
client = carla.Client('localhost',2000)
world = client.get_world()

# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Set up the TM in synchronous mode
traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

# Set a seed so behaviour can be repeated if necessary
traffic_manager.set_random_device_seed(0)
random.seed(0)

# We will aslo set up the spectator so we can see what we do
spectator = world.get_spectator()
# Get the blueprint library and filter for the vehicle blueprints
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')

# print(vehicle_blueprints)

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()

cars = []
helper = world.debug
tras = []
# Spawn 50 vehicles randomly distributed throughout the map 
# for each spawn point, we choose a random vehicle from the blueprint library
for i in range(0,30):
    car = world.try_spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points)) # if fails return None
    if car is not None:
        cars.append(car)
        tras.append([])

# ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points)) # if fails raise an exception.
print("cars: "+str(len(cars)))
print("tras: "+str(len(tras)))

for vehicle in cars:
    vehicle.set_autopilot(True)
    # traffic_manager.ignore_lights_percentage(vehicle, random.randint(0,50))

while(True):
    for i,c in enumerate(cars):
        location = c.get_location()
        rotation = c.get_transform().rotation
        tras[i].append(location)
        if (len(tras[i])>1):
            #helper.draw_line(begin = tras[i][-1],end = tras[i][-2])
            helper.draw_line(begin = location,end = location + carla.Location(x =10*np.cos(rotation.yaw),y = 10*np.sin(rotation.yaw)),life_time = 1)
    world.tick() # only in this way the world can really become alive.