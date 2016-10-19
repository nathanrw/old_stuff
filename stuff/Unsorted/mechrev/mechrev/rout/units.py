import pygame
import random
import math
from menu import menu as mnu
pygame.font.init()
fnt = pygame.font.SysFont("Verdana",20)

si = 32

def gs(col):
    """Make tile that's that color"""
    s = pygame.Surface([si,si])
    s.fill(col)
    return s

class fakesound:
    def __init__(self):
        pass
    def play(self):
        pass
    def stop(self):
        pass
def loadsound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print "fakesounds"
        return fakesound()

sndgun = loadsound("snd/machinegun.ogg")
sndsword=loadsound("snd/blade.ogg")
sndrocket=loadsound("snd/rocket_sound.ogg")
marchsound=loadsound("snd/march.ogg")
#foot=loadsound("../snd/footsteps.ogg")
#foot.play()

robimg = pygame.image.load("gfx/robot.png")
erobimg = pygame.image.load("gfx/erobot.png")
robframes = [robimg.subsurface([[x,0],[32,32]]) for x in [0,32,64,96,128,160]]
erobframes = [erobimg.subsurface([[x,0],[32,32]]) for x in [0,32,64,96,128,160]]
robframes.extend([pygame.transform.flip(robframes[4],1,0),pygame.transform.flip(robframes[5],1,0)])
erobframes.extend([pygame.transform.flip(erobframes[4],1,0),pygame.transform.flip(erobframes[5],1,0)])
robattackimg = pygame.image.load("gfx/robotattack.png")
robattackframes = [robattackimg.subsurface([[x,0],[160,robattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]
erobattackimg = pygame.image.load("gfx/erobotattack.png")
erobattackframes = [erobattackimg.subsurface([[x,0],[160,erobattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]

pwrgen = pygame.image.load("gfx/powergenerator.png")
pwrframes = [pwrgen.subsurface([[x,0],[32,32]]) for x in [0,32,64,96]]
pwrframes.extend([pygame.transform.flip(pwrframes[3],1,0),pygame.transform.flip(pwrframes[2],1,0),pygame.transform.flip(pwrframes[1],1,0)])

doorimg = pygame.image.load("gfx/door.png")
doorimgrot = pygame.transform.rotate(doorimg,90)

fmimg = pygame.image.load("gfx/footman.png")
efmimg = pygame.image.load("gfx/efootman.png")
fmframes = [fmimg.subsurface([[x*32,0],[32,32]]) for x in range(10)]
efmframes = [efmimg.subsurface([[x*32,0],[32,32]]) for x in range(10)]
fmframes.reverse()
efmframes.reverse()
fmattackimg = pygame.image.load("gfx/footmanattack.png")
fmattackframes = [fmattackimg.subsurface([[x,0],[160,fmattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]
efmattackimg = pygame.image.load("gfx/efootmanattack.png")
efmattackframes = [efmattackimg.subsurface([[x,0],[160,efmattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]


mhimg = pygame.image.load("gfx/mainhero.png")
mhframes = [mhimg.subsurface([[x,0],[32,32]]) for x in [0,32,64,96,128,160]]
mhframes.extend([pygame.transform.flip(mhframes[4],1,0),pygame.transform.flip(mhframes[5],1,0)])
mhattackimg = pygame.image.load("gfx/mainheroattack.png")
mhattackframes = [mhattackimg.subsurface([[x,0],[160,mhattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]

bdimg = pygame.image.load("gfx/boss.png")
bdframes = [bdimg.subsurface([[x,0],[32,32]]) for x in [0,32,64,96,128,160]]
bdframes.extend([pygame.transform.flip(bdframes[4],1,0),pygame.transform.flip(bdframes[5],1,0)])
bdattackimg = pygame.image.load("gfx/bossattack.png")
bdattackframes = [bdattackimg.subsurface([[x,0],[160,bdattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]

ebimg = pygame.image.load("gfx/endboss.png")
ebframes = [ebimg.subsurface([[x,0],[32,32]]) for x in [0,32,64,96,128,160]]
ebframes.extend([pygame.transform.flip(ebframes[4],1,0),pygame.transform.flip(ebframes[5],1,0)])
ebattackimg = pygame.image.load("gfx/endbossattack.png")
ebattackframes = [ebattackimg.subsurface([[x,0],[160,ebattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]

grampsimg = pygame.image.load("gfx/gramps.png")
grampsimg.set_colorkey([255,255,255])
grampsattackimg = pygame.image.load("gfx/grampsattack.png")
grampsattackframes = [grampsattackimg.subsurface([[x,0],[160,grampsattackimg.get_size()[1]]]) for x in [0,160,320,480,640,820]]

rlimg = pygame.image.load("gfx/rocketlauncher.png")
erlimg = pygame.image.load("gfx/erocketlauncher.png")
rlatkimg = pygame.image.load("gfx/rocketlauncherattack.png")
rlattackframes = [rlatkimg.subsurface([[x,0],[160,rlatkimg.get_size()[1]]]) for x in [0,160]]

rocket = pygame.image.load("gfx/rocket.png")
rocket.set_colorkey([255,255,255])
rocketflip = pygame.transform.flip(rocket,0,1)
explosion = pygame.image.load("gfx/explosion.png")
explosion.set_colorkey([255,255,255])

def ld(name):
    img = pygame.image.load("gfx/"+name+".png")
    img.set_colorkey([255,255,255])
    return img
bcktiles = {"crates":ld("cratesbackbattle"),"bridge":ld("bridgebackbattle"),"town":ld("townbackbattle"),"floor":ld("floorbackbattle"),"grass":ld("grassbackbattle"),"forest":ld("forestbackbattle"),"mountain":ld("mountainbackbattle")}
frnttiles = {"crates":ld("cratesfrontbattle"),"bridge":ld("bridgefrontbattle"),"town":ld("townfrontbattle"),"floor":ld("floorfrontbattle"),"grass":ld("grassfrontbattle"),"forest":ld("forestfrontbattle"),"mountain":ld("mountainfrontbattle")}

class attack:
    def __init__(self,name,mode="close",shape="cross",range=1,power=1,distmod=0,powerused=0):
        self.name = name
        self.mode = mode
        self.shape = shape
        self.range = range
        self.power = power
        self.distmod = distmod
        self.powerused = powerused
    def inrange(self,map,pos):
        tiles = []
        def valid(pos):
            if pos[0]>=0 and pos[0]<len(map[0]) and pos[1]>=0 and pos[1]<len(map):
                return True
            return False
        if self.shape == "cross":
            y = pos[1]
            for x in range(pos[0]-self.range,pos[0]+self.range+1):
                if x!=pos[0] and x>=0 and x<len(map[0]):
                    tiles.append([x,y])
            x = pos[0]
            for y in range(pos[1]-self.range,pos[1]+self.range+1):
                if y!=pos[1] and y>=0 and y<len(map):
                    tiles.append([x,y])
        if self.shape == "diamond":
            for i in range(1,self.range+1):
                yoff=0
                for x in range(pos[0]-i,pos[0]+1):
                    t1 = [x,pos[1]+yoff]
                    t2 = [x,pos[1]-yoff]
                    if valid(t1):
                        tiles.append(t1)
                    if valid(t2):
                        tiles.append(t2)
                    yoff+=1
                yoff=i
                for x in range(pos[0],pos[0]+i+1):
                    t1 = [x,pos[1]+yoff]
                    t2 = [x,pos[1]-yoff]
                    if valid(t1):
                        tiles.append(t1)
                    if valid(t2):
                        tiles.append(t2)
                    yoff-=1
        units = []
        for p in tiles:
            u = map[p[1]][p[0]].unit
            if u:
                units.append(u)
        return units
    def frames(self):
        return {"sword":[4,5],"guns":[0,1],"missile volley":[0,0],"missile volley+1":[0,1]}[self.name]
        
data = {"sword":attack("sword","close","cross",1,4,0,1),
    "guns":attack("guns","ranged","cross",2,5,1,2),
    "missiles":attack("missile volley","ranged","diamond",3,6,0,5),
    "missiles2":attack("missile volley+1","ranged","diamond",30,9,0,8),
    "missiles3":attack("missile volley+1","ranged","diamond",4,8,0,3)}
data["missiles2"].killer=1
data["missiles3"].killer=1

def getdef(u,atk):
    if u.type in ["robot","mainhero","branden"]:
        if atk.name=="sword":
            return 1
        if atk.name=="guns":
            return 4
        if atk.name=="missile volley":
            return 2
    if u.type=="footman":
        if atk.name=="sword":
            return 2
        if atk.name=="guns":
            return 1
        if atk.name=="missile volley":
            return 0
    if u.type=="power":
        return 5
    #print "no match for:",u.type,"vs",atk.name
    return 0
    

class unit(object):
    def __init__(self,type,map,pos=[0,0],side="enemy"):
        self.type = type
        self.side = side
        self.cost=None
        self.pos = pos
        self.map = map
        if type=="robot":
            self.frames = {"player":robframes,"enemy":erobframes}[side]
            self.surf = self.frames[random.choice([0,2,4,6])]
            self.speed = 3
            self.attacks = [data["sword"],data["guns"]]
            self.maxhealth = 15
            if side=="enemy":
                self.maxpower = 200
            else:
                self.maxpower=10
            self.attackframes = {"player":robattackframes,"enemy":erobattackframes}[side]
        elif type=="power":
            self.surf = pwrframes[0]
            self.topframe = pwrframes[1]
            self.speed = 0
            self.attacks=[]
            self.maxhealth = 5
            self.range = 3
            self.side = "none"
        elif type=="door":
            self.surf=doorimg
            self.speed=0
            self.attacks=[]
            self.maxhealth=8
            self.side="none"
        elif type=="footman":
            self.maxhealth = 10
            self.fmframes = {"player":fmframes,"enemy":efmframes}[side]
            self.surf = self.fmframes[self.health-1]
            self.attacks=[attack("guns","ranged","cross",2,2,1)]
            self.attackframes = {"player":fmattackframes,"enemy":efmattackframes}[side]
        elif type=="mainhero":
            self.frames = mhframes
            self.surf = self.frames[random.choice([0,2,4,6])]
            self.speed = 4
            self.attacks = [data["sword"],data["guns"],data["missiles"]]
            self.maxhealth = 20
            self.maxpower = 15
            self.attackframes = mhattackframes
        elif type=="branden":
            self.frames = bdframes
            self.surf = self.frames[random.choice([0,2,4,6])]
            self.speed = 4
            self.attacks = [data["sword"],data["guns"],data["missiles"]]
            self.maxhealth = 20
            self.maxpower = 200
            self.attackframes = bdattackframes
        elif type=="endboss":
            self.frames = ebframes
            self.surf = self.frames[random.choice([0,2,4,6])]
            self.speed = 1
            self.attacks = [data["missiles3"]]
            self.maxhealth = 25
            self.maxpower = 3
            self.attackframes = ebattackframes
        elif type=="gramps":
            self.side = "none"
            self.surf = grampsimg
            self.speed = 3
            self.attacks = []
            self.maxhealth = 2
            self.attackframes = grampsattackframes
            self.tag="gramps"
        elif type=="rocketlauncher":
            self.surf = {"player":rlimg,"enemy":erlimg}[side]
            self.attacks=[data["missiles2"]]
            self.maxhealth = 3
            self.maxpower=8
            self.power=0
            self.speed=0
            self.attackframes = rlattackframes
        
        self.path = None
        def stay(u=self):
            u.map.map[u.pos[1]][u.pos[0]].unit = None
            u.pos = [int(u.tpos[0]/32),int(u.tpos[1]/32)]
            u.map.map[u.pos[1]][u.pos[0]].unit = u
            u.moved=1
        self.deffunc=stay
        self.endpathfunc = stay
        
        self.attacked = 0
        self.moved = 0
        self.finished = 0
        
        self.atime = 0
        
        self.attackchosen = None
    def __setattr__(self,attr,val):
        if attr=="map":
            if hasattr(val,"si"):
                self.tpos = [self.pos[0]*val.si,self.pos[1]*val.si]
        if attr=="maxpower":
            self.__dict__["power"]=val
        if attr=="maxhealth":
            self.__dict__["health"]=val
        self.__dict__[attr]=val
    def __getattr__(self,attr):
        if attr=="speed" and self.type=="footman":
            if self.health>5:
                return 2
            return 3
        return self.__dict__[attr]
    def ps(self):
        if hasattr(self,"power"):
            return str(self.power)+"/"+str(self.maxpower)
        return "N/A"
    def canmove(self):
        #if hasattr(self,"power") and self.power == 0:
        #   return False
        if self.moved:
            return False
        return True
    def resetstate(self):
        self.attacked=0
        self.moved=0
        self.finished=0
    def nextturn(self):
        if hasattr(self,"power") and self.power>=0:
            getpower = 0
            import math
            if self.attacked==1:
                #print "*attacked"
                getpower=-1
            else:
                if self.map.gettile(self.pos).terrain in ["floor","crates"]:
                    #print "*on floor"
                    getpower=1
                if not getpower:
                    for pwr in [x for x in self.map.getunits() if x.type=="power"]:
                        d = int(math.sqrt((pwr.pos[0]-self.pos[0])**2+(pwr.pos[1]-self.pos[1])**2))
                        if d<=pwr.range:
                            #print "*near power"
                            getpower = 1
                            break
            #if getpower==-1 and self.power>0:
            #   self.power-=1
            #   pygame.messages.append(["Power -1",[self.tpos[0],self.tpos[1]],-1,[self.tpos[0],self.tpos[1]],[255,0,0]])
            #print "getpower=",getpower
            if getpower==1 and self.power<self.maxpower:
                self.power+=3
                #message,currentpos,direction,startpos,color
                pygame.messages.append(["Power +3",[self.tpos[0],self.tpos[1]],-1,[self.tpos[0],self.tpos[1]],[0,255,0]])
            elif getpower!=-1 and self.power<self.maxpower:
                self.power+=1
                pygame.messages.append(["Power +1",[self.tpos[0],self.tpos[1]],-1,[self.tpos[0],self.tpos[1]],[0,255,0]])
    def attack(self,o):
        animlength = 60
        if self.type=="footman":
            self.attacks[0].power=self.health/2
            if self.attacks[0].power==0:
                self.attacks[0].power=1
        surf = pygame.display.get_surface()
        fade = pygame.Surface([640,480])
        fade.fill([0,0,0])
        fade.set_alpha(100)
        surf.blit(fade,[0,0])
        os = surf.copy()
        a = self.attacks[self.attackchosen]
        if a.powerused and hasattr(self,"power") and self.power>0:
            pygame.messages.append(["Power -"+str(a.powerused),[self.tpos[0],self.tpos[1]],-1,[self.tpos[0],self.tpos[1]],[255,0,0]])
            self.power-=a.powerused
            if self.power<0:
                self.power = 0
        import math
        d = math.sqrt((o.pos[0]-self.pos[0])**2+(o.pos[1]-self.pos[1])**2)
        dmg=None
        fronttile = self.map.map[self.pos[1]][self.pos[0]].terrain
        backtile = self.map.map[o.pos[1]][o.pos[0]].terrain
        frontimg = frnttiles[fronttile].convert()
        dpos = [126,81]
        apos = [396,249]
        if backtile=="mountain":
            dpos[1]-=50
        if fronttile=="mountain":
            apos[1]-=50
        if hasattr(self,"attackframes"):
            frontimg.blit(self.attackframes[a.frames()[0]],apos)
        backimg = bcktiles[backtile].convert()
        if hasattr(o,"attackframes"):
            backimg.blit(o.attackframes[2],dpos)
        bckx = 640
        frntx = -640
        pygame.event.clear()
        while bckx>=0:
            surf.blit(os,[0,0])
            surf.blit(backimg,[bckx,0])
            surf.blit(frontimg,[frntx,0])
            pygame.theclock.tick(60)
            pygame.display.update()
            bckx-=10
            frntx+=10
            pygame.event.poll()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.event.clear()
                while 1:
                    pygame.event.poll()
                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        break
            
        hp = None
        hppos = None
        frontimg = frnttiles[fronttile].convert()
        backimg = bcktiles[backtile].convert()
        xd=yd=0
        missilesup = []
        missilesdown = []
        myd = 300/15
        myu = 600/15
        if a.mode=="close":
            xd = (apos[0]-dpos[0]-80)/25
            yd = (apos[1]-dpos[1]-60)/25
        elif a.mode=="ranged":
            xd = 30/25
            yd=15/25
        atksound=0
        i=0.0
        while i<90:
            dt = pygame.theclock.tick(60)/30.0
            i+=dt
            pygame.event.poll()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.event.clear()
                while 1:
                    pygame.event.poll()
                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        break
            if i>34 and not hppos:
                if dmg==None:
                    dmg = o.hit(self,d)
                if dmg<=0:
                    dmg="miss!"
                hp = fnt.render(str(dmg),1,[255,0,0])
                hppos = [130,200]
            surf.blit(os,[0,0])
            surf.blit(backimg,[0,0])
            if hasattr(o,"attackframes"):
                #Draw back guy
                if i<34:
                    surf.blit(o.attackframes[2],dpos)
                else:
                    surf.blit(o.attackframes[3],dpos)
                if i>=34 and i<=60:
                    dpos[0]-=1.0*dt
                    dpos[1]-=1.0*dt
                if i>60 and i<80:
                    dpos[1]+=1.0*dt
            for m in missilesdown:
                surf.blit(m[0],[m[1],m[2]])
                if m[0]!=explosion:
                    m[2]+=myd
                    if m[2]>m[3]:
                        m[0]=explosion
            if hp:
                surf.blit(hp,hppos)
                hppos[1]+=(i-38)*.8
            surf.blit(frontimg,[0,0])
            if hasattr(self,"attackframes"):
                #draw front guy
                if i<30:
                    surf.blit(self.attackframes[a.frames()[0]],apos)
                    if i<25:
                        apos[0]-=xd*dt
                        apos[1]-=yd*dt
                if i>=30 and i<40:
                    if a.name=="guns" and atksound==0:
                        atksound=1
                        sndgun.play()
                    if a.name=="sword" and atksound==0:
                        atksound=1
                        sndsword.play()
                    surf.blit(self.attackframes[a.frames()[1]],apos)
                    if i<35:
                        apos[0]-=1*dt
                        apos[1]-=1*dt
                    else:
                        apos[0]+=1*dt
                        apos[1]+=1*dt
                if i>=40:
                    surf.blit(self.attackframes[0],apos)
            if i>=30 and i<40:
                if a.name=="missile volley":
                    sndrocket.play()
                    missilesup.append([rocket,random.randint(int(apos[0]),int(apos[0])+100),random.randint(int(apos[1])-30,int(apos[1]))])
                if a.name=="missile volley+1":
                    sndrocket.play()
                    for i in range(5):
                        missilesup.append([rocket,random.randint(int(apos[0]),int(apos[0])+100),random.randint(int(apos[1])-30,int(apos[1]))])
            newmup = []
            for m in missilesup:
                surf.blit(m[0],[m[1],m[2]])
                m[2]-=myu*dt
                if m[2]<0:
                    missilesdown.append([rocketflip,random.randint(100,270),random.randint(-50,-20),random.randint(int(dpos[0])+20,int(dpos[0])+100)])
                else:
                    newmup.append(m)
            missilesup = newmup
            self.stats([400,10])
            o.stats([10,350])
            pygame.display.update()
        if hasattr(self,"frames"):
            if o.pos[0]<self.pos[0]:
                if self.surf not in self.lframes():
                    self.surf = self.lframes()[0]
            if o.pos[0]>self.pos[0]:
                if self.surf not in self.rframes():
                    self.surf = self.rframes()[0]
            if o.pos[1]<self.pos[1]:
                if self.surf not in self.uframes():
                    self.surf = self.uframes()[0]
            if o.pos[1]>self.pos[1]:
                if self.surf not in self.dframes():
                    self.surf = self.dframes()[0]
    def hit(self,u,dist=1):
        atk=u.attacks[u.attackchosen]
        p = int(atk.power/(float(dist-1)*float(atk.distmod)+1))
        d = getdef(self,atk)
        if self.map.gettile(self.pos).terrain in ["mountain"]:
            d+=1
            p+=1
        if self.map.gettile(self.pos).terrain in ["town","forest"]:
            d+=2
            p-=1
    
        li = []
        for i in range(0,p+1):
            d2=abs(i-d)
            for i2 in range(d2*2+1):
                li.append(i)
        if hasattr(atk,"killer"):
            while 0 in li:
                li.remove(0)
            for i in range(10):
                li.append(li[-1])
        #print li
    
        p=random.choice(li)
        if hasattr(u,"fullpower"):
            p=li[-1]
        if p<0: p=0
        #return p  #Delete this line when copying
        if self.health>0:
            self.health-=p
            pygame.messages.append([str(p),[self.tpos[0],self.tpos[1]],-1,[self.tpos[0],self.tpos[1]],[100,0,0]])
        if self.health<=0:
            self.map.map[self.pos[1]][self.pos[0]].unit = None
        return p
    def lframes(self):
        return [self.frames[6],self.frames[7]]
    def rframes(self):
        return [self.frames[4],self.frames[5]]
    def uframes(self):
        return [self.frames[0],self.frames[1]]
    def dframes(self):
        return [self.frames[2],self.frames[3]]
    def display(self,surf=None):
        block = 0
        if not surf:
            surf = pygame.display.get_surface()
        if self.type=="door":
            left = self.map.gettile([self.pos[0]-1,self.pos[1]])
            right = self.map.gettile([self.pos[0]+1,self.pos[1]])
            if left and left.terrain=="wall" or right and right.terrain=="wall":
                self.surf=doorimg
            else:
                self.surf=doorimgrot
        if self.path:
            if not hasattr(self,"mplay"):
                self.mplay = 1
                marchsound.play()
            block = 1
            nxt = self.path[0].pos
            gox,goy = nxt[0]*32,nxt[1]*32
            if hasattr(self,"frames"):
                frames = None
                if gox<self.tpos[0]:
                    frames=self.lframes()
                elif gox>self.tpos[0]:
                    frames = self.rframes()
                elif goy<self.tpos[1]:
                    frames =  self.uframes()
                elif goy>self.tpos[1]:
                    frames = self.dframes()
                if frames:
                    if self.surf not in frames:
                        self.surf = frames[0]
                    self.atime += 1
                    if self.atime>10 and frames:
                        if self.surf==frames[0]:
                            self.surf=frames[1]
                        else:
                            self.surf=frames[0]
                        self.atime = 0
            diffx = self.tpos[0]-gox
            diffy = self.tpos[1]-goy
            atx,aty=0,0
            if abs(diffx)>.01:
                self.tpos[0]+=-abs(diffx)/(diffx)*2
            else:
                atx=1
                self.tpos[0]=gox
            if abs(diffy)>.01:
                self.tpos[1]+=-abs(diffy)/(diffy)*2
            else:
                aty=1
                self.tpos[1]=goy
            if atx and aty:
                del self.path[0]
                if not self.path and hasattr(self,"mplay"):
                    del self.mplay
                    marchsound.stop()
                if not self.path:
                    self.path = None
                    if self.endpathfunc:
                        self.endpathfunc()
                    self.endpathfunc = self.deffunc
        if self.type=="footman":
            if self.health:
                fm = int(math.ceil(self.health))-1
                if fm>9:
                    fm=9
                self.surf = self.fmframes[fm]
        surf.blit(self.surf,[int(self.tpos[0]),int(self.tpos[1])])
        if self.type=="power":
            surf.blit(self.topframe,[int(self.tpos[0]),int(self.tpos[1])])
            self.atime += 1
            if self.atime>15:
                nxt = pwrframes.index(self.topframe)+1
                if nxt>=len(pwrframes):
                    nxt=1
                self.topframe = pwrframes[nxt]
                self.atime = 0
        return block
    def aimove(self,pu,usu):
        from pathfinding import findpath
        u=self
        if u.canmove():
            pths = []
            pth = None
            for pl in pu:
                for dir in [-1,0],[1,0],[0,-1],[0,1]:
                    np = pl.pos[0]+dir[0],pl.pos[1]+dir[1]
                    t = u.map.gettile(np)
                    if not t:
                        continue
                    pth = findpath(u.pos,t.pos,u.map.map)
                    d=10
                    if hasattr(u,"airange"):
                        d=u.airange
                    if pth and pth[-1].g<d:
                        pths.append(pth)
                        break
            if not pths:
                #No players to attack
                #print "no players to attack"
                u.finished = 1
                return False
            def _cmp(ptha,pthb):
                if ptha and pthb and ptha[-1].g==None and pthb[-1].g==None:
                    return 0
                if not ptha or ptha[-1].g==None:
                    return -1
                if not pthb or pthb[-1].g==None:
                    return 1
                return cmp(ptha[-1].g,pthb[-1].g)
            pths.sort(_cmp)
            pth = pths[0]
            #print "plength:",len(pth)
            #Can't reach any players
            if not pth or pth[-1]==None or pth[-1].g == None:
                #print "cant reach other players"
                u.finished = 1
                return False
            i = 0
            lastpos = pth[i]
            cost = lastpos.g
            i = 1
            #Cant move
            if cost>u.speed:
                #print "cant move"
                u.finished=1
                return False
            while i<len(pth):
                nextpos = pth[i]
                if nextpos.g>u.speed:
                    break
                else:
                    lastpos = nextpos
                i+=1
            def sty():
                u.map.map[u.pos[1]][u.pos[0]].unit = None
                u.pos = [int(u.tpos[0]/32),int(u.tpos[1]/32)]
                u.map.map[u.pos[1]][u.pos[0]].unit = u
                u.moved=1
            u.endpathfunc = sty
            u.path = pth[:i]
            return True
    def aiattack(self,pu,usu):
        u=self
        from pathfinding import findpath
        if not u.attacked:
            unitsinrange = []
            for atck in u.attacks:
                ir = [p for p in atck.inrange(u.map.map,u.pos) if p.side=="player" and (not hasattr(u,"power") or atck.powerused<=u.power)]
                unitsinrange.append(ir)
            if not [ir for ir in unitsinrange if ir]:
                #print "hmm no units are in range?"
                u.attacked=2
                return False
            def _cmp(p1,p2):
                return cmp(p1.health,p2.health)
            lowestu=None
            lowesti=None
            for i in range(len(unitsinrange)):
                ir=unitsinrange[i]
                #print ir,u.attacks[i].name
                if not ir:
                    continue
                ir.sort(_cmp)
                if not lowestu:
                    lowestu=ir[0]
                    lowesti=i
                    continue
                if ir[0].health<lowestu.health or u.attacks[i].power-getdef(ir[0],u.attacks[i])>u.attacks[lowesti].power-getdef(ir[0],u.attacks[lowesti]):
                    lowestu=ir[0]
                    lowesti=i
                    continue
            pa = lowestu
            u.attackchosen=lowesti
            u.attack(pa)
            u.attacked=1
            return True
    def stats(self,pos=None):
        u=self
        if not u:
            global cunit
            u = cunit
        if not hasattr(u,"attacks"):
            pass#print u.type
        li = ["Type:"+u.type,"Attacks:"+",".join([x.name for x in u.attacks]),"Speed:"+str(u.speed),"Health:"+"%d/%d"%(u.health,u.maxhealth)]
        if hasattr(u,"power"):
            li.append("Power:"+str(u.power))
        m = mnu(li)
        m.o=-1
        if not pos:
            if u.tpos[0]>320:
                m.pos[0]=10
            else:
                m.pos[0]=640-m.width-10
        else:
            m.pos=pos
        m.display()
