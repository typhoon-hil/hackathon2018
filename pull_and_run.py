#!/usr/bin/env python
import sys
import os
import subprocess
import shutil

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
