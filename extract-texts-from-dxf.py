# (C) 2018 Asher Blum
# feedme an ACAD10 DXF on stdin
# I output one line per text with height, insertion point, content

import sys

def get_texts_from_stdin():
  key = None
  pairs = []

  lineno = 0
  for line in sys.stdin:
    lineno += 1
    if line.startswith('\x1a'):
      pass
    elif key is None:
      key = int(line.strip())
    else:
      pairs.append((key, line.rstrip()))
      key = None

  ents = []
  ent = None
  for k, v in pairs:
    if k == 0:
      if ent:
        ents.append(ent)
      ent = {0: v}
    elif ent:
      ent[k] = v

  if ent:
    ents.append(ent)
    
  texts = [e for e in ents if e[0] == 'TEXT']
  return texts

# use for hacking:

def f1():
  texts = get_texts_from_stdin()
  for txt in texts:
    for k, v in sorted(txt.items()):
      print "%4d  %s" % (k, v)
    print ""

def main():
  texts = get_texts_from_stdin()
  for txt in texts:
    valign = 'b'
    halign = 'l'

    # acad10 expresses alignment with 11, 21 codes

    if txt.get(21, 0) == '2.0':
      valign = 'm'
    if txt.get(11, 0) == '2.0':
      halign = 'c'
    if txt.get(11, 0) == '4.0':
      halign = 'r'
    height = txt[40]

    print "%s %s%s %s" % (height, valign, halign, txt[1])
    
if __name__ == '__main__':
  main()
