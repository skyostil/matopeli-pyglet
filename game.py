#!/usr/bin/python
import pyglet
import random
import math

win = pyglet.window.Window(width = 640, height = 480)
pallo = pyglet.image.load('pallo.png')
kaarme = pyglet.sprite.Sprite(pyglet.image.load('paa.png'))
tausta = pyglet.sprite.Sprite(pyglet.image.load('tausta.png'))
omppu = pyglet.sprite.Sprite(pyglet.image.load('omppu.png'))
hantaKuvat = pyglet.graphics.Batch()
hanta = []
pituus = 20
suunta = 0

kaarme.position = (320, 240)
pallo.anchor_x, pallo.anchor_y = (16, 16)
kaarme.image.anchor_x, kaarme.image.anchor_y = (16, 16)
omppu.position = random.random() * 500, random.random() * 300

efekti = pyglet.media.load('efekti1.ogg', streaming = False)
musiikki = pyglet.media.load('menuman.ogg')
musiikki.play()

@win.event
def on_key_press(key, modifiers):
  global suunta
  if key == pyglet.window.key.LEFT:
    suunta = -1
  elif key == pyglet.window.key.RIGHT:
    suunta = 1

@win.event
def on_key_release(key, modifiers):
  global suunta
  suunta = 0

@win.event
def on_draw():
  win.clear()
  tausta.draw()
  omppu.draw()
  hantaKuvat.draw()
  kaarme.draw()

@pyglet.clock.schedule
def update(dt):
  global hanta, pituus
  kaarme.x += math.cos(kaarme.rotation * math.pi / 180) * 100 * dt
  kaarme.y -= math.sin(kaarme.rotation * math.pi / 180) * 100 * dt
  kaarme.rotation += 200.0 * suunta * dt
  hanta.append(pyglet.sprite.Sprite(pallo, batch = hantaKuvat, x = kaarme.x, y = kaarme.y))
  hanta = hanta[-pituus:]

  for i, osa in enumerate(hanta):
    osa.visible = not i % 10
    if osa.visible and i < len(hanta) - 20 and \
       kaarme.x > osa.x - 16 and kaarme.y > osa.y - 16 and \
       kaarme.x < osa.x + 16 and kaarme.y < osa.y + 16:
      win.close()
      break

  if kaarme.x > omppu.x and kaarme.y > omppu.y and \
     kaarme.x < omppu.x + omppu.width and kaarme.y < omppu.y + omppu.height:
    omppu.position = random.random() * 500, random.random() * 300
    pituus += 20
    efekti.play()

pyglet.app.run()
