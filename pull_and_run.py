#!/usr/bin/env python
import sys
import os
import subprocess
import shutil

# Team 3 - https://github.com/mihajlolukic12/hackathonEnergy
# Maker  - https://github.com/dusansimic/hackathon2018
# py.yeet - https://github.com/Selich/TyphoonHackathon2018
# Lambda - https://github.com/nmilosev/lphpub
# CodeAmplifiers - https://github.com/SrdjanPaunovic/Hackathon2018
# SWeet - https://github.com/phuskus/pyhackathon18.git
# Zelena Jabuka - https://bitbucket.org/vladimirvincan/pythonhackathon2018/src/master/
# CodeBanders - https://github.com/stevanmatovic/hakalaka2018
# Data Vaders - https://gitlab.com/nemanja-m/hil-hackathon
# K33 - https://github.com/stevorackovic/h333

if __name__ == '__main__':
    theirs = 'hackathon2018.their'
    os.system('git reset --hard')
    subprocess.run(['git', 'clone', sys.argv[1], theirs])

    # Remove ours requirements file
    os.remove('requirements.txt')
    # Get theirs
    shutil.copyfile(os.path.join(theirs, 'requirements.txt'),
                    'requirements.txt')

    # Remove our hackathon/solution
    shutil.rmtree(os.path.join('hackathon', 'solution'))
    # Get their hackathon/solution
    shutil.copytree(os.path.join(theirs, 'hackathon', 'solution'),
                    os.path.join('hackathon', 'solution'))

    # Remove their repository completely
    if sys.platform.startswith('win'):
        os.system('rmdir /S /Q "{}"'.format(theirs))
    else:
        shutil.rmtree(theirs)

    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    subprocess.run(['python', 'run.py'])
