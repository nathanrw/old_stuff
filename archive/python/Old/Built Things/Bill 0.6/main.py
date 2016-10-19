#The Amazing Chilvers Game
#Main file

#And thus begins a rather poor attempt at coding a game, but a pretty good
#stab at a practical joke.

#Import py
import pygame, os, random
from pygame.locals import *
from math import *
import enemies, projectiles
from LoadRes import *

#Ready the text!
pygame.font.init()

#Ready the random!
random.seed()

#Window size
SCREENRECT = Rect(0, 0, 800, 320)

#Set up the sound
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
global channel0
channel0 = pygame.mixer.Channel(0)
global channel1
channel1 = pygame.mixer.Channel(1)

global channel2
channel2 = pygame.mixer.Channel(2)
global gatling
gatling = LoadSound("gatling.wav")

#Some Constants
global incoming
incoming = pygame.sprite.OrderedUpdates()
global fireball_sprites
fireball_sprites = pygame.sprite.OrderedUpdates()
global particles
particles = pygame.sprite.OrderedUpdates()
global emitters
emitters = []

#Top status bar thing
class HealthBar():
    def __init__(self):
        self.healthbarimg = ImportImg("top_bar.bmp").convert()
        self.image = ImportImg("top_bar.bmp").convert()
        self.rect = self.image.get_rect()
    def update(self,killcounter=None,health=None, nxtlvl=None):
        self.image.blit(self.healthbarimg,(0,0))
        if killcounter is not None and nxtlvl is not None:
            self.image.blit(MakeText(str(killcounter) + "/" + str(nxtlvl),40,(200,200,200)),(330,-3))
        if health is not None:
            self.image.blit(MakeText(str(health),40,(200,200,200)),(134,-3))

#Background which scrolls, so chilvers has some motion.
class Floor():
    def __init__(self, FloorImg):
        self.x = -1.5
        self.image = FloorImg
        self.loopimg = self.image
        self.counter = 0
    def update(self):
        self.counter += 1
        if self.counter == 3:
            self.loopimg = self.image
            self.loopimg.blit(self.image, (self.x,0))
            self.loopimg.blit(self.image, ((800+self.x),0))
            self.counter = 0

class BillGun(pygame.sprite.Sprite):
    def __init__(self,arm):
        pygame.sprite.Sprite.__init__(self)
        self.anims = []
        self.anims.append(ImportPNG("chilve_gun.png"))

        self.image = self.anims[0]
        self.rect = self.image.get_rect()

        self.armjoint = arm
        self.rect.left = self.armjoint[0] - 7
        self.rect.top = self.armjoint[1] - 8
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

    def turn(self):
        #Trigonometry time, fool!

        # Random Diagram ## # Another Diagram ###
        ################### #####################
        #       y         # #                   #
        #       |         # #  .m               #
        # +y -x | +y +x   # #  |                #
        #       |         # #  | j              #
        # ------+------ x # #  |                #
        #       |         # #  |       i        #
        # -y -x | -y +x   # #  -------------.s  #
        #       |         # #                   #
        ################### #####################

        self.rect.center = (self.x,self.y)

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        #position of mouse
        m_x = pygame.mouse.get_pos()[0]
        m_y = pygame.mouse.get_pos()[1]

        # centre of the gun
        s_x = self.x
        s_y = self.y

        i = float(m_x - s_x)
        # distance x
        j = float(m_y - s_y)
        # distance y

        try:
            angle = degrees(atan(j/i))
        except:
            angle = 0

        angle = -angle
        
        if i < 0 and j > 0:
            angle = angle + 180
        elif i < 0 and j < 0:
            angle = angle - 180

        self._rotate(angle)
        self.rect.center = self.BetterRotPoint( (self.rect.center) , (self.armjoint), (-angle) )
        
    def _rotate(self,angle):

        #Rotate the image, recalculate the rect
        self.image = pygame.transform.rotate(self.anims[0],angle)
        self.rect = self.image.get_rect()

        #Put it back in the old place.
        self.rect.center = (self.x,self.y)

    def _move(self, arm):
        self.image = self.anims[0]
        self.rect = self.image.get_rect()
        self.armjoint = arm
        self.rect.left = self.armjoint[0]-7
        self.rect.top = self.armjoint[1]-8
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.turn()

    def update(self):
        pass

    def BetterRotPoint(self, a , b, angle):
        #Function to rotate one point about another
        #This has proven that RotPoint works. Damn.

        # a = point
        # b = origin
        # angle is the angle of rotation
        
        angle = radians(angle)
        
        sinval = sin(angle) # Gets sine and cosine of the angle and keeps hold the it.
        cosval = cos(angle)

        x = a[0] - b[0] #Get the difference between
        y = a[1] - b[1] #the origin and the point

        nx = (x * cosval - y * sinval) + b[0] #Rotate the point.
        ny = (y * cosval + x * sinval) + b[1]

        nxy = (nx,ny)
        return nxy

    def RotPoint(self, point, axis, ang):
        #Function to generate a new centre. This is stolen from a person called altern.
        x = point[0] - axis[0]
        y = point[1] - axis[1]
        radius = sqrt(x*x + y*y)
        RAng = radians(ang)

        h = axis[0] + ( radius * cos(RAng) )
        v = axis[1] + ( radius * sin(RAng) )

        newpos = (h,v)
        return newpos
    
    def _set_coord(self):
        return

#Ye Billvaloth himself.
class Bill(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.health = 1000

        self.anim_idle = ImportImages("chilve_walk",6, 1)

        self.image = self.anim_idle[0]
        self.rect = self.image.get_rect()

        self.rect.bottom = 290
        
        self.mpos = (0,0)
        self.counter = 0
        self.limitcounter = 0
        self.state = "idle"

        self.yvel = 0

    def update(self):
        self.mpos = pygame.mouse.get_pos()

        self.rect.move_ip(0,self.yvel)

        if self.rect.bottom < 190:
            self.rect.bottom = 190
        if self.rect.bottom > 320:
            self.rect.bottom = 320

        if self.state == "idle":
            if self.limitcounter == 2:
                self.image = self.anim_idle[self.counter]
                if self.counter == 6:
                    self.counter = 0

                self.counter += 1
                
                self.limitcounter = 0

        self.limitcounter += 1

#I'm a chargin mah fireball!
class shot(pygame.sprite.Sprite):
    def __init__(self, pos, splode, fly):
        pygame.sprite.Sprite.__init__(self)

        self.image = fly[0]
        
        self.anim_splode = splode
        self.holder = (0,0)
        
        self.counter = 0
        self.limitcounter = 0
        self.state = ["fly", "alive"]
        
        self.target = pygame.mouse.get_pos()
        self.pos1 = pos

        #Does some trigonometry to find out where the shot is going
        #so that the x and y components can be obtained.

        self.dist = sqrt(pow((self.target[1]-self.pos1[1]),2) + \
                         pow((self.target[0]-self.pos1[0]),2) \
                         )
        self.angle = asin((self.target[0]-self.pos1[0])/self.dist)
        self.cangle = acos((self.target[0]-self.pos1[0])/self.dist)

        #Sets the total velocity and then finds its x and y components
        #using sine and cosine.
        
        self.resvel = 18

        #Selection statements make stuff go in the right directions (or put
        #the vector triangle the right way up, if you will). Probably not
        #done properly and so should be improved at some point.

        self.anim_fly = []
        
        if self.target[0]-self.pos1[0] > 0 or self.target[0]-self.pos1[0] == 0:
            self.xvel = self.resvel*sin(self.angle)
        elif self.target[0]-self.pos1[0] < 0:
            self.xvel = -(self.resvel*sin(self.angle))
        if self.target[1]-self.pos1[1] > 0 or self.target[1]-self.pos1[1] == 0:
            self.yvel = self.resvel*cos(self.angle)
        elif self.target[1]-self.pos1[1] < 0:
            self.yvel = -(self.resvel*cos(self.angle))
            self.cangle = -self.cangle

        for image in fly:
            self.anim_fly.append(pygame.transform.rotate(image,degrees(-self.cangle)))
        self.image = self.anim_fly[0]

        self.velfour = self.resvel+4
        self.rect = self.image.get_rect()

        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def update(self):

        #Main animation.
        if self.state[0] == "fly":
            if self.limitcounter == 1:
                self.rect.move_ip(self.xvel, self.yvel)
                #if self.counter == 0:
                    #self.counter = 0
                self.image = self.anim_fly[self.counter]
                #self.counter += 1
                
                self.limitcounter = 0

            #Determines if the missile impacts.
            if self.rect.center[1] <= self.target[1]+self.velfour \
               and self.rect.center[1] >= self.target[1]-self.velfour \
               and self.rect.center[0] <= self.target[0] + self.velfour \
               and self.rect.center[0] >= self.target[0] - self.velfour:
                self.destroy()

            #If it goes off screen, the missile is killed, keeping things
            #tidy.
            if self.rect.left > 800 \
               or self.rect.top > 320 \
               or self.rect.bottom < 0 \
               or self.rect.right < 0:
                self.kill()

        #Death Animation
        if self.state[0] == "splode":
            if self.limitcounter == 1:
                self.image = self.anim_splode[self.counter]
                self.counter += 1
                self.limitcounter = 0
                self.counter += 1
            if self.counter == 26:
                self.kill()

        #Limits the speed of the animation.        
        self.limitcounter += 1

    #Sets up the attributes so that the explosion works.
    def destroy(self):
        self.state[0] = "splode"
        self.counter = 0
        self.limitcounter = 0

#Awesomeness on a stick. Throws particles at things.
class GeneralEmitter():
    """Emits a sprite at a given angle, at a given velocity and with a given
        acceleration."""
    def __init__(self, resvel, angle, accel, anim, pos,
                 particle_controlling_array, anim2=None,
                 anim3=None):
        
        self.resvel = resvel
        self.angle = radians(angle)
        self.emits = anim

        self.xvel = self.resvel * sin(self.angle)
        self.yvel = -self.resvel * cos(self.angle)
        self.accel = accel

        self.pos = pos

        self.prtxvel = 0
        self.prtyvel = 0

        self.particle_controlling_array = particle_controlling_array

        self.counter = 0

        self.reinit()

    def reinit():
        pass

    def update(self):
        if self.counter == 4:
            self.xvel += self.accel[0]
            self.yvel += self.accel[1]
            self.pos = (self.pos[0] + self.xvel,self.pos[1] + self.yvel)
            for particle in self.particle_controlling_array:
                self.addparticle(particle[0],particle[1],particle[2])
            self.counter = 0
        self.counter += 1

        self.reupdate()

    def reupdate():
        pass

    def addparticle(self,resvel,angle,accel):
        self.prtxvel = resvel * sin(radians(angle))
        self.prtyvel = resvel * cos(radians(angle))
        particles.add(self.Particle(self.emits,self.prtxvel,
                               self.prtyvel,accel,1,
                               self.pos
                               )
                      )
        
    def destroy(self):
        self = None

    class Particle(pygame.sprite.Sprite):
        def __init__(self, anim, xvel, yvel, accel, maxplays, pos):
            pygame.sprite.Sprite.__init__(self)
            self.anim = anim
            self.image = self.anim[0]
            self.rect = self.image.get_rect()
            self.counter = 0
            self.limitcounter = 0
            self.xvel = xvel
            self.yvel = yvel
            self.animlim = len(self.anim)-1
            self.accel = accel
            self.maxplays = maxplays
            self.playcounter = 0
            self.rect.center = (pos[0],pos[1])
        def update(self):
            if self.limitcounter == 2:
                self.xvel += self.accel[0]
                self.yvel += self.accel[1]
                self.image = self.anim[self.counter]
                self.rect.move_ip(self.xvel,self.yvel)
                self.counter += 1
                if self.counter == self.animlim:
                    self.counter = 0
                    self.playcounter += 1
                if self.playcounter == self.maxplays:
                    self.kill()
                self.limitcounter = 0
            self.limitcounter += 1
        
#Plays music. You might have guessed.
class MusicPlayer():
    def __init__(self):
        #Holds a list of all of the music tracks.
        self.tracks = ["Voitel.mp3",
                       "Dragon.mp3",
                       "Tricycles.mp3",
                       "Svartberg End.mp3",
                       "odetojoy.ogg",
                       "otj2.ogg",
                       "ganon.ogg",]
        #Music is randomised.
        self.randomise = 4
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(self.tracks[self.randomise])
        pygame.mixer.music.play()

    def update(self):
        #Plays a random track if one is not playing already.
        if pygame.mixer.music.get_busy() == 0:
            pygame.mixer.music.load(self.tracks[self.randomise])
            pygame.mixer.music.play()
            #It only plays ode to joy at the moment.

#Main function. Woot!
def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF, NOFRAME)
    pygame.display.set_caption("Chilvers' Massacre Of The Lost Board Of Shareholders On Their Icy Planet Of Lolland")
    #screen.blit(ImportImg("splash.png"),(400-268,160-70))

    loader = pygame.Surface((800,320))
    loader.blit(ImportImg("holder.png"),(100,125))
    bar = ImportImg("bar.png")
    loader.blit(bar,(151,140))
    screen.blit(loader,(0,0))
    pygame.display.update()

    print "-- LOADING --"
    #Start the music
    player = MusicPlayer()
    
    #Floor scrolling
    print "//Loading Surfaces//"
    FloorImg = ImportImg("floor.bmp")
    TheFloor = Floor(FloorImg)

    loader.blit(bar,(201,140))
    screen.blit(loader,(0,0))
    pygame.display.update()
    
    #Sky and other main surfaces.
    background = pygame.Surface((800,320))
    background.fill((0, 0, 0))
    sky = ImportImg("sky.bmp").convert()
    background.blit(sky,(0,0))
    screen.blit(background, (0, 0))

    StatsBar = HealthBar()

    loader.blit(bar,(251,140))
    screen.blit(loader,(0,0))
    pygame.display.update()
    
    #Get Sounds
    print "//Loading Sounds//"
    LaserSound = LoadSound("gatling.wav")
    ZapSound = LoadSound("expll.wav")
    ZapSound.set_volume(0.2)
    Quake_Sounds = QuakeSounds()
    NarratorSounds = QuakeSounds("narrator",2)
    EighteenTwelve = LoadSound("1812.wav")
    EighteenTwelve.set_volume(1.0)

    channel1.play(NarratorSounds[0])

    #Counters / Controllers
    randomcounter = 0
    killcounter = 0
    
    isshooting = 0
    shotlim = 0
    
    ismessage = 0
    msgcounter = 0

    levelcap = 10
    level = 0

    billdead = 0
    spawning = 1

    loader.blit(bar,(301,140))
    screen.blit(loader,(0,0))
    pygame.display.update()

    #Strings and Text
    message = AnnouncerTexter("")
    LevelMsgs = ["FAIL","First Blood!","Multikill!",
                     "Ultrakill!","Whickedsick!","Ludicrouskill!",
                     "Monsterkill!","Godlike!"]
    OtherMsgs = ["RA RA RASPUTIN!"]

    loader.blit(bar,(351,140))
    screen.blit(loader,(0,0))
    pygame.display.update()
    
    # Anim
    print "//Loading Anim//"

    # ---
    # ----
    # -----
    
    # -- Shot
    Shot_fly = []
    Shot_fly.append(ImportPNG("shotp.png"))
    Shot_splode = ImportImages("shot_splode", 7, 1)
    # -- Cultists
    Cultists_Anim_Walk = ImportImages("cult_walk",3,1)
    Cultists_Anim_Death = ImportImages("cult_death",5,1)
    # -- Tanks
    Tank_Anim_Move = ImportImages("tank",2,1)
    Tank_Anim_Death = ImportImages("tank_splode_new",7,1)
    # -- Siege Assault Bots
    Bot_Anim_Shoot = ImportImages("SAB_shoot",7,-1)
    Bot_Anim_Proj_Fly = ImportPNG("SAB_Plasma_Fly_0.png")
    # -- Gatling Bots
    Gatling_Anim_Shoot = ImportImages("gatling_shoot",7,-1)
    # -- Rasputin
    Rasputin_Head = ImportImages("rasputin",1,1)

    # -- Bot Explosion (Could Have Many Uses)
    FX_Anim_Explosion= ImportImages("SAB_expl",26,-1)
    Fireball_Anim = ImportImages("8expl",6,-1)
    
    # -----
    # ----
    # ---

    for x in range(50,150,50): loader.blit(bar,(351 + x,140))
    screen.blit(loader,(0,0))
    pygame.display.update()

    print "//Initialising//"

    #Mighty chilvers
    bill = Bill()
    billgun = BillGun((bill.rect.left+8,bill.rect.top+38))

    #Sprite groups
    global chilve_sprite
    chilve_sprite = pygame.sprite.RenderClear([bill,billgun])
    global laser_sprite
    laser_sprite = pygame.sprite.RenderClear()
    global flan_sprites
    flan_sprites = pygame.sprite.OrderedUpdates()
    test_group = pygame.sprite.OrderedUpdates()
    fireball = None

    # Make an all thing. Not used at the moment.
    all = pygame.sprite.RenderUpdates()

    # Make a clock
    clock = pygame.time.Clock()

    #Update the stats bar
    StatsBar.update(killcounter,bill.health)

    for x in range(50,200,50):loader.blit(bar,(451 + x,140))
    screen.blit(loader,(0,0))
    pygame.display.update()

    bar = None
    loader = None

    #Take a short break
    pygame.time.wait(1600)

    #####################
    #######################
    #########################
    #\TESTING AREA#############
    #############################

    #What the emitter needs.
    #self, resvel, angle, accel, anim, pos, particle_controlling_array, anim2=None, anim3=None

    #emitters.append(GeneralEmitter(2,0,(0,0),FX_Anim_Explosion,(200,200),[[10,270,(0,0)],[10,90,(0,0)]]))

    #############################
    #/TESTING AREA#############
    #########################
    #######################
    #####################

    #Game Loop
    
    while 1:

        #Handles input
        for event in pygame.event.get():
            if event.type == QUIT   \
               or (event.type == KEYDOWN and    \
                   event.key == K_ESCAPE):
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.mixer.quit()
                pygame.font.quit()
                return
            if billdead == 0:
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        bill.yvel = -4
                    elif event.key == K_s:
                        bill.yvel = 4
                if event.type == KEYUP:
                    if event.key == K_w:
                        bill.yvel = 0
                    if event.key == K_s:
                        bill.yvel = 0
                        
        if billdead == 0:

            isshooting = pygame.mouse.get_pressed()[0]
            #Shoots for Bill             
            if isshooting:
                if shotlim == 2:
                    laser_sprite.add(shot((billgun.rect.right,billgun.rect.center[1]),FX_Anim_Explosion, Shot_fly))
                    LaserSound.play()
                    shotlim = 0
                shotlim += 1

            #Detects hits
            for sprite in laser_sprite:
                for dude in flan_sprites:
                    if sprite.rect.center[1] > dude.hitbox[2]  \
                       and sprite.rect.center[1] < dude.hitbox[3] \
                       and sprite.rect.center[0] < dude.hitbox[1] \
                       and sprite.rect.center[0] > dude.hitbox[0] \
                       and dude.state != "dead":

                        #Explosions
                        sprite.kill()
                        dude.destroy()
                        ZapSound.play()
                        killcounter += 1

            #Quake & Kills
            if killcounter > levelcap:
                levelcap = levelcap + 12 + int(0.1*levelcap)
                level += 1
                try:
                    channel1.play(Quake_Sounds[level-1])
                except:
                    print "No sound"
                try:
                    message = AnnouncerTexter(LevelMsgs[level])
                except:
                    message = AnnouncerTexter("Impressive.")
                ismessage = 1

                if level == 8:
                    spawning = 0
                    flan_sprites.add(enemies.RaRaRasputin(Rasputin_Head))
                    level = 9
                    pygame.mixer.music.stop()
                    player.randomise = 6
                    message =  AnnouncerTexter(OtherMsgs[0])

        #Blits the surfaces.
        screen.blit(background, (0,0))
        screen.blit(TheFloor.loopimg,(0,157))

        #Adds enemies
        if spawning == 1:
            randomcounter = random.randrange(0,40)
            if randomcounter == 15:
                flan_sprites.add(enemies.Cultists(Cultists_Anim_Walk,Cultists_Anim_Death))
            if randomcounter == 16:
                flan_sprites.add(enemies.CultTank(Tank_Anim_Move, Tank_Anim_Death))
            if randomcounter == 12:
                flan_sprites.add(enemies.SAB(Bot_Anim_Shoot))
            if randomcounter == 11:
                flan_sprites.add(enemies.Gatling(Gatling_Anim_Shoot))

                #The amazing sorting algorithm
                spriteholder = []
                y = 200
                while y <= 320:
                    for sprite in flan_sprites:
                        if sprite.rect.bottom == y:
                            spriteholder.append(sprite)
                    y += 20
                flan_sprites.empty()
                for sprite in spriteholder:
                    flan_sprites.add(sprite)

            #Fire!
            for sprite in flan_sprites:
                if sprite.rect.right < 75:
                    sprite.kill()
                if sprite.shot != 0:
                    if sprite.shot == 1:
                        shoty = sprite.rect.top + sprite.gun[0]
                    try:
                        if sprite.shot == 2:
                            shoty = sprite.rect.top + sprite.gun[1]
                    except:
                        pass

                    shotx = sprite.rect.left + sprite.gunmodifier

                    incoming.add(projectiles.SAB_Plasma(shotx,shoty,Bot_Anim_Proj_Fly))

            #Shots hit bill
            for sprite in incoming:
                if sprite.rect.left < 60 \
                   and sprite.rect.top > bill.rect.top \
                   and sprite.rect.bottom < bill.rect.bottom:
                    sprite.kill()
                    bill.health -= 1

            if bill.health <= 0:
                bill.health = 1
                bill.kill()
                billdead = 1
                TheFloor.x = 0
                ismessage = 1
                msgcounter = 0
                spawning = 0
                pygame.mixer.music.stop()
                message =  AnnouncerTexter(LevelMsgs[0])
                channel1.play(NarratorSounds[1])
                EighteenTwelve.play()

        #Updates
        TheFloor.update()
        if billdead == 0:
            chilve_sprite.update()
            billgun._move((bill.rect.left+24,bill.rect.top+38))
            StatsBar.update(killcounter, bill.health, int(levelcap))
            player.update()
        flan_sprites.update()
        laser_sprite.update()
        particles.update()
        incoming.update()
        if emitters is not None:
            for emitter in emitters:
                emitter.update()

        #Draw
        if billdead == 0:
            chilve_sprite.draw(screen)
        flan_sprites.draw(screen)
        laser_sprite.draw(screen)
        incoming.draw(screen)
        fireball_sprites.draw(screen)
        particles.draw(screen)
        if billdead == 0:
            screen.blit(StatsBar.image,(0,0))

        #Add superimposed.
        if ismessage == 1:
            screen.blit(message,
                        (screen.get_width()/2 - message.get_width()/2,
                         screen.get_height()/2 - message.get_height()/2))
            msgcounter += 1
            if msgcounter > 75:
                ismessage = 0
                msgcounter = 0

        #Update
        pygame.display.update()
        pygame.time.wait(10)
        bill.health += 1

        # maintain frame rate
        clock.tick(35)

if __name__ == '__main__': main()
