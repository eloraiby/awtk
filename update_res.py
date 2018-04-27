#!/usr/bin/python

import os
import glob
import shutil
import platform
import copy

def joinPath(root, subdir):
  return os.path.normpath(os.path.join(root, subdir))

DPI='x1'
CWD=os.getcwd()
BIN_DIR=joinPath(CWD, 'bin')
APP_DIR=joinPath(CWD, 'demos')
INPUT_DIR=joinPath(APP_DIR, 'res/raw')
OUTPUT_DIR=joinPath(APP_DIR, 'res/inc')
RESOURCE_C=joinPath(APP_DIR, 'resource.c')

def buildTools():
  os.system('scons bin/resgen')
  os.system('scons bin/fontgen')
  os.system('scons bin/themegen')
  os.system('scons bin/imagegen')
  os.system('scons bin/xml_to_ui')

def buildAll():
  os.system('scons')

def removeDir(path):
  if os.path.isdir(path):
     print('rmdir:' + path);
     shutil.rmtree(path)

def prepare():
  removeDir(OUTPUT_DIR)
  os.makedirs(joinPath(OUTPUT_DIR, 'theme'));
  os.makedirs(joinPath(OUTPUT_DIR, 'images'));
  os.makedirs(joinPath(OUTPUT_DIR, 'fonts'));
  os.makedirs(joinPath(OUTPUT_DIR, 'ui'));

def themegen(raw, inc):
  os.system(joinPath(BIN_DIR, 'themegen') + ' ' + joinPath(INPUT_DIR, raw) + ' ' + joinPath(OUTPUT_DIR, inc))

def resgen(raw, inc):
  os.system(joinPath(BIN_DIR, 'resgen') + ' ' + joinPath(INPUT_DIR, raw) + ' ' + joinPath(OUTPUT_DIR, inc))

def fontgen(raw, text, inc, size):
  os.system(joinPath(BIN_DIR, 'fontgen') + ' ' + joinPath(INPUT_DIR, raw) + ' ' + joinPath(INPUT_DIR, text) +' ' + joinPath(OUTPUT_DIR, inc) + ' ' + str(size))

def imagegen(raw, inc):
  print(joinPath(BIN_DIR, 'imagegen') + ' ' + raw + ' ' + inc)
  os.system(joinPath(BIN_DIR, 'imagegen') + ' ' + raw + ' ' + inc)

def xml_to_ui(raw, inc):
  os.system(joinPath(BIN_DIR, 'xml_to_ui') + ' ' + raw + ' ' + inc)

def gen_all():
  themegen('theme/theme.xml', 'theme/default.data');
  resgen('fonts/font.ttf', 'fonts/default_ttf.data');
  resgen('fonts/action_protocol.ttf', 'fonts/ap.data');
  fontgen('fonts/font.ttf', 'fonts/text.txt', 'fonts/default.data', 20);

  for f in glob.glob(joinPath(INPUT_DIR, 'images/'+DPI+'/*.*')):
    inc=copy.copy(f);
    raw=copy.copy(f);
    basename=os.path.basename(inc);
    inc=joinPath(OUTPUT_DIR, 'images/'+basename);
    inc=inc.replace('.png', '.data')
    inc=inc.replace('.jpg', '.data')
    imagegen(raw, inc)

  for f in glob.glob(joinPath(INPUT_DIR, 'ui/*.xml')):
    inc=copy.copy(f);
    raw=copy.copy(f);
    inc=inc.replace('.xml', '.data')
    inc=inc.replace(INPUT_DIR, OUTPUT_DIR)
    xml_to_ui(raw, inc)

def writeResult(str):
  fd = os.open(RESOURCE_C, os.O_RDWR|os.O_CREAT|os.O_TRUNC)
  os.write(fd, str)
  os.close(fd)

def gen_res_c():
  result = '#include "tk.h"\n'
  result += '#include "base/resource_manager.h"\n'

  files=glob.glob(joinPath(OUTPUT_DIR, '**/*.data'))
  for f in files:
    incf = copy.copy(f);
    incf=incf.replace(APP_DIR, ".");
    incf=incf.replace('\\', '/');
    incf=incf.replace('./', '');
    result += '#include "'+incf+'"\n'

  result += '\n';
  result += 'ret_t resource_init(void) {\n'
  result += '  resource_manager_init(30);\n\n'
  result += ''

  for f in files:
    incf = copy.copy(f);
    basename = incf.replace(OUTPUT_DIR, '.');
    basename = basename.replace('\\', '/');
    basename = basename.replace('./', '');
    basename = basename.replace('/', '_');
    basename = basename.replace('fonts', 'font');
    basename = basename.replace('images', 'image');
    basename = basename.replace('.data', '');
    result += '  resource_manager_add('+basename+');\n'

  result += '\n'
  result += '  tk_init_resources();\n'
  result += '  return RET_OK;\n'
  result += '}\n'
  writeResult(result);

def run():
  buildTools()
  prepare()
  gen_all()
  gen_res_c()
  buildAll()

run()

