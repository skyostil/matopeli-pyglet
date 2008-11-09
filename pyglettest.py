#!/usr/bin/python
import pyglet
import random

win = pyglet.window.Window(width=640, height=480)
sprite = pyglet.sprite.Sprite(pyglet.image.load('sprite.png'))
sprites = [
  pyglet.sprite.Sprite(pyglet.image.load('sprite.png'), x = random.randint(0, 640), y = random.randint(0, 480))
  for i in range(10)
]
acc = [[random.random() * 2 - 1, 0.0] for i in range(10)]

@win.event
def on_mouse_motion(x, y, dx, dy):
  sprite.position = (x, y)

@win.event
def on_draw():
  win.clear()
  sprite.draw()
  [s.draw() for s in sprites]

@pyglet.clock.schedule
def update(dt):
  for i in range(10):
    sprites[i].x += acc[i][0]
    sprites[i].y += acc[i][1]
    acc[i][1] -= 0.1
    if sprites[i].y < 0:
      acc[i][1] *= -1
    if sprites[i].x < 0 or sprites[i].x > 640:
      acc[i][0] *= -1

pyglet.app.run()
