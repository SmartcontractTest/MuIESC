import configparser
import codecs
from pathlib import Path

import Mu

cp = configparser.SafeConfigParser()
with codecs.open('Config.conf', 'r', encoding='utf-8') as f:
    cp.readfp(f)

sourecepath = cp.get('sourcepath', 'path')
targetpath = cp.get('targetpath', 'path')


def Mut(spath, tpath):
    path = Path(spath)
    all_sol_file = list(path.glob('**/*.sol'))
    for sol_file in all_sol_file:
        solpath = str(sol_file.parent) + '/' + str(sol_file.name)
        Mu.p(solpath, tpath)


Mut(sourecepath, targetpath)
