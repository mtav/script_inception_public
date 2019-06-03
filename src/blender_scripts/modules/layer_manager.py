#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To make Blender happy:
bl_info = {"name":"layer_manager", "category": "User"}

""" Registration info for Blender menus:
Name: 'Layer Manager'
Blender: 240
Group: 'System'
Tooltip: 'Manages layers and layers sets'

.. todo:: blender 2.5+ port
"""

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2005-2006 Mariano Hidalgo
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------


__author__ = "Mariano Hidalgo AKA uselessdreamer"
__url__ = ("blender", "elysiun")
__version__ = "1.0"

__bpydoc__ = """\
Blender Layer Manager Script 1.0

The buttons on each row are:
Solo Layer - Click to make this layer the only one visible (this
   is the same as regular click in the layer buttons in header).
Turn Layer ON and OFF - Click to turn layer on and off (same as
   Ctrl Click in the layer buttons in the 3D View header).
Layer Name - Shows the layer name. Click to change it.
Layer Objects - Displays a menu with all the object in this layer.   

By using Layer Sets you can easily prepare sets of layers with the
requiered ones to do a full render, make a set with only important
layers, objects but no enviroment, etc.
You can add a empty set or add a copy of the current one with the
options in the menu left to the set name. To rename a set just click
in the set name string input. The little X on the right will remove
the set from the list.

Layer names and layer set are saved in the .blend as texts.
"""

#import Blender
#from Blender import Draw, BGL, Text, Scene, Window, Object

class LayerManagerObjects:
  def __init__(self):
    self.toggles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
    self.offset = 0
    
    #~ try:
      #~ print 'normal stuff...'
      #~ self.txt = Text.Get("layernames")
    #~ except:
      #~ print 'Blender, we have an exception!'
      #~ self.txt = Text.New("layernames")
      #~ self.txt.write("Camera afdsfsnd Martelly\n")
      #~ self.layersets = ["Working Set,1"]
      #~ for i in range(19):
        #~ self.txt.write("huhu " + i + " hihih\n")
      #~ for i in self.layersets:
        #~ self.txt.write(i +"\n")
    
    # initialisation
    self.DefaultLayers =  ['box',
    'spheres',
    'blocks',
    'cylinders',
    'excitations',
    'mesh',
    'probes',
    'time_snapshots_X',
    'time_snapshots_Y',
    'time_snapshots_Z',
    'eps_snapshots_X',
    'eps_snapshots_Y',
    'eps_snapshots_Z',
    'frequency_snapshots_X',
    'frequency_snapshots_Y',
    'frequency_snapshots_Z']

    #self.txt = Text.New("layernames")
    #for i in range(20):
      #if i<len(self.DefaultLayers):
        #self.txt.write(self.DefaultLayers[i]+'\n')
      #else:
        #self.txt.write('\n')
    
    #self.layersets = ["Working Set,1"]
    #for i in self.layersets:
      #self.txt.write(i +"\n")
      
    #self.names = self.txt.asLines()
    #self.names.pop()
    #self.layersets = self.names[20:]  
    
    #self.curset = self.layersets[0][0:self.layersets[0].find(",")]
    
    #self.scn = Scene.getCurrent()
    #for i in range(20):
      #if self.scn.layers.count(i):
        #self.toggles[i-1] = 1

  def event(self, evt, val):
    #global offset
    if evt == Draw.ESCKEY or evt == Draw.QKEY or evt == Draw.RIGHTMOUSE:
      Draw.Exit()             
      return
    if evt == Draw. WHEELUPMOUSE:
      self.offset = self.offset +20
      Draw.Redraw(1)    
    if evt == Draw. WHEELDOWNMOUSE:
      self.offset = self.offset -20
      Draw.Redraw(1)    
  
  def button_event(self, evt):
    #global curset, templayers 
    
    #
    # Layer ON/OFF button events
    #
    if evt <20:
      self.toggles[evt] = 1 - self.toggles[evt]
      mylayers = []
      for i in range(20):
        if self.toggles[i]:
          mylayers.append(i+1)
          self.scn.layers = mylayers
      Draw.Redraw()
      self.scn.update(1)
      Blender.Redraw()
    
    #
    # Layer SOLO/UNSOLO button events
    #
    if evt >= 20 and evt < 40:
      if self.scn.layers != [evt -19]:
        templayers = self.scn.layers
        for i in range(20):
          self.toggles[i] = 0
        self.toggles[evt-20] = 1  
        self.scn.layers = [evt -19]
      else:
        self.scn.layers = templayers
        for item in self.scn.layers:
          self.toggles[item-1] = 1
      Draw.Redraw()
      self.scn.update(1)
      Blender.Redraw()
    
    #
    # Layer NAME Button events
    #
    if evt >= 40 and evt < 60 and Window.GetKeyQualifiers() != 48:
      newname = Draw.PupStrInput("Name:", self.names[evt-40], 25)
      if newname:
        self.names[evt-40] = newname
        self.updatetxt()
        Draw.Redraw()
    
    #
    # Layer OBJEctS button events
    #
    elif evt >= 60 and evt < 80:
      objs = []
      obs = Object.Get()
      for ob in obs:
        if ob.layers.count(evt-59):
          objs.append(ob.getName())
      menu = "Objects in this Layer%t|"
      for item in objs:  
        menu = menu + "|" + item  
      if menu != "Objects in this Layer%t|":
        menu = menu + "|%l|Select all%x100"
      else:
        menu = "Sorry%t|There are no Objects in this Layer"
      c = Draw.PupMenu(menu)  
      if c != -1 and c != 100 and menu != "Sorry%t|There are no Objects in this Layer":
        sel = Object.GetSelected()
        for item in sel:
          item.select(0)
        newob = Object.Get(objs[c-1])
        newob.select(1)
      elif c == 100:
        sel = Object.GetSelected()
        for item in sel:
          item.select(0)
        for item in objs:
          Object.Get(item).select(1)
    
    #
    # Remove Layer Set
    #
    if evt == 99:
      for item in self.layersets:
        if item.find(self.curset) != -1:
          toremove = item
          print("toremove:" + toremove)
      self.layersets.remove(toremove)
      self.curset = self.layersets[0][0:self.layersets[0].find(",")]
      self.updatetxt()
      tomodify = self.layersets[0].split(",")
      tomodify.pop(0)    
      for item in range(21):
        self.toggles[item-1] = 0
      for item in tomodify:  
        self.toggles[int(item)-1] = 1
      Draw.Redraw(1)
    
    #
    # Update Layer Manager
    #
    if evt == 98:  
      for i in range(21):
        if self.scn.layers.count(i):
          self.toggles[i-1] = 1
        else:  
          self.toggles[i-1] = 0
      Draw.Redraw(1)
      Blender.Window.FileSelector(self.algosomething, "Import Bristol FDTD file...");
    
    #
    # Layer Sets Menu
    #
    if evt == 100:    
      if men.val <= len(self.layersets):
        # Set LayerSet current Set
        for item in self.layersets:
          if item.find(self.curset) != -1:
            tomodify = item
        if tomodify:
          tomodify = tomodify.split(",")
          tomodify.pop(0)
        count = 0
        c = -1
        for item in self.toggles:
          if item == 1: count = count +1
        if len(tomodify) != count:      
          c = Draw.PupMenu("Set has Changed. Save?%t|Yes|No")
        else:
          for item in tomodify:
            if self.toggles[int(item)-1] == 0:
              c = Draw.PupMenu("Set has Changed. Save?%t|Yes|No")
        if c != -1 and c != 2:
          for item in self.layersets:
            if item.find(self.curset) != -1:
              tomodify = item
          if tomodify:
            self.layersets.remove(tomodify)
            self.layersets.append(self.curset + "," + str(self.scn.layers)[1:-1])
            self.layersets.sort()
            self.layersets.reverse()
            self.updatetxt()
        toset = self.layersets[men.val-1].split(",")
        self.curset = toset[0]
        toset.pop(0)
        mylayers = []
        for item in toset:
          mylayers.append(int(item))
        self.scn.layers = mylayers  
        Draw.Redraw(1)
        for i in range(21):
          if self.scn.layers.count(i):
            self.toggles[i-1] = 1
          else:  
            self.toggles[i-1] = 0  
        #
        
      if men.val == 100 or men.val == 101:
        newset = Draw.PupStrInput("Set Name:", "", 25)
        if newset != None:
          newset = newset.replace(","," ")
          print(newset)
          if men.val == 100:
            self.layersets.append(newset + ",1")
          else:
            toap = newset
            for item in self.scn.layers:
              toap = toap + "," + str(item)
            self.layersets.append(toap)
          self.curset = self.layersets[-1][0:self.layersets[-1].find(",")]        
          if men.val == 100:
            self.scn.layers = [1]
            for i in range(20):
              self.toggles[i] = 0
            self.toggles[0] = 1
      elif men.val == 102:
        for item in self.layersets:
          if item.find(self.curset) != -1:
            tomodify = item
        if tomodify:
          self.layersets.remove(tomodify)
          self.layersets.append(self.curset + "," + str(self.scn.layers)[1:-1])
      self.layersets.sort()
      self.layersets.reverse()
      self.updatetxt()
      Draw.Redraw(1)
      self.scn.update(1)
      Blender.Redraw()
    
    if evt == 101:
      st.val = st.val.replace(","," ")
      count = 0
      for item in self.layersets:
        if item.find(self.curset) != -1:
            tomodify = item
            toindex = count
        count = count + 1    
      tomodify = tomodify.replace(self.curset,st.val)
      self.layersets[toindex] = tomodify
      self.layersets.sort()
      self.layersets.reverse()
      self.updatetxt()
      self.curset = st.val
      Draw.Redraw(1)
      
  def updatetxt(self):
    #global txt
    Text.unlink(self.txt)
    self.txt = Text.New("layernames")
    for i in range(20):
      self.txt.write(self.names[i] +"\n")
    for i in self.layersets:
      self.txt.write(i +"\n")
    
  def INTtoFLOAT(self, rgba):
    r = float(rgba[0] *10 /254) /10
    g = float(rgba[1] *10 /254) /10
    b = float(rgba[2] *10 /254) /10
    a = float(rgba[3] *10 /254) /10
    return [r,g,b,a]
    
  def gui(self):
    #global st,men,lsetmenu,curset, offset
    #lsetmenu = "Layer Sets%t"
    lsetmenu = ""
    for i in self.layersets:
      lsetmenu = lsetmenu + "|    " + i[0:i.find(",")]
    lsetmenu = lsetmenu + "|SAVE SET%x102|NEW SET FROM LAYERS%x101|NEW SET%x100"  
    
    theme = Blender.Window.Theme.Get()[0]
    buts = theme.get('buts')    
    r,g,b,a = self.INTtoFLOAT(buts.back)  
    BGL.glClearColor(r+0.05,g+0.05,b+0.05,a)
    BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
    
    
    BGL.glEnable(BGL.GL_BLEND)
    BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
    
    r,g,b,a = self.INTtoFLOAT(buts.panel)
    
    BGL.glColor4f(r,g,b,a+0.1)
    BGL.glBegin(BGL.GL_POLYGON)
    BGL.glVertex2i(5, self.offset + 5)
    BGL.glVertex2i(5, self.offset + 415)
    BGL.glVertex2i(185, self.offset + 415)
    BGL.glVertex2i(185, self.offset + 5)
    BGL.glEnd()  
    
    r,g,b,a = self.INTtoFLOAT(buts.header)  
    BGL.glColor4f(r-0.1,g-0.1,b-0.1,a)
    BGL.glBegin(BGL.GL_POLYGON)
    BGL.glVertex2i(5, self.offset + 415)
    BGL.glVertex2i(5, self.offset + 431)
    BGL.glVertex2i(185, self.offset + 431)
    BGL.glVertex2i(185, self.offset + 415)
    BGL.glEnd()  
    
    BGL.glDisable(BGL.GL_BLEND)
    
    BGL.glColor3f(1,1,1)
    BGL.glRasterPos2i(10,self.offset + 419)
    Draw.Text("Layer Manager", "small")
    
    BGL.glColor3f(1,1,1)
    Draw.PushButton("Update", 98, 110, self.offset + 395, 60,16 , "Updates Layer Manager")
    men = Draw.Menu(lsetmenu, 100, 26, self.offset + 10, 18,16 ,1, "Display a menu with Layer Sets")
    Draw.PushButton("X", 99, 153, self.offset + 10, 18,16 , "Exit Layer Manager")
    st = Draw.String("SET:", 101, 44, self.offset + 10, 110,16 ,self.curset,25, "Current Layer Set")
    for i in range(20):
      Draw.Toggle(str(i+1), i, 25, self.offset + 375-(18*i), 25, 16, self.toggles[i],"Turn this Layer ON and OFF")
      Draw.PushButton("", i+20, 10, self.offset + 379-(18*i), 8, 8, "Only this Layer")
      Draw.PushButton("", i+60, 173, self.offset + 376-(18*i), 6, 6, "Select Objects in this Layer")
      Draw.PushButton(self.names[i], i+40, 50, self.offset + 375 -(18*i), 120, 16, "Click to change Layer name")
  def algosomething(self):
    print('hello')
    
def main():
  layer_manager_objects = LayerManagerObjects()
  Draw.Register(layer_manager_objects.gui, layer_manager_objects.event, layer_manager_objects.button_event)
  
  print('==========================')
  print(Blender.Window.GetScreens())
  print(Blender.Window.GetAreaID())
  print(Blender.Window.GetAreaSize())
  print(Blender.Window.GetScreenInfo())
  print(Blender.Text.Get())
  print('==========================')
  #~ Blender.Window.FileSelector(algosomething, "Import Bristol FDTD file...");
  #~ Blender.Run('~/.blender/scripts/bfdtd_import.py')

if __name__ == "__main__":
  main()
