import sys
import os
import subprocess
import math
def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return iter(p.stdout.readline, b'')

if __name__=="__main__":
    print math.exp(800)


