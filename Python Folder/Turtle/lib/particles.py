import pygame, os, math, random
from pygame.locals import *
from maths import *
from copy import deepcopy

def rndsign():
    return random.choice([1,-1])

def rnd2D():
    return [rndsign()*random.random(), rndsign()*random.random()]

class CompositeEmitter():
    def __init__(self, *emitters):
        self.emitters = []
        self.group = None
        for emitter in emitters:
            self.emitters.append(emitter)
            emitter.set_group(self.emitters)
    def update(self):
        for emitter in self.emitters:
            emitter.update()
    def draw(self, surface, camera_position):
        for emitter in self.emitters:
            emitter.draw(surface, camera_position)
    def set_position(self, pos):
        for emitter in self.emitters:
            emitter.set_position(pos)
    def set_group(self,group):
        self.group = group
    def add(self, emitter):
        self.emitters.append(emitter)
        emitter.set_group(self.emitters)
    def toggle(self):
        for emitter in self.emitters:
            emitter.toggle()

class Emitter():
    def __init__(self):
        self.group = None
        self.particles = []
        self.volume = 0
        self.pos = [0,0]
        self.prt_a = [0,0]
        self.prt_t = 0
        self.prt_v = [0,0]
        self.timer = 0
        self.anim = None
        self.colours = None
        self.prt_size = 0
        self.on = 1
        self.counter = 0
        self.period = 0
    
    #==========================================================================
    
    def set_group(self, list):
        self.group = list
    def set_position(self, pos):
        self.pos = pos
    def set_volume(self, volume):
        self.volume = volume
        self.period = 1.0/(volume+0.0000001)
    def set_animation(self, *anim):
        self.anim = []
        for animation in anim:
            self.anim.append(animation)
    def set_colours(self, c1, c2):
        self.colours = [c1, c2]
    def set_particle_acceleration(self, accel):
        self.prt_a = accel
    def set_particle_lifespan(self, time):
        self.prt_t = time
    def set_particle_size(self, size):
        self.prt_size = size
    def set_particle_velocity(self, vel):
        self.prt_v = vel
    def toggle(self):
        self.on = not self.on
    
    #==========================================================================
        
    def rotate(self, angle):
        self.prt_v = Rotate2DVector(self.prt_v, angle)
    def rotate_deg(self, angle):
        self.prt_v = Rotate2DVector(self.prt_v, math.radians(angle))
        
    #==========================================================================
        
    def emit2(self):
        if not self.on:
            return
        if self.anim is not None:
            for n in range(0,self.volume): self.add_img_particle()
        else:
            for n in range(0,self.volume): self.add_rect_particle()
    
    def emit(self):
        if self.on:
            self.counter += 0.1
            if self.counter > self.period:
                if self.anim is not None:self.add_img_particle()
                else: self.add_rect_particle()
                self.counter = 0
    
    def add_rect_particle(self):
        self.particles.append(RectParticle(self.particles,self.pos,\
        self.prt_v,self.prt_a,self.prt_t,self.prt_size,self.colours[0],\
        self.colours[1]))
    
    def add_img_particle(self):
        self.particles.append(ImgParticle(self.particles,self.pos,\
        self.prt_v,self.prt_a,self.prt_t,random.choice(self.anim)))
    
    #==========================================================================
    
    def update(self):
        self.emit()
        for particle in self.particles:
            particle.update()
            
    def draw(self, surface, camera_position):
        for particle in self.particles:
            particle.draw(surface, camera_position)
            
    def kill(self):
        self.group.remove(self)
    
    def copy(self):
        return deepcopy(self)

#=============================================================================
#=============================================================================

class Particle():
    def __init__(self, group, p, v, a, T):
        self.group = group
        self.pos = p
        self.vel = Add2DVector(rnd2D(),v)
        self.acc = a
        self.lifecounter=0
        self.lifespan=T
    def update(self):
        self.pos = Add2DVector(self.pos,self.vel)
        self.vel = Add2DVector(self.vel,self.acc)
        self.lifecounter+=1
        if self.lifecounter > self.lifespan:
            self.kill()
    def kill(self):
        self.group.remove(self)

class RectParticle(Particle):
    def __init__(self, group, p, v, a, T, size, c1, c2):
        Particle.__init__(self, group, p, v, a, T)
        self.colour = c1
        self.step = Mul3DVector(Sub3DVector(c2,c1),1.0/T)
        self.size = size
    def update(self):
        Particle.update(self)
        self.colour = Add3DVector(self.colour,self.step)
        if self.colour[0] < -self.step[0] and self.colour[1] < -self.step[1] \
        and self.colour[2] < -self.step[2]:
            self.kill()
    def draw(self, surface, camera_position):
        pos = Sub2DVector(Sub2DVector(self.pos, camera_position),(self.size/2,self.size/2))
        pygame.draw.rect(surface,self.colour,Rect(pos[0],pos[1],self.size,self.size))

class ImgParticle(Particle):
    def __init__(self, group, p, v, a, T, images):
        Particle.__init__(self, group, p, v, a, T)
        self.images = images
        self.animcounter = 0
        self.sizemod = [self.images[0].get_width()/2,self.images[0].get_height()/2]
        self.delta_t = 0
        self.step = 255.0/T
        self.rotation = math.atan2(self.vel[0],self.vel[1])
    def update(self):
        Particle.update(self)
        self.rotation = math.atan2(self.vel[0],self.vel[1])
        self.animcounter += 1
        if self.animcounter > len(self.images)-1:
            self.animcounter = 0
    def draw(self, surface, camera_position):
        pos = Sub2DVector(Sub2DVector(self.pos, camera_position),self.sizemod)
        img = self.images[self.animcounter]
        img = pygame.transform.rotate(img,math.degrees(self.rotation)-90)
        surface.blit(img,pos)

def main():
    pass

if __name__ == '__main__':main()