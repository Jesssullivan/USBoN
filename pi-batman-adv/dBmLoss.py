# estimate free space dBm attenuation
# (Pi wifi module BCM43143)
# a WIP for the D&M Makerspace @ github/jesssullivan

from math import log10
from sys import argv

'''
Tx = 19~20 dBm
Rx = not clear how low we can go here
d = distance Tx --> Rx
f = frequency
c = attenuation constant: meters / MHz = -27.55
#    see here for more info:
#    https://en.wikipedia.org/wiki/Free-space_path_loss
'''

f = 2400  # MHz
c = 27.55 # RF attenuation constant (in meters / MHz)

def_Tx = 20  # expected dBm transmit
def_Rx = 40  # (absolute value) of negative dBm thesh

def logdBm(num):
    return 20 * log10(num)

def maxDist(Rx, Tx):
    dBm = 0
    d = .1  # meters!
    while dBm < Tx + Rx:
        dBm = logdBm(d) + logdBm(f) - Tx - Rx + c
        d += .1  # meters!
    return d

# Why not use this with arguments Tx + Rx from shell if we want:
def useargs():
    use = bool
    try:
        if len(argv) == 3:
            use = True
        elif len(argv) == 1:
            print('\n\nyou can add (default) Rx Tx arguments using the following syntax: \n \
                python3 dBmLoss.py 20 40 \n \
                python3 dBmLoss.py <Rx> <Tx> \
                \n')
            use = False
        else:
            print('you must use both Rx & Tx arguments or no arguments')
            raise SystemExit
    except:
        print('you must use both Rx & Tx arguments or no arguments')
        raise SystemExit
    return use

def main():

    if useargs() == True:
        arg = [int(argv[1]), int(argv[2])]
    else:
        arg = [def_Rx, def_Tx]

    print(str('\n ' + str(maxDist(arg[0], arg[1])*3.281) + \
        ' ft = max. mesh node spacing, @ \n' + \
        ' Rx = ' + str(arg[0]) + '\n' + \
        ' Tx = ' + str(arg[1])))

main()
