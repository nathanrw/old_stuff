#The Amazing Chilvers Game
#Main file

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
channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)

#Some Constants
global incoming
incoming = pygame.sprite.OrderedUpdates()

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

class Bill(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.health = 1000000

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

class shot(pygame.sprite.Sprite):
    def __init__(self, pos, splode, fly):
        pygame.sprite.Sprite.__init__(self)
        
        self.anim_fly = fly
        self.image = self.anim_fly[0]
        self.rect = self.image.get_rect()
        self.anim_splode = splode
        self.holder = (0,0)
        
        self.counter = 0
        self.limitcounter = 0
        self.state = ["fly", "alive"]
        
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        
        self.target = pygame.mouse.get_pos()
        self.pos1 = pos

        #Does some trigonometry to find out where the shot is going
        #so that the x and y components can be obtained.

        self.dist = sqrt(pow((self.target[1]-self.pos1[1]),2) + \
                         pow((self.target[0]-self.pos1[0]),2) \
                         )
        self.angle = asin((self.target[0]-self.pos1[0])/self.dist)

        #Sets the total velocity and then finds its x and y components
        #using sine and cosine.
        
        self.resvel = 18

        #Selection statements make stuff go in the right directions (or put
        #the vector triangle the right way up, if you will)
        
        if self.target[0]-self.pos1[0] > 0 or self.target[0]-self.pos1[0] == 0:
            self.xvel = self.resvel*sin(self.angle)
        elif self.target[0]-self.pos1[0] < 0:
            self.xvel = -(self.resvel*sin(self.angle))
        if self.target[1]-self.pos1[1] > 0 or self.target[1]-self.pos1[1] == 0:
            self.yvel = self.resvel*cos(self.angle)
        elif self.target[1]-self.pos1[1] < 0:
            self.yvel = -(self.resvel*cos(self.angle))

    def update(self):

        #Main animation.
        if self.state[0] == "fly":
            if self.limitcounter == 1:
                self.rect.move_ip(self.xvel, self.yvel)
                if self.counter == 2:
                    self.counter = 0
                self.image = self.anim_fly[self.counter]
                self.counter += 1
                
                self.limitcounter = 0

        #Death animation
        elif self.state[0] == "splode":
            self.counter == 0
            if self.limitcounter == 3:
                if self.counter == 7:
                    self.kill()
                self.image = self.anim_splode[self.counter]
                self.counter += 1
                
                self.limitcounter = 0

        #Limits the speed of the animation.        
        self.limitcounter += 1

        #Determines if the missile impacts.
        self.velfour = self.resvel+4
        if self.rect.center[1] <= self.target[1]+self.velfour \
           and self.rect.center[1] >= self.target[1]-self.velfour \
           and self.rect.center[0] <= self.target[0] + self.velfour \
           and self.rect.center[0] >= self.target[0] - self.velfour:
            self.destroy()

        #If it goes off screen, the missile is killed, keeping things
        #tidy.
        if self.rect.left > 800 or self.rect.top > 320 or self.rect.bottom < 0 or self.rect.right < 0:
            self.kill()

    #Sets up the attributes so that the explosion works.
    def destroy(self):
        self.state[0] = "splode"
        self.holder = [self.rect.center,self.rect.bottom]
        self.image = self.anim_splode[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.holder[0]
        self.rect.bottom = self.holder[1]
        self.counter = 0
        self.limitcounter = 0

class MusicPlayer():
    def __init__(self):
        #Holds a list of all of the music tracks.
        self.tracks = ["Voitel.mp3",
                       "Dragon.mp3",
                       "Tricycles.mp3",
                       "Svartberg End.mp3"]
        #Music is randomised.
        self.randomise = 3
        self.playing = 0
        pygame.mixer.music.set_volume(0.7)

    def update(self):
        #Plays a random track if one is not playing already.
        if pygame.mixer.music.get_busy() == 0:
            self.randomise = 3
            pygame.mixer.music.load(self.tracks[self.randomise])
            pygame.mixer.music.play()

def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF)
    pygame.display.set_caption("Chilvers' Massacre Of The Lost Board Of Shareholders On Their Icy Planet Of Lolland")
    screen.blit(ImportImg("splash.png"),(400-268,160-70))
    pygame.display.update()

    print "-- LOADING --"
    #Start the music
    player = MusicPlayer()
    
    #Floor scrolling
    print "//Loading Surfaces//"
    FloorImg = ImportImg("floor.bmp")
    TheFloor = Floor(FloorImg)
    
    #Sky and other main surfaces.
    background = pygame.Surface((800,320))
    background.fill((0, 0, 0))
    sky = ImportImg("sky.bmp").convert()
    background.blit(sky,(0,0))
    screen.blit(background, (0, 0))

    StatsBar = HealthBar()
    
    #Get Sounds
    print "//Loading Sounds//"
    LaserSound = LoadSound("ChilveLaser.wav")
    ZapSound = LoadSound("zap.wav")
    Quake_Sounds = QuakeSounds()

    #Counters / Controllers
    randomcounter = 0
    killcounter = 0
    
    isshooting = 0
    shotlim = 0
    
    ismessage = 0
    msgcounter = 0

    levelcap = 10
    level = 0

    #Strings and Text
    message = AnnouncerTexter("")
    LevelMsgs = ["CHILVEEERRRS","First Blood!","Multikill!",
                     "Ultrakill!","Whickedsick!","Ludicrouskill!",
                     "Monsterkill!","Godlike!"]
    
    # Anim
    print "//Loading Anim//"

    # ---
    # ----
    # -----
    
    # -- Shot
    Shot_fly = ImportImages("shotf",2,1)
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
    
    # -----
    # ----
    # ---

    print "//Initialising//"

    #Mighty chilvers
    bill = Bill()

    #Sprite groups
    chilve_sprite = pygame.sprite.RenderClear(bill)
    laser_sprite = pygame.sprite.RenderClear()
    flan_sprites = pygame.sprite.OrderedUpdates()
    test_group = pygame.sprite.OrderedUpdates()

    # Make an all thing. Not used at the moment.
    all = pygame.sprite.RenderUpdates()

    # Make a clock
    clock = pygame.time.Clock()

    #Update the stats bar
    StatsBar.update(killcounter,bill.health)

    #Take a short break
    pygame.time.wait(1200)

    #Game loop
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
            if event.type == MOUSEBUTTONDOWN:
                isshooting = 1
            if event.type == MOUSEBUTTONUP:
                isshooting = 0

            #Shoots for Bill 
            shotlim += 1
            if shotlim == 4:
                if isshooting == 1:
                    laser_sprite.add(shot((90,bill.rect.top+70),Shot_splode, Shot_fly))
                    LaserSound.play()
                shotlim = 0

        #Detects hits
        for sprite in laser_sprite:
            for dude in flan_sprites:
                if sprite.rect.center[1] > dude.hitbox[2]  \
                   and sprite.rect.center[1] < dude.hitbox[3] \
                   and sprite.rect.center[0] < dude.hitbox[1] \
                   and sprite.rect.center[0] > dude.hitbox[0] \
                   and dude.state == "idle":

                    #Explosions
                    sprite.destroy()
                    dude.destroy()
                    ZapSound.play()
                    killcounter += 1

        #Quake & Kills
        if killcounter > levelcap:
            levelcap = levelcap + 50 + int(0.1*levelcap)
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

        #Blits the surfaces.
        screen.blit(background, (0,0))
        screen.blit(TheFloor.loopimg,(0,157))

        #Adds enemies
        randomcounter = random.randrange(0,40)
        if randomcounter == 12 or randomcounter == 15 or randomcounter == 16:
            #if randomcounter == 15:
                #flan_sprites.add(enemies.Cultists(Cultists_Anim_Walk,Cultists_Anim_Death))
            #elif randomcounter == 16:
                #flan_sprites.add(enemies.CultTank(Tank_Anim_Move, Tank_Anim_Death))
            if randomcounter == 12:
                flan_sprites.add(enemies.SAB(Bot_Anim_Shoot))

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
            if sprite.shot == 1 or sprite.shot == 2:
                if sprite.shot == 1:
                    shoty = sprite.rect.top + 29
                elif sprite.shot == 2:
                    shoty = sprite.rect.top + 24

                shotx = sprite.rect.left

                incoming.add(projectiles.SAB_Plasma(shotx,shoty,Bot_Anim_Proj_Fly))

        #Shots hit bill
        for sprite in incoming:
            if sprite.rect.left < 60 \
               and sprite.rect.top > bill.rect.top \
               and sprite.rect.bottom < bill.rect.bottom:
                sprite.kill()
                bill.health -= 1

        #Updates
        TheFloor.update()
        player.update()
        chilve_sprite.update()
        flan_sprites.update()
        laser_sprite.update()
        StatsBar.update(killcounter, bill.health, int(levelcap))
        incoming.update()

        #Draw
        chilve_sprite.draw(screen)
        flan_sprites.draw(screen)
        laser_sprite.draw(screen)
        incoming.draw(screen)
        screen.blit(StatsBar.image,(0,0))

        #Add superimposed.
        if ismessage == 1:
            screen.blit(message[msgcounter],
                        (screen.get_width()/2 - message[0].get_width()/2,
                         screen.get_height()/2 - message[0].get_height()/2))
            msgcounter += 1
            if msgcounter > 24:
                ismessage = 0
                msgcounter = 0

        #Update
        pygame.display.update()
        pygame.time.wait(10)

        # maintain frame rate
        clock.tick(28)

if __name__ == '__main__': main()
