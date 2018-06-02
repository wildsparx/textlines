# (C) 2018 Asher Blum
# Feed me a file with one text per line like this:
# (height, alignment, content)
# .156 mc THIS IS TEXT
# I generate one DXF file per text

import json
import re
import sys

from dxf import DXFDoc
from apbhershey import HersheyPainter

def text_to_dxf(font, txt='ABC',  sf=1.0, xsf=1.0, kern=0, valign="m", halign="c"):
  painter = HersheyPainter()
  painter.begin(font, x=0, y=0, sf=sf, xsf=xsf, kern=kern)
  painter.draw_str(txt)
  lines = painter.get_aligned_lines(valign=valign, halign=halign)
  dxfdoc = DXFDoc('output.dxf')
  for line in lines:
    dxfdoc.line(*line)
  return str(dxfdoc)

def mk_filename(content, size_s, align):
  '''Generate a .dxf filename'''
  els = content.split() + [size_s] + [align]
  fn = '-'.join(els).lower()
  fn = re.sub(r'[^a-z0-9]+', '-', fn)
  fn = re.sub(r'^\W', '', fn)
  fn += '.dxf'
  return fn

def main():
  xsf = 0.8
  kern = 0.2
  font_name = 'romans'
  fonts = json.load(open('fonts.json'))
  font = fonts[font_name]

  for line in sys.stdin:
    # print "line=%r" % line
    size_s, align, content = line.rstrip().split(' ', 2)
    size = float(size_s)
    # print "size=%r align=%r content=%r" % (size_s, align, content)
    dxfdoc = text_to_dxf(font, content, sf=size, xsf=xsf, kern=kern, valign=align[0], halign=align[1])
    fn = mk_filename(content, size_s, align)
    open(fn, 'w').write(dxfdoc)
    print fn

if __name__ == '__main__':
  main()
