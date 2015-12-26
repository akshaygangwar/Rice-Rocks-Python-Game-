# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
expl_time = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
explosion_dim = 24

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0,0]
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    #key handlers
    def keydown(self, key):
        global started
        if started:
            ang_vel = 0.04
            if key == simplegui.KEY_MAP["left"]:
                self.angle_vel -= ang_vel
            elif key == simplegui.KEY_MAP["right"]:
                self.angle_vel += ang_vel
            elif key == simplegui.KEY_MAP["up"]:
                self.thrust = True
                if self.thrust == True:
                    ship_thrust_sound.play()
            elif key == simplegui.KEY_MAP["space"]:
                self.shoot()
                missile_sound.play()
            
        
    def keyup(self, key):
        ang_vel = 0
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel = ang_vel
        elif key == simplegui.KEY_MAP["right"]:
            self.angle_vel = ang_vel
        elif key == simplegui.KEY_MAP["up"]:
            self.thrust = False
            if self.thrust == False:
                ship_thrust_sound.pause()
    
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def update(self):
        
        self.pos[0] += self.vel[0] #% WIDTH
        self.pos[1] += self.vel[1] #% HEIGHT
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        self.vel[0] *= 0.97
        self.vel[1] *= 0.97
        if self.thrust == True:
            self.forward = angle_to_vector(self.angle)
            self.vel[0] += self.forward[0] * 0.2
            self.vel[1] += self.forward[1] * 0.2
        pass
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        global expl_time
        # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated:
            explosion_index = (expl_time % explosion_dim) // 1
            explosion_center = self.image_center
            current_explosion_center = explosion_center[0] + explosion_index * self.image_size[1], self.image_center[1]
            canvas.draw_image(self.image, current_explosion_center, self.image_size, self.pos, self.image_size)
            expl_time +=1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_rad = other_object.get_radius()
        separation = dist(self.pos,other_pos)
        if separation < self.radius + other_rad:
            return True
        else:
            return False
        
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0] % WIDTH
        self.pos[1] += self.vel[1] % HEIGHT
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += 1
        if self.age < self.lifespan:
            return True
        else:
            return False
        pass        

           
def draw(canvas):
    global time, lives, started, rock_group, missile_group, explosion_group, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    if started:
        my_ship.draw(canvas)
        #a_rock.draw(canvas)
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    if group_collide(rock_group, my_ship):
        lives -= 1
    group_group_collide(rock_group, missile_group)
    
    if lives == 0:
        started = False
        rock_group = set([])
        timer.stop()
        soundtrack.rewind()
    # a_rock.update()
    #a_missile.update()
    
    # draw splash screen
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2,  HEIGHT/2], splash_info.get_size())
    
    # display score and lives 
    canvas.draw_text("Lives: " + str(lives), [20,30], 25, "White")
    canvas.draw_text("Score: " + str(score), [670, 30], 25, "White")

def mouseclick(position):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inside_width = (center[0] - size[0] / 2) < position[0] < (center[0] + size[0] / 2)
    inside_height = (center[1] - size[1] / 2) < position[1] < (center[1] + size[1] / 2)
    if (not started) and inside_width and inside_height:
        started = True
        lives = 3
        score = 0
        timer.start()
        rock_spawner()
        soundtrack.play()
    
def process_sprite_group(group, canvas):
    for sprite in group:
        remove_sprite = set([])
        sprite.draw(canvas)
        if sprite.update() == False:
            remove_sprite.add(sprite)
        group.difference_update(remove_sprite)

def group_collide(group,  other_object):
    global explosion_group
    remove_set = set([])
    for sprite in group:
        if sprite.collide(other_object) == True:
            remove_set.add(sprite)
            explosion_group.add(Sprite(sprite.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
        group.difference_update(remove_set)
    if len(remove_set) > 0:
        return True

def group_group_collide(group1, group2):
    remove_set = set([])
    global score
    for sprite in group1:
        if group_collide(group2,sprite) == True:
            score += 10
            remove_set.add(sprite)
        group1.difference_update(remove_set)

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, started
    position = [WIDTH * random.random(), HEIGHT * random.random()]
    distance = dist(position, my_ship.get_position())
    if len(rock_group) <12 and started:
        if distance > my_ship.get_radius() + asteroid_info.get_radius() + 100:
            rock_group.add(Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], [random.random(), random.random()], 0, (float(random.randrange(9))/100) - 0.049, asteroid_image, asteroid_info))
        #print rock_group
        
    

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.02, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(my_ship.keydown)
frame.set_keyup_handler(my_ship.keyup)
frame.set_mouseclick_handler(mouseclick)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

