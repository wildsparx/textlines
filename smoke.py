# (C) 2017 Asher Blum
import json
import re
import sys

from dxf import DXFDoc
from apbhershey import HersheyPainter

def text_to_dxf(txt='ABC', font_name='romans', sf=1.0, xsf=1.0, valign="m", halign="c"):
  fonts = json.load(open('fonts.json'))
  font = fonts[font_name]
  painter = HersheyPainter()
  painter.begin(font, x=0, y=0, sf=sf, xsf=xsf, kern=0)
  painter.draw_str(txt)
  lines = painter.get_aligned_lines(valign=valign, halign=halign)
  dxfdoc = DXFDoc('output.dxf')
  for line in lines:
    dxfdoc.line(*line)
  return str(dxfdoc)

def f5():
  buf = text_to_dxf(txt="I", sf=1.0, xsf=0.5, valign="m", halign="c")
  open('output.dxf', 'w').write(buf)

if __name__ == '__main__':
  f5()
