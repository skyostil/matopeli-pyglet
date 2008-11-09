#!/usr/bin/python
import pyglet
import random
import math

win = pyglet.window.Window(width=640, height=480)
head = pyglet.sprite.Sprite(pyglet.image.load('paeae.png'))
tail = pyglet.sprite.Sprite(pyglet.image.load('haentae.png'))
omppu = pyglet.sprite.Sprite(pyglet.image.load('omppu.png'))
tail.image.anchor_x, tail.image.anchor_y = (16, 16)
head.image.anchor_x, head.image.anchor_y = (0, 16)
coords = []
length = 200
#direction = 0.0
turn = 0
head.position = (320, 240)
omppu.position = random.random() * 640, random.random() * 480

@win.event
def on_key_press(key, modifiers):
  global turn
  if key == pyglet.window.key.LEFT:
    turn = -1
  elif key == pyglet.window.key.RIGHT:
    turn = 1

@win.event
def on_key_release(key, modifiers):
  global turn
  turn = 0

@win.event
def on_draw():
  win.clear()
  i = -len(coords)
  omppu.draw()
  for coord in coords:
    i += 1
    if i % 5: continue
    tail.position = coord
    tail.draw()
  head.draw()

@pyglet.clock.schedule
def update(dt):
  #global hx, hy, coords, direction
  global coords
  head.x += math.cos(head.rotation * math.pi / 180) * 100 * dt
  head.y -= math.sin(head.rotation * math.pi / 180) * 100 * dt
  head.rotation += 200.0 * turn * dt
  coords.append(head.position)
  coords = coords[-length:]

pyglet.app.run()
