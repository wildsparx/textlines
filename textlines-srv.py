# (C) 2017 Asher Blum
import flask
import json
import logging
import os
import re
import StringIO

from apbhershey import HersheyPainter
from dxf import DXFDoc


APP = flask.Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = BASE_DIR + "/fonts.json"
FONTS = json.load(open(FONT_FILE))
LISTEN_PORT = 8020

logging.basicConfig(filename=os.path.join(BASE_DIR, 'textlines.log'),level=logging.DEBUG)

logger = logging.getLogger(__name__)

#http://localhost:5000/?txt=ABCewrewrewr&height=1&xsf=0.8&halign=left&valign=mid

SCHEMA = [
    ('txt',     re.compile(r'[ -~]{1,100}$')), # all printable ASCII chars
    ('halign',  re.compile(r'left|center|right$')),
    ('valign',  re.compile(r'top|mid|bottom')),
    ('height',  (0.0, 1000.0)),
    ('xsf',     (0.001, 1000.0)),
    ('kern',     (-2.0, 2.0)),
]

class Request(object):
  def __init__(self):
    self.valid = False

def text_to_dxf(txt='ABC', font_name='romans', sf=1.0, xsf=1.0, kern=0.0, valign="m",
                halign="c"):
  font = FONTS[font_name]
  painter = HersheyPainter()
  painter.begin(font, x=0, y=0, sf=sf, xsf=xsf, kern=kern)
  painter.draw_str(txt)
  lines = painter.get_aligned_lines(valign=valign, halign=halign)
  dxfdoc = DXFDoc('output.dxf')
  for line in lines:
    dxfdoc.line(*line)
  return str(dxfdoc)

def validate_one(params, key, rule, req):
  '''Validate one field, copying its value to req; return list of errors'''

  if not key in params: 
    return ["Missing %s" % key]

  if hasattr(rule, 'match'):
    if not rule.match(params[key]):
      return ["Invalid %s" % key]
    setattr(req, key, params[key])

  if type(rule) == tuple:
    fval = 0.0

    try:
      fval = float(params[key])
      setattr(req, key, fval)
    except:
      return ["Invalid %s" % key]

    minval, maxval = rule

    if fval < minval:
      return ["%s must be at least %s" % (key, minval)]
    if fval > maxval:
      return ["%s must be less than %s" % (key, maxval)]
  return []
      

def validate(params):
  '''Validate expected params, ignoring extras; return (errstr, Request)'''
  req = Request()
  errors = [validate_one(params, key, rule, req) for key, rule in SCHEMA]
  errors = sum(errors, [])
  estr = '; '.join(errors)
  if not estr:
    req.valid = True
  return (estr or None, req)

def str_to_filename(s):
  '''Return a safe DXF filename based on a string'''
  s = re.sub(r'[^\w-]+', '_', s)
  return s[:30] + ".dxf"
  

@APP.route("/textlines", methods=['GET','POST'])
def index():
  if flask.request.method == 'POST':
    errstr, req = validate(flask.request.form)
    if req.valid:
      dxfstr = text_to_dxf(txt=req.txt, sf=req.height, xsf=req.xsf,
                           kern=req.kern, valign=req.valign[0],
                           halign=req.halign[0])
      return flask.send_file(
          filename_or_fp=StringIO.StringIO(dxfstr),
          mimetype="Application/DXF",
          as_attachment=True,
          attachment_filename=str_to_filename(req.txt)
      )
    else:
      return flask.render_template('main.html', error=errstr)

  return flask.render_template('main.html')

if __name__ == "__main__":
  APP.debug = False
  APP.run(host='0.0.0.0', port=LISTEN_PORT)

