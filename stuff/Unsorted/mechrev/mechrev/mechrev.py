import pygame
log = open("log.txt","w")
fullscreen=0
playsnd=0
import sys
#sys.stdout = log
#sys.stderr = log
#print "log"

f=None
try:
    f = open("config.txt")
    print "success"
except:
    f = open("config.txt","w")
    f.write("fullscreen=1\nplaysnd=1")
    f.close()

f = open("config.txt")
if f:
    try:
        l = f.readlines()
        for i in range(len(l)):
            exec(l[i])
    except:
        print "config file error on line",i
f.close()
print "fullscreen=",fullscreen
print "playsnd=",playsnd
if playsnd:
    pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
    pygame.mixer.init()
    print "set up sounds"
    
#delay importing units until sound system set up
from rout.menu import menu as mnu
from rout.map import map
from rout.pathfinding import findpath
from rout.units import unit,attack,getdef  
    
def playmusic(file):
    if playsnd:
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
        except:
            pass

try:
    import psyco
    psyco.full()
except:
    print "psyco not available"

global menu,cunit,cunitmode,tirange,keys,lastkeys,mousepos,lastmousepos,mousebut,lastmousebut,clock,turn,side,lvl,placed,indlg,playerunits

mode = "intro"

menu = None#mnu()  #Menu we are currently editing
cunit = None  #Unit we are currently controlling
cunitmode = None #None=select an option, attack=selecting target, move=selecting destination
tirange = None #Region of tiles capable to move to
keys = None  #Keys pressed
lastkeys = None  #Keys pressed last time
mousepos = None #Position of mouse
lastmousepos = None #Last position of mouse
mousebut = None  #Mouse buttons
lastmousebut = None #Last mouse buttons
clock = None
turn = 0
side = "player"  #whos turn it is
lastlvl=-1
lvl = 0  #What level we are on
placed=0
indlg=None

mapnames = "t1","t2","t3","m1","m2","m3","m4","m5"
maps = [map("lvls/"+m) for m in mapnames]

terrain = "grass"
eunit = "robot"

units = []  #Units on the map
playerunits = ["mainhero","robot"]   #Units the player owns
playerunits = [unit(t,None,None,"player") for t in playerunits]
def setplayerunits(li):
    global playerunits
    playerunits = [unit(t,None,None,"player") for t in playerunits]
playermoney = 6

highlight = pygame.Surface([32,32])
highlight.fill([255,255,255])
highlight.set_alpha(100)
arrowup = pygame.image.load("gfx/arrow.png")
arrowup.set_alpha(255)
arrowleft = pygame.transform.rotate(arrowup,90)
arrowdown = pygame.transform.rotate(arrowup,180)
arrowright = pygame.transform.rotate(arrowup,270)

aiunits=[]
aiturn=0

f = open("lvls/story.txt")
gametext = f.readlines()
f.close()

import pickle

#~ s=None
#~ try:
    #~ s=pickle.load("save")
#~ except:
    #~ pass
#~ if s:
    #~ global playerunits,playermoney,maps
    #~ playerunits = s.pu
    #~ playermoney = s.pm
    #~ maps = s.maps

def showpic(file):
    pygame.event.clear()
    surf = pygame.display.get_surface()
    pic = pygame.image.load("gfx/"+file+".png")
    surf.blit(pic,[0,0])
    pygame.display.update()
    pygame.event.poll()
    mbut = pygame.mouse.get_pressed()
    while 1:
        lastmbut = mbut
        pygame.event.poll()
        mbut = pygame.mouse.get_pressed()
        if mbut[0] and not lastmbut[0]:
            break
        if mbut[2] and not lastmbut[2]:
            return
        pygame.event.poll()
        for evt in pygame.event.get():
            if evt.type==pygame.KEYDOWN:
                return

maxlines = 3
def dialog(starttag,endtag,after=1,pos=[0,100]):
    global indlg,lastmousebut,mousebut
    if after:
        indlg=[starttag,endtag]
        return
    indlg=None
    surf = pygame.display.get_surface()
    s2 = surf.copy()
    #~ s3 = pygame.transform.scale(s2,[500,400])
    #~ s4 = pygame.transform.scale(s3,[650,490])
    #~ s4.set_alpha(100)
    #~ s5 = pygame.transform.scale(s2,[700,580])
    #~ s6 = pygame.transform.scale(s5,[630,470])
    #~ s6.set_alpha(100)
    #~ s2.fill([150,150,150])
    #~ s2.blit(s4,[-5,-5])
    #~ s2.blit(s6,[5,5])
    lastmousebut = pygame.mouse.get_pressed()
    pygame.event.clear()
    dipic = pygame.Surface([0,0])
    start=0
    stopconvo=0
    i=0
    picname = None
    while i<len(gametext) and not stopconvo:
        lines = []
        stop=0
        starti=i
        while len(lines)<maxlines and (i-starti)<len(gametext) and not stop:
            line = gametext[i].replace("\r","").replace("\n","")
            if not start:
                if line.lower()=="#"+starttag.lower():
                    start=1
                i+=1
                starti+=1
                continue
            if line.lower()=="#"+endtag.lower():
                stopconvo=1
                break
            if line[0]=="#":
                i+=1
                starti+=1
                continue
            if line[0]=="$":
                if lines:
                    stop = 1
                    continue
                else:
                    i+=1
                #Change dialog pic
                line = line[1:].replace("\r","").replace("\n","")
                try:
                    dipic = pygame.image.load("gfx/"+line.strip()+"pic.png")
                    picname=line.strip()
                except:
                    #print "no pic:",line[0:]+"pic.png"
                    dipic = pygame.Surface([0,0])
                continue
            lines.append(line)
            i+=1
        if not lines:
            continue
        li = lines+["left click to continue; right click to skip"]
        m = mnu(li,[pos[0]+0,pos[1]+100])
        surf.blit(s2,[0,0])
        m.display(surf)
        surf.blit(dipic,[pos[0]+0,pos[1]+0])
        pygame.display.update()
        pygame.event.poll()
        mousebut = pygame.mouse.get_pressed()
        while 1:
            lastmousebut = mousebut[:]
            pygame.event.poll()
            mousebut = pygame.mouse.get_pressed()
            if mousebut[0] and not lastmousebut[0]:
                lastmousebut=mousebut[:]
                break
            if mousebut[2] and not lastmousebut[2]:
                return
        
def restartlevel():
    global playerunits,maps,oldmaps,oldplayerunits,lastlvl,oldplayermoney,playermoney
    maps = oldmaps
    playerunits=oldplayerunits
    playermoney = oldplayermoney
    lastlvl=-1

def incturn():
    global units,side,turn,menu,cunit,aiturn,aiunits,placed
    if side == "player":
        #print "enemies turn"
        side = "enemy"
        aiturn=0
        aiunits=[]
        menu = None
        cunit = None
        if not [u for u in units if u.side=='player'] and placed:
            showpic("dead")
            restartlevel()
    else:
        side = "player"
        #print "players turn"
        turn+=1
    for u in [u for u in units if u.side==side]:
        u.nextturn()
        u.resetstate()
        if hasattr(u,"thought"):
            del u.thought
def turnover():
    global units,side,placed
    if side=="player" and not placed:
        return False
    for u in [u for u in units if u.side==side]:
        if u.side=="none":
            continue
        if u.finished or (u.attacked and u.moved):
            pass
        else:
            return False
    incturn()
    return True
def endturn():
    global units
    for u in units:
        u.finished = 1

def store():
    cost = {"robot":3,"footman":1,"mainhero":"N/A","rocketlauncher":7,"heal":1,"maxhealth":4}
    maxuphealth = {"robot":25,"mainhero":30,"footman":10}
    global playerunits,playermoney,menu
    lio = ["Buy mech - price:"+str(cost["robot"]),"Buy footman - price:"+str(cost["footman"]),"Buy rocket launcher - price:"+str(cost["rocketlauncher"]),"Upgrade a unit","Done"]
    i=1
    li=lio[:]
    li.append("##Current money:"+str(playermoney)+"##")
    d={}
    for u in playerunits:
        cansell = 1
        selltxt = "  (sell:%s)"%str(cost[u.type])
        if u.health!=u.maxhealth:
            cansell=0
            selltxt = "(can't sell damaged units)"
        if u.type=="mainhero":
            cansell=0
            selltxt = "(can't sell main character)"
        o="  "+str(i)+". "+u.type+"  hp:"+"%d/%d"%(u.health,u.maxhealth)+" power:"+u.ps()+selltxt
        li.append(o)
        if cansell:
            def sell(theu=u):
                global playerunits,playermoney
                playerunits.remove(theu)
                playermoney+=cost[theu.type]
                store()
            d[o]=sell
        i+=1
    if playermoney<cost["robot"]:
        li[0]=li[0]+"(cant afford)"
    if playermoney<cost["footman"]:
        li[1]=li[1]+"(cant afford)"
    if playermoney<cost["rocketlauncher"]:
        li[2]=li[2]+"(cant afford)"
    if not playerunits:
        li.remove(lio[3])
    def dne():
        global menu
        menu = None
    def bmch():
        global playerunits,playermoney
        playerunits.append(unit("robot",None,[0,0],"player"))
        playermoney -= cost["robot"]
        store()
    def bfm():
        global playerunits,playermoney
        playerunits.append(unit("footman",None,[0,0],"player"))
        playermoney -= cost["footman"]
        store()
    def brl():
        global playerunits,playermoney
        playerunits.append(unit("rocketlauncher",None,[0,0],"player"))
        playermoney -= cost["rocketlauncher"]
        store()
    def upgrademen():
        global menu,playerunits
        li = ["Upgrade "+u.type+" hp:"+"%d/%d"%(u.health,u.maxhealth)+" power"+u.ps() for u in playerunits]
        li.append("cancel")
        d = {}
        for i in range(len(li)-1):
            def upu(theunit=playerunits[i]):
                global menu,playermoney
                lio = ["heal:"+"%d/%d"%(theunit.health,theunit.maxhealth)+"->"+"%d/%d"%(theunit.maxhealth,theunit.maxhealth)+"   -cost:1"]
                lio.append("maxhealth:"+str(theunit.health)+"/"+str(theunit.maxhealth)+"->"+str(theunit.maxhealth+5)+"/"+str(theunit.maxhealth+5)+"  -cost:3")
                lio.append("##Current money:"+str(playermoney)+"##")
                li=lio[:]
                if theunit.maxhealth>=maxuphealth[theunit.type]:
                    li[1]+=" (maxxed out)"
                elif playermoney<3:
                    li[1]=li[1]+" (not enough money)"
                if theunit.health==theunit.maxhealth:
                    li[0] = li[0]+" (health full)"
                elif playermoney<1:
                    li[0] = li[0]+" (not enough money)"
                li.append("cancel")
                def cncl():
                    upgrademen()
                def healm(theunit=theunit):
                    global playermoney
                    theunit.health=theunit.maxhealth
                    playermoney -= 1
                    upu(theunit)
                def maxhealthm(theunit=theunit):
                    global playermoney
                    theunit.maxhealth+=5
                    playermoney -= 3
                    upu(theunit)
                d = {lio[0]:healm,"_offmenu":cncl,"cancel":cncl,lio[1]:maxhealthm}
                menu = mnu(li,[100,100],d)
            d[li[i]]=upu
        def cncl():
            store()
        d.update({"_offmenu":cncl,"cancel":cncl})
        menu = mnu(li,[100,100],d)
    d.update({lio[4]:dne,lio[0]:bmch,lio[1]:bfm,lio[3]:upgrademen,lio[2]:brl})
    menu = mnu(li,[100,100],d)
    
def mainmenu():
    global menu
    li = ["End turn","Cancel"]
    def cncl():
        global menu
        menu = None
    def it():
        cncl()
        incturn()
    d = {"End turn":it,"Cancel":cncl}
    menu = mnu(li,[100,100],d)

def updatesprites():
    global units
    animblocked = 0
    for u in units:
        if u.display():
            animblocked = 1
    if pygame.messages:
        surf = pygame.display.get_surface()
        m = pygame.messages[0]
        bck=surf.copy()
        fnt = pygame.font.SysFont("Verdana",20)
        if m:
            t=pygame.theclock.tick(60)/16.0
            #surf.blit(bck,[0,0])
            fs = fnt.render(m[0],1,m[4])
            surf.blit(fs,[m[1][0],int(m[1][1])])
            if m[1][1]>m[3][1]:
                m[1][1]+=m[2]*t/2.0
            else:
                m[1][1]+=m[2]*t
            if m[1][1]<m[3][1]-5:
                m[2]=1
            if m[1][1]>m[3][1]+5:
                del pygame.messages[0]
                m=None
            #pygame.display.update()
    return animblocked
    
def menuinput(m=None):
    global keys,lastkeys,mousepos,lastmousepos,mousebut,lastmousebut,menu
    if not m:
        m = menu
    if keys[pygame.K_UP] and not lastkeys[pygame.K_UP]:
        m.o-=1
        if m.o<0:
            m.o=0
    if keys[pygame.K_DOWN] and not lastkeys[pygame.K_DOWN]:
        m.o+=1
        if m.o>=len(m.options):
            m.o=len(m.options)-1
    over = 0
    x,y=mousepos
    if x>=m.pos[0] and x<m.pos[0]+m.width and y>=m.pos[1] and y<m.pos[1]+m.height:
        over = 1
        if mousepos[0]!=lastmousepos[0] or mousepos[1]!=lastmousepos[1]:
            y-=m.pos[1]
            m.o=y/(m.optionrenders[0].get_size()[1]+4)
    if over and m.o>=0 and not hasattr(m,"init"):
        m.init=1
        y-=m.pos[1]
        m.o = y/(m.optionrenders[0].get_size()[1]+4)
    m.display()
    if mousebut[0] and not lastmousebut[0] and not over and m.funcs.has_key("_offmenu"):
        m.funcs["_offmenu"]()
    if (keys[pygame.K_RETURN]and not lastkeys[pygame.K_RETURN]) or (mousebut[0] and not lastmousebut[0] and over):
        if m.o>=0 and m.o<len(m.options) and m.funcs.has_key(m.options[m.o]):
            m.funcs[m.options[m.o]]()
def mapinput(lvlmap):
    """Click on units to do stuff"""
    global mousepos,mousebut,lastmousebut
    x,y=mousepos
    tx,ty = x/lvlmap.si,y/lvlmap.si
    groundstats(lvlmap,[tx,ty])
    u = lvlmap.map[ty][tx].unit
    if u:
        u.stats()
    if mousebut[0] and not lastmousebut[0]:
        if u:
            if u.side=="player":
                global cunit,tirange
                tirange = None
                cunit = lvlmap.map[ty][tx].unit
        else:
            mainmenu()
def groundstats(map,pos):
    t = map.map[pos[1]][pos[0]]
    sp = t.speed
    if sp<0:
        sp="N/A"
    li = ["Terrain type:"+t.terrain,"Move Cost:"+str(sp)]
    m = mnu(li,[10,400])
    m.o=-1
    if pos[0]<21:
        m.pos[0]=640-m.width-10
    m.display()
def unitinput():
    """Selected unit, choose appropriate menu"""
    global cunit,menu,cunitmode,tirange,mousebut,lastmousebut,mousepos
    unitsinrange = []
    surf = pygame.display.get_surface()
    for atck in cunit.attacks:
        ir = [u for u in atck.inrange(cunit.map.map,cunit.pos) if u.side!=cunit.side and (not hasattr(cunit,"power") or atck.powerused<=cunit.power)]
        unitsinrange.append(ir)
    #~ def et():
        #~ global cunit,menu
        #~ cunit.finished = 1
        #~ cunit = None
        #~ menu = None
    def cl():
        global cunit,menu
        cunit = None
        menu = None
    def mv():
        global cunit,menu,cunitmode
        cunitmode = "move"
        menu = None
    def at():
        global cunit,menu,cunitmode
        cunitmode = "chooseweap"
        menu = None
    def cncl():
        global cunitmode,cunit,menu
        cunitmode = None
        cunit = None
        menu = None
    def join():
        global cunitmode,menu
        cunitmode = "join"
        menu = None
    def repair():
        global cunitmode,menu
        cunitmode = "repair"
        menu = None
    joinup = []
    if cunit.type=="footman" and cunit.health<10:
        for d in [-1,0],[1,0],[0,-1],[0,1]:
            ti = cunit.map.gettile([cunit.pos[0]+d[0],cunit.pos[1]+d[1]])
            if ti and ti.unit and ti.unit.side=="player" and ti.unit.type=="footman" and ti.unit.health<10:
                joinup.append(ti.unit)
    healunits = []
    if cunit.type=="footman":
        global lvl
        healunits = []
        for u in maps[lvl].getunits():
            dx = abs(u.pos[0]-cunit.pos[0])
            dy = abs(u.pos[1]-cunit.pos[1])
            if u.side=="player" and u.health<u.maxhealth and (dx==0 and dy<=1) or (dy==0 and dx<=1):
                healunits.append(u)
        
        #~ us = [u for u in maps[lvl].getunits()]
        #~ healunits = []
        #~ for u in us:
            #~ dx = abs(u.pos[0]-cunit.pos[0])
            #~ dy = abs(u.pos[1]-cunit.pos[1])
            #~ print u.type,u.side,u.health,abs(u.pos[0]-cunit.pos[0]),abs(u.pos[1]-cunit.pos[1])
            #~ if u==cunit:
                #~ continue
            #~ if u.side!="player":
                #~ continue
            #~ if u.health>=u.maxhealth:
                #~ continue
            #~ if not (dx==0 and dy<=1) and not (dy==0 and dx<=1):
                #~ continue
            #~ healunits.append(u)
        #~ print healunits
    if not cunitmode:
        li = ["Move","Attack","Repair","Join","Cancel"]
        if not cunit.canmove() or cunit.finished:
            li.remove("Move")
        if cunit.attacked or cunit.finished or not [ur for ur in unitsinrange if ur]:
            li.remove("Attack")
        if not joinup:
            li.remove("Join")
        if not healunits:
            li.remove("Repair")
        po = [cunit.tpos[0]+32,cunit.tpos[1]]
        menu = mnu(li,po,{"Move":mv,"Attack":at,"Cancel":cncl,"_offmenu":cncl,"Join":join,"Repair":repair})
        if cunit.tpos[0]>320:
            menu.pos[0]=cunit.tpos[0]-menu.width
    elif cunitmode == "chooseweap":
        def cncl():
            global cunitmode,menu
            cunitmode = None
            menu = None
        funcs = {}
        tst = {}
        li = []
        for i in range(len(cunit.attacks)):
            if not unitsinrange[i]:
                continue
            w = cunit.attacks[i]
            refname=w.name+"  pwr:"+str(w.powerused)
            li.append(refname)
            def f(index=i):
                global cunit,cunitmode,menu
                cunit.attackchosen = index
                cunitmode ="attack"
                menu = None
            funcs[refname]=f
        funcs["Cancel"]=cncl
        funcs["_offmenu"]=cncl
        li.append("Cancel")
        menu = mnu(li,cunit.tpos,funcs)
    elif cunitmode == "attack":
        for badu in unitsinrange[cunit.attackchosen]:
            x,y = badu.pos
            tx,ty = x*32,y*32
            surf.blit(highlight,[tx,ty])
            if mousepos[0]>=tx and mousepos[0]<tx+32 and mousepos[1]>=ty and mousepos[1]<ty+32:
                badu.stats()
                if mousebut[0] and not lastmousebut[0]:
                    cunit.attack(badu)
                    cunit.attacked = 1
                    cunitmode = None
                    cunit = None
                    menu = None
                    return
            else:
                if mousebut[0] and not lastmousebut[0]:
                    cunitmode="chooseweap"
                    menu = None
    elif cunitmode == "join":
        for u in joinup:
            x,y = u.pos
            tx,ty = x*32,y*32
            surf.blit(highlight,[tx,ty])
            if mousepos[0]>=tx and mousepos[0]<tx+32 and mousepos[1]>=ty and mousepos[1]<ty+32:
                u.stats()
                if mousebut[0] and not lastmousebut[0]:
                    u.health += cunit.health
                    cunit.health = 0
                    if u.health>u.maxhealth:
                        dif = u.health-u.maxhealth
                        u.health = u.maxhealth
                        cunit.health = dif
                    cunit.finished=1
                    u.finished=1
                    if cunit.health<=0:
                        cunit.map.map[cunit.pos[1]][cunit.pos[0]].unit = None
                        cunit = None
                    cunitmode = None
                    menu = None
                    return
            else:
                if mousebut[0] and not lastmousebut[0]:
                    cunitmode=None
                    menu = None
    if cunitmode == "repair":
        for u in healunits:
            x,y = u.pos
            tx,ty = x*32,y*32
            surf.blit(highlight,[tx,ty])
            if mousepos[0]>=tx and mousepos[0]<tx+32 and mousepos[1]>=ty and mousepos[1]<ty+32:
                u.stats()
                if mousebut[0] and not lastmousebut[0]:
                    u.health+=u.maxhealth/3
                    if u.health>u.maxhealth:
                        u.health=u.maxhealth
                    cunit.finished=1
                    cunitmode = None
                    menu = None
                    return
            else:
                if mousebut[0] and not lastmousebut[0]:
                    cunitmode=None
                    menu = None
    elif cunitmode == "move":
        if tirange==None:
            tirange = []
            sp = cunit.speed
            sx = cunit.pos[0]-sp
            sy = cunit.pos[1]-sp
            ex = cunit.pos[0]+sp
            ey = cunit.pos[1]+sp
            chktiles = []
            for tx in range(sx,ex+1):
                for ty in range(sy,ey+1):
                    chktiles.append([tx,ty])
            for ti in chktiles:
                pth = findpath(cunit.pos,ti,cunit.map.map)
                if pth and pth[-1].g<=sp:
                    tirange.append(pth)
        if not tirange:
            cunitmode = None
            menu = None
            return
        for ti in tirange:
            surf.blit(highlight,[ti[-1].pos[0]*32,ti[-1].pos[1]*32])
        global mousepos,mousebut,lastmousebut
        mtx,mty = mousepos[0]/32,mousepos[1]/32
        pth = None
        for ti in tirange:
            if mtx==ti[-1].pos[0] and mty==ti[-1].pos[1]:
                pth = ti
        if not pth and mousebut[0] and not lastmousebut[0]:
            cunitmode = None
        if pth:
            p = cunit.pos
            i = 0
            while i<len(pth):
                lastp = p
                p = pth[i].pos
                if p[0]>lastp[0]:
                    surf.blit(arrowright,[lastp[0]*32,lastp[1]*32])
                elif p[0]<lastp[0]:
                    surf.blit(arrowleft,[lastp[0]*32,lastp[1]*32])
                elif p[1]>lastp[1]:
                    surf.blit(arrowdown,[lastp[0]*32,lastp[1]*32])
                elif p[1]<lastp[1]:
                    surf.blit(arrowup,[lastp[0]*32,lastp[1]*32])
                i+=1
            mnu([str(pth[-1].g)],[mtx*32,mty*32]).display()
            if mousebut[0] and not lastmousebut[0]:
                tirange = None
                cunit.path = pth
                def stay(u=cunit):
                    u.map.map[u.pos[1]][u.pos[0]].unit = None
                    u.pos = [int(u.tpos[0]/32),int(u.tpos[1]/32)]
                    u.map.map[u.pos[1]][u.pos[0]].unit = u
                    global menu
                    menu = None
                    global cunit,cunitmode
                    cunit = None
                    cunitmode = None
                    u.moved=1
                def cncl(u=cunit):
                    u.tpos = [u.pos[0]*32,u.pos[1]*32]
                    global menu,cunitmode,cunit
                    cunit = u
                    menu = None
                    cunitmode = None
                def fin(u=cunit):
                    global menu
                    menu = mnu(["Stay","Cancel"],[u.tpos[0]+32,u.tpos[1]],{"Stay":stay,"Cancel":cncl})
                    if u.tpos[0]>320:
                        menu.pos[0]=u.tpos[0]-menu.width
                cunit.endpathfunc = fin
                cunitmode = None
                cunit = None
        elif mousebut[0] and not lastmousebut[0]:
            cunitmode = None
            menu = None
def aiplay(lvlmap):
    global aiunits,aiturn
    units = lvlmap.getunits()
    usu = [u for u in units if u.side=="enemy"]
    if not usu:
        incturn()
        return
    if not aiunits:
        aiunits = usu
        aiturn = 0
    pu = [u for u in units if u.side=="player"]
    if not aiturn<len(aiunits):
        incturn()
        return
    u = aiunits[aiturn]
    surf = pygame.display.get_surface()
    surf.blit(highlight,u.tpos)
    if u.path:
        return
    if u.aimove(pu,usu):
        u.moved=1
        return
    u.aiattack(pu,usu)
    if not u.canmove():
        u.moved = 1
    #if u.moved and u.attacked:
    #   u.finished = 1
    #   aiturn+=1
    aiturn+=1
    u.finished=1
    return
def editinput(editmap,surf):
    global terrain,mousepos,mousebut,lastmousebut,eunit
    if keys[pygame.K_1]:
        terrain = "grass"
    if keys[pygame.K_2]:
        terrain = "mountain"
    if keys[pygame.K_3]:
        terrain = "water"
    if keys[pygame.K_4]:
        terrain = "forest"
    if keys[pygame.K_5]:
        terrain = "bridge"
    if keys[pygame.K_6]:
        terrain = "floor"
    if keys[pygame.K_7]:
        terrain = "wall"
    if keys[pygame.K_8]:
        terrain = "crates"
    if keys[pygame.K_9]:
        terrain = "town"
    if keys[pygame.K_q]:
        eunit = "robot"
    if keys[pygame.K_w]:
        eunit = "power"
    if keys[pygame.K_e]:
        eunit = "playerstart"
    if keys[pygame.K_r]:
        eunit = "footman"
    if keys[pygame.K_t]:
        eunit = "gramps"
    if keys[pygame.K_y]:
        eunit = "door"
    if keys[pygame.K_u]:
        eunit = "rocketlauncher"
    if keys[pygame.K_i]:
        eunit = "endboss"
    x,y = mousepos
    tx,ty = x/editmap.si,y/editmap.si
    if mousebut[0]:
        editmap.map[ty][tx].terrain = terrain
        editmap.display(surf)
    if mousebut[2] and not lastmousebut[2]:
        if eunit=="playerstart":
            if editmap.map[ty][tx].playerstart:
                editmap.map[ty][tx].playerstart=False
            else:
                editmap.map[ty][tx].playerstart=True
        else:
            if editmap.map[ty][tx].unit:
                editmap.map[ty][tx].unit = None
            else:
                editmap.map[ty][tx].unit = unit(eunit,editmap,[tx,ty])
    u = editmap.map[ty][tx].unit
    if u:
        u=u.type
    else:
        u="none"
    tm = mnu(["edit:"+terrain,"over:"+editmap.map[ty][tx].terrain,"addunit:"+eunit,"overunit:"+u,
    "pos:["+str(tx)+","+str(ty)+"]"])
    tm.o=-1
    if x<320:
        tm.pos[0]=400
    menuinput(tm)
def placeunits(editmap):
    global mousepos,mousebut,lastmousebut,playerunits,menu
    if not hasattr(editmap,"plcemnu"):
        def dne():
            global placed
            placed=1
        li = ["*Place units.  Once you click finish,","you won't be able to place the rest","until the next mission","Finished"]
        if "mainhero" not in [u.type for u in editmap.getunits() if u.side=="player"]:
            li[3]="Must at least place main hero"
        editmap.plcemnu = mnu(li,funcs={"Finished":dne})
    surf = pygame.display.get_surface()
    high2=highlight.copy()
    high2.fill([0,0,255])
    high2.set_alpha(50)
    for tx in range(20):
        for ty in range(15):
            if editmap.map[ty][tx].playerstart:
                surf.blit(high2,[tx*32,ty*32])
    x,y = mousepos
    tx,ty = x/editmap.si,y/editmap.si
    li = []
    d = {}
    i = 0
    for u in playerunits:
        s = str(i)+"."+u.type
        i+=1
        li.append(s)
        def setu(em=editmap,un=u):
            global menu,playerunits,units
            em.map[ty][tx].unit = un
            un.pos = [tx,ty]
            un.map = em
            menu = None
            playerunits.remove(un)
            units = em.getunits()
            del em.plcemnu
        d[s]=setu
    def cncl():
        global menu
        menu = None
    li.append("Cancel")
    d["_offmenu"]=cncl
    d["Cancel"]=cncl
    m = mnu(li,[x,y],d)
    u = editmap.map[ty][tx].unit
    ps = editmap.map[ty][tx].playerstart
    if ps:
        surf.blit(highlight,[tx*32,ty*32])
        if mousebut[0] and not lastmousebut[0]:
            oldu = editmap.map[ty][tx].unit
            if oldu:
                playerunits.append(oldu)
                editmap.map[ty][tx].unit = None
            else:
                menu = m
    menuinput(editmap.plcemnu)
    
def special(themap,back,calltime="before"):
    global lvl,menu,cunit
    if lvl==0:
        if turn==0 and not hasattr(themap,"state"):
            showpic("title")
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("introstart","introend",0)
            u = themap.map[7][11].unit = unit("robot",themap,[11,7],"player")
            u.power = 200
            u.nosave=1
            u.attacks = []
            themap.u = u
            themap.upos = u.pos
            themap.state=0
            return
        if themap.state==0:
            if not hasattr(themap,"firstdi"):
                dialog("grampsintro","grampsintroend")
                themap.firstdi=1
                global placed
                placed=1
            if menu and cunit:
                menu.display()
                dialog("grampsmenus","grampsmenue",0,[0,300])
                themap.state=1
                themap.turn=turn
            return
        if themap.state==1 and not menu and not cunit:
            dialog("GrampsStay","GrampsStayE")
            themap.state=2
            return
        if themap.state==2:
            umoved=0
            for u in themap.getunits():
                if not umoved:
                    umoved=u.moved
            if umoved:
                dialog("GrampsEndTurnS","GrampsEndTurnE")
                themap.state=3
                return
        if themap.state==3:
            if turn!=themap.turn:
                dialog("grampsmoveagains","grampsmoveagaine")
                themap.state=4
                themap.turn=turn
            return
        if themap.state==4:
            for pos in [[15,6],[15,7],[15,8],[16,3],[16,4],[16,5],[16,6],
            [16,7],[16,8],[16,9],[16,10],[16,11],[17,3],[17,4],[17,5],[17,6],
            [17,7],[17,8],[17,9],[17,10],[17,11],[18,3],[18,4],[18,5],[18,6],
            [18,7],[18,8],[18,9],[18,10],[18,11]]:
                if turn!=themap.turn and themap.u.pos[0]==pos[0] and themap.u.pos[1]==pos[1]:
                    themap.state=5
                    dialog("tut1endings","tut1endinge",0)
                    lvl+=1
                    return
            return
        return
    if lvl==1:
        if not hasattr(themap,"state") and calltime=="before":
            global placed
            u1=themap.map[7][9].unit = unit("footman",themap,[9,7],"player")
            u1.health=4
            u1.speed=0
            u1.nosave=1
            u1.attacks=[]
            u2=themap.map[7][10].unit = unit("footman",themap,[10,7],"player")
            u2.health=3
            u2.speed=0
            u2.nosave=1
            u2.attacks=[]
            themap.state=0
            themap.u1=u1
            themap.u2=u2
            placed=1
            return
        if not hasattr(themap,"state"):
            return
        if themap.state==0:
            if not hasattr(themap,"startdlg"):
                dialog("tut2s","tut2e")
                themap.startdlg=1
                themap.turn = turn
                return
            if turn!=themap.turn and calltime=="after" and (themap.u1.health==7 or themap.u2.health==7):
                dialog("tut2afterjoins","tut2afterjoine",0)
                lvl+=1
                return
    if lvl==2:
        global placed
        placed=1
        if turn==0:
            u = themap.map[5][5].unit = unit("mainhero",themap,[5,5],"player")
            u.nosave=1
            gramps = [x for x in themap.getunits() if x.type=="gramps"][0]
            themap.gramps=gramps
            themap.state=0
            return
        if themap.state==0:
            dialog('tut3s','tut3e')
            themap.state=1
            return
        if themap.state==1:
            e = themap.map[5][11].unit=unit("footman",themap,[11,5],"enemy")
            e.health=3
            e.fullpower=1 #Make his attacks always do full damage, in order to make sure he kills gramps
            e.attacks=[attack("guns","ranged","cross",1,1,0)]
            gramps = themap.gramps
            e.path = findpath(e.pos,[gramps.pos[0]+1,gramps.pos[1]],themap.map)
            themap.state=2
            themap.e = e
            return
        if themap.state==2:
            if not themap.e.path:
                themap.state=3
                dialog("guardtlk1","guardtlk1e",0)
            return
        if themap.state==3 or themap.state==5:
            themap.state+=1
            themap.e = themap.map[themap.e.pos[1]][themap.e.pos[0]].unit
            themap.e.attackchosen=0
            themap.e.attack(themap.gramps)
            return
        if themap.state==4:
            dialog("guardtlk2","guardtlk2e",0)
            themap.state=5
            return
        if themap.state==6:
            dialog("guardtlk3","guardtlk3e")
            themap.state=7
            global side
            incturn()
            return
        if themap.state==7:
            if not [x for x in themap.getunits() if x.side=="enemy"]:
                dialog("tut3ends","tut3ende",0)
                lvl+=1
            return
    if lvl==3:
        global menu,cunit
        if turn==0:
            store()
            themap.state=0
            return
        if themap.state==0 and placed:
            dialog("chapter one begin","chapter one end")
            themap.state=1
            return
        if themap.state==1 and not cunit and not menu and not [u for u in themap.getunits() if u.side=="enemy"]:
            dialog("After you kill the last robot","intermission 1",0)
            lvl+=1
            global playermoney
            playermoney += 2
            return
    if lvl==4:
        if turn==0 and not hasattr(themap,"state"):
            playmusic("snd/mus2.ogg")
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("intermission 1","intermission 1 end",0)
            themap.state=1
            return
        if themap.state==1:
            store()
            themap.turn = turn
            themap.state=2
            return
        global placed
        if themap.state==2 and placed:
            dialog("chapter two begin","Evil units enter screen")
            u1=unit("robot",themap,[11,14],"enemy")
            u1.airange=20
            themap.map[u1.pos[1]][u1.pos[0]].unit=u1
            u1.path=findpath(u1.pos,[12,12],themap.map)
            
            u2=unit("robot",themap,[15,14],"enemy")
            u2.airange=20
            themap.map[u2.pos[1]][u2.pos[0]].unit=u2
            u2.path=findpath(u2.pos,[16,13],themap.map)
            themap.state=3
            return
        if themap.state==3 and not [u for u in themap.getunits() if u.side=="enemy" and u.path]:
            themap.state=4
            u1 = unit("footman",themap,[13,14],"enemy")
            u1.airange=50
            themap.map[u1.pos[1]][u1.pos[0]].unit=u1
            u2 = unit("footman",themap,[18,14],"enemy")
            u2.airange=50
            themap.map[u2.pos[1]][u2.pos[0]].unit=u2
            u1.path=findpath(u1.pos,[14,13],themap.map)
            u2.path=findpath(u2.pos,[18,13],themap.map)
            
            u3 = unit("branden",themap,[10,14],"enemy")
            themap.map[u3.pos[1]][u3.pos[0]].unit=u3
            u3.path=findpath(u3.pos,[10,12],themap.map)
            return
        if themap.state==4 and not [u for u in themap.getunits() if u.side=="enemy" and u.path]:
            dialog("Evil units enter screen","Branden walks over to river")
            bd = [u for u in themap.getunits() if u.type=="branden"][0]
            bd.path=findpath(bd.pos,[8,13],themap.map)
            themap.state=5
            return
        if themap.state==5 and not [u for u in themap.getunits() if u.side=="enemy" and u.path]:
            dialog("Branden walks over to river","chapter two end")
            themap.state=6
            return
        if themap.state==6 and not [u for u in themap.getunits() if u.type=="branden"]:
            dialog("chapter two end","Branden dies",0)
            dialog("Branden dies","intermission 2 begin",0)
            lvl+=1
            global playermoney
            playermoney += 4
            themap.state=7
            return
    if lvl==5:
        if turn==0 and not hasattr(themap,"state"):
            playmusic("snd/mus1.ogg")
            themap.state=0
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("intermission 2 begin","chapter three begin",0)
            store()
            return
        if themap.state==0 and placed:
            dialog("chapter three begin","Guards up in the hills see the good guys down in the valley.")
            themap.state=2
            return
        global side
        if themap.state==2 and side=="enemy" and calltime=="before":
            themap.state=3
            dialog("Guards up in the hills see the good guys down in the valley.","chapter three end")
            return
        if themap.state==3 and not [u for u in themap.getunits() if u.side=="enemy"]:
            dialog("chapter three end","intermission 3 begin",0)
            global playermoney,lvl
            lvl+=1
            playermoney+=4
            return
    if lvl == 6:
        if turn==0 and not hasattr(themap,"state"):
            playmusic("snd/mus2.ogg")
            themap.state=0
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("intermission 3 begin","chapter four begin",0)
            store()
            return
        if themap.state==0 and placed:
            dialog("chapter four begin","chapter four end")
            themap.state=1
            return
        if themap.state==1 and not [u for u in themap.getunits() if u.side=="enemy"]:
            dialog("chapter four end","intermission four begin",0)
            global playermoney,lvl
            lvl+=1
            playermoney+=6
            return
    if lvl == 7:
        if turn==0 and not hasattr(themap,"state"):
            themap.state=0
            playmusic("snd/mus1.ogg")
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("intermission four begin","chapter five begin",0)
            store()
            return
        if themap.state==0 and placed:
            dialog("chapter five begin","When you reach core room")
            themap.state=1
            return
        if themap.state==1 and calltime=="after":
            for x in range(6,13+1):
                for y in range(1,6+1):
                    t = themap.gettile([x,y])
                    if t and t.unit and t.unit.side=="player":
                        dialog("When you reach core room","chapter five end")
                        themap.state=2
                        playmusic("snd/mus3.ogg")
                        return
        if themap.state==2 and not [u for u in themap.getunits() if u.side=="enemy"]:
            playmusic("snd/endmusic.ogg")
            dialog("chapter five end","finale",0)
            showpic("cutscene1")
            pygame.display.get_surface().fill([0,0,0])
            pygame.display.update()
            dialog("finale","end",0)
            showpic("ending")
            import sys
            sys.exit()

def loop():
    go=1
    global units,menu,cunit,keys,lastkeys,mousepos,lastmousepos,mousebut
    global lastmousebut,clock,lvl,playerunits,side,turn,placed,lastlvl
    surf = pygame.display.get_surface()
    lvlmap = maps[lvl]
    bck = pygame.Surface([640,480])
    lvlmap.display(bck)
    edit = 0
    #~ pygame.mixer.music.load("snd/mus1.ogg")
    #~ pygame.mixer.music.play(-1)
    while go:
        if lvl!=lastlvl:
            def setpower(u):
                if hasattr(u,"power") and hasattr(u,"maxpower"):
                    u.power=u.maxpower
            def uphealth(u):
                if u.health<u.maxhealth*.75:
                    u.health=int(u.maxhealth*.75)
            [(playerunits.append(u),lvlmap.clearunit(u),setpower(u),uphealth(u),u.resetstate()) for u in lvlmap.getunits() if u.side=="player" and not hasattr(u,"nosave")]
            lvlmap = maps[lvl]
            lvlmap.display(bck)
            lastlvl=lvl
            turn=0
            placed=0
            cunit = None
            global oldmaps,oldplayerunits,oldplayermoney
            oldplayermoney=playermoney
            oldmaps = [map(lines=m.tostr()) for m in maps]
            def cpy(u):
                nu = unit(u.type,None,[0,0],"player")
                nu.maxhealth=u.maxhealth
                nu.health=u.health
                if hasattr(u,"maxpower"):
                    nu.maxpower=u.maxpower
                    nu.power=u.power
                return nu
            oldplayerunits = [cpy(u) for u in playerunits]
        if not edit:
            special(lvlmap,bck,"before")
        clock.tick(60)
        surf.blit(bck,[0,0])
        
        units = lvlmap.getunits()
                
        if not playerunits:
            units = [x for x in units]
        
        #display
        animblocker = updatesprites()  #Play idle animations
        
        #input
        pygame.event.pump()
        keys = list(pygame.key.get_pressed())
        mousepos = pygame.mouse.get_pos()
        mousebut = pygame.mouse.get_pressed()
        placing=0
        if keys[pygame.K_ESCAPE]:
            return
        if keys[pygame.K_TAB] and not lastkeys[pygame.K_TAB]:
            if not edit:
                edit = 1
            else:
                edit = 0
        if keys[pygame.K_e]:
            incturn()
        if edit:
            editinput(lvlmap,bck)
            if keys[pygame.K_PERIOD] and not lastkeys[pygame.K_PERIOD]:
                if lvl<len(maps)-1:
                    lvl+=1
            elif keys[pygame.K_COMMA] and not lastkeys[pygame.K_COMMA]:
                if lvl>0:
                    lvl -= 1
                    lvlmap = maps[lvl]
                    lvlmap.display(bck)
                    turn = 0
            #elif keys[pygame.K_r] and not lastkeys[pygame.K_r]:
            #   lvlmap = map()
            #   maps[lvl]=lvlmap
            #   lvlmap.display(bck)
            elif keys[pygame.K_F5] and not lastkeys[pygame.K_F5]:
                lvlmap.save("lvls/"+mapnames[lvl])
            elif keys[pygame.K_F7] and not lastkeys[pygame.K_F7]:
                lvlmap = map("lvls/m"+str(lvl+1))
                maps[lvl] = lvlmap
                lvlmap.display(bck)
        elif menu and not animblocker:
            menuinput(menu)
        elif side=="enemy" and not animblocker:
            aiplay(lvlmap)
        elif side=="player" and not placed and not animblocker and lvlmap.getplayerstarts():
            placeunits(lvlmap)
        elif side=="player" and cunit and not animblocker:
            unitinput()
        elif side=="player" and not animblocker:
            mapinput(lvlmap)
        lastkeys = keys
        lastmousepos = mousepos[:]
        lastmousebut = mousebut[:]
        pygame.display.flip()
        global indlg
        if not menu and indlg:
            dialog(indlg[0],indlg[1],0)
            indlg=0
        if not edit:
            special(lvlmap,bck,"after")
        if not cunit and not edit and not menu and placed:
            turnover()
        #~ if not edit and not [eu for eu in lvlmap.getunits() if eu.side=="enemy"]:
            #~ playerunits = [pu for pu in lvlmap.getunits() if pu.side=="player"]
            #~ side = "player"
            #~ turn = 0
            #~ lvlmap = nxtlvl(bck)
            #~ if not lvlmap:
                #~ return
        if not edit and turn==0:
            turn=1

def run():
    global lastkeys,clock,lastmousepos,lastmousebut
    pygame.display.set_mode([640,480],pygame.FULLSCREEN*fullscreen)
    lastkeys = pygame.key.get_pressed()
    lastmousepos = pygame.mouse.get_pos()
    lastmousebut = pygame.mouse.get_pressed()
    clock  = pygame.time.Clock()
    pygame.theclock = clock
    pygame.messages = []
    loop()
    
if __name__=="__main__":
    run()
