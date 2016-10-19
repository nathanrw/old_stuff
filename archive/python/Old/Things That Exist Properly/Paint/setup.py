from distutils.core import setup, Extension

import sys, os, pygame, shutil
import py2exe

sys.argv[1:] = ['py2exe'] + sys.argv[1:]

setup( options={ "py2exe": { "packages": [] } },
       name='Copter',
       author='my name',
       author_email='copter-t1rxLZ7CIXjQT0dZR+AlfA@xxxxxxxxxxxxxxxx',
       url='www.mysite.com',
       version='0.2',
       windows=['Paint.py'],)


#also need to hand copy the extra files here
def installfile(name):
    dst = 'dist'
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name


pygamedir = os.path.split(pygame.base.__file__)[0]
installfile(os.path.join(pygamedir, pygame.font.get_default_font()))
