#!/usr/bin/python
# -*- encoding: iso8859-1 -*-
#
#  Matopeli (C) 2008 Sami Ky�stil� <sami.kyostila@gmail.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#

import pyglet
import random
import math

# Avataan ikkuna
win = pyglet.window.Window(width = 640, height = 480)

# Ladataan grafiikka
pallo = pyglet.image.load('pallo.png')
mato = pyglet.sprite.Sprite(pyglet.image.load('paa.png'))
tausta = pyglet.sprite.Sprite(pyglet.image.load('tausta.png'))
omppu = pyglet.sprite.Sprite(pyglet.image.load('omppu.png'))

# Alustetaan madon tiedot
hanta = []
pituus = 20
suunta = 0
mato.position = (320, 240)
pallo.anchor_x, pallo.anchor_y = (16, 16)
mato.image.anchor_x, mato.image.anchor_y = (16, 16)
hantaOsat = pyglet.graphics.Batch()

# Arvotaan omenalle paikka
omppu.position = random.random() * 500, random.random() * 300

# Ladataan ��niefektit ja musiikki
efektit = [
    pyglet.media.load('efekti1.ogg', streaming = False),
    pyglet.media.load('efekti2.ogg', streaming = False),
    pyglet.media.load('efekti3.ogg', streaming = False),
]
musiikki = pyglet.media.load('menuman.ogg')

# Laitetaan musiikki soimaan
musiikki.play()

@win.event
def on_key_press(key, modifiers):
  """K�sittelee n�pp�inpainallukset"""
  global suunta
  if key == pyglet.window.key.LEFT:
    suunta = -1
  elif key == pyglet.window.key.RIGHT:
    suunta = 1

@win.event
def on_key_release(key, modifiers):
  """K�sittelee n�pp�inten vapautukset"""
  global suunta
  suunta = 0

@win.event
def on_draw():
  """Piirt�� ikkunan sis�ll�n"""
  win.clear()
  tausta.draw()
  omppu.draw()
  hantaOsat.draw()
  mato.draw()

  # Piirret��n pistelaskuri
  pyglet.text.Label("%d" % (pituus - 20), font_size = 32, x = 25, y = 25).draw()

@pyglet.clock.schedule
def update(dt):
  """P�ivitt�� animaation"""
  global hanta, pituus

  # Siirret��n madon p��t� eteenp�in
  mato.x += math.cos(mato.rotation * math.pi / 180) * 100 * dt
  mato.y -= math.sin(mato.rotation * math.pi / 180) * 100 * dt

  # K��nnet��n kulkemissuuntaa
  mato.rotation += 200.0 * suunta * dt

  # Lis�t��n uusi h�nt�kappale
  hanta.append(pyglet.sprite.Sprite(pallo, batch = hantaOsat, x = mato.x, y = mato.y))
  hanta = hanta[-pituus:]

  # K�yd��n kaikki h�nt�kappaleet l�pi
  for i, osa in enumerate(hanta):
    # N�ytet��n vain joka kymmenes h�nn�n osa
    osa.visible = not i % 10

    # Jos p�� t�rm�si h�nt��n, peli loppuu
    if osa.visible and i < len(hanta) - 30 and \
       mato.x > osa.x - 16 and mato.y > osa.y - 16 and \
       mato.x < osa.x + 16 and mato.y < osa.y + 16:
      print "Kuolit! %d pojoa" % (pituus - 20)
      win.close()
      break

  # Jos p�� osui omppuun, siirret��n se uuteen paikkaan ja kasvatetaan matoa
  if mato.x > omppu.x and mato.y > omppu.y and \
     mato.x < omppu.x + omppu.width and mato.y < omppu.y + omppu.height:
    omppu.position = random.random() * 500, random.random() * 300
    pituus += 20
    # Soitetaan satunnainen ��niefekti
    random.choice(efektit).play()

# K�ynnistet��n pelimoottori
pyglet.app.run()
