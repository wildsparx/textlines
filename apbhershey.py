# (C) 2017 Asher Blum
# string -> list<line>
# font is mapping of charcode ->
# (-8, 9)  [[(-5, -5), (6, 9)], [(6, -5), (-5, 9)]]

class HersheyPainter(object):
  '''Renders strings to lists of lines, using Hershey fonts'''
  def __init__(self):
    pass

  def begin(self, font, x, y, sf, xsf, kern):
    self.font = font
    self.x = x
    self.y = y
    self.sf = sf
    self.xsf = xsf
    self.kern = kern
    self.lines = []
    self._get_m_height()

  def draw_str(self, s):
    for c in s:
      self.draw_char(ord(c))
    
  def _get_lines(self):
    '''Return properly scaled, but not aligned lines'''
    return [[(float(v)-self.mbottom)/self.mheight for v in line] for line in self.lines]

  def get_aligned_lines(self, valign='m', halign='c'):
    '''tmb lrc'''
    lines = self._get_lines() # y from 0 to 1
    cols = zip(*lines) # transform to X0, Y0, X1, Y1 ...
    xvals = list(cols[0]) + list(cols[2])
    minx = min(xvals)
    maxx = max(xvals)
    deltax = 0.0
    deltay = 0.0

    if halign == 'l':
      deltax = -minx
    elif halign == 'r':
      deltax = -maxx
    elif halign == 'c':
      deltax = (minx+maxx)/-2

    if valign == 't':
      deltay = -1.0 * self.sf
    elif valign == 'b':
      deltay = 0
    elif valign == 'm':
      deltay = -0.5 * self.sf

    deltas = (deltax, deltay)
    ncols = [[v + deltas[i%2] for v in col] for i, col in enumerate(cols)]
    return zip(*ncols)
   
    
  def to_ps(self): # dumb and foolproof PS for testing:
    ll = ["%s %s moveto %s %s lineto stroke" % l for l in self.lines]
    return "\n".join(ll)

  def end(self):
    pass

  def _get_m_height(self):
    limits, paths = self.font[str(ord('M'))]
    points = [item for sublist in paths for item in sublist]
    ys = [p[1] for p in points]
    self.mbottom = min(ys)
    self.mheight = max(ys) - self.mbottom

  def draw_char(self, ac):
    limits, paths = self.font[str(ac)]
    width = limits[1] - limits[0]
    self.x -= limits[0] * self.sf * self.xsf # which is neg, so mv forward
    for path in paths:
      ox = None
      oy = None
      for x, y in path:
        nx = self.x + x * self.sf * self.xsf
        ny = self.y + y * self.sf
        if ox:
          self.lines.append((ox, oy, nx, ny))
        ox = nx
        oy = ny
    self.x += limits[1] * self.sf * self.xsf
    self.x += self.kern * self.mheight * self.sf
       
if __name__ == '__main__':
  d = DataOut()
