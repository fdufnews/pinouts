#!/bin/env python3
import os
import sys

def main():
    filemask = '_pins.py'
    defaultargs = ['', '--all']
    filelist =[]
    with os.scandir() as it:
        for entry in it:
            if entry.name.endswith(filemask):
                filelist.append(entry.name)

    if len(filelist) == 0:
        print('No {} files in this directory'.format(filemask))
        exit(1)
    filelist.sort()
#    print(filelist)
#    print('\n\r')
#    print(sys.argv)
    
    count = 1
    for file in filelist:
        print('[{:2d}] - {:20s}'.format(count, file), end='    ')
        count += 1
        if (count - 1) % 3 == 0:
            print('\n\r')
    if len(sys.argv) < 2:
        print('\n\rNo given arguments. Default arguments will be used ')
        args = defaultargs
    else:
        print('Given arguments will be used ')
        args = sys.argv
    print(args)
    entry = None
    while entry not in range(0, len(filelist)+1):
        prompt = 'Enter a number between 1 and {} or 0 to exit:'.format(len(filelist))
        try:
            entry = int(input(prompt))
        except:
            print('Please enter a number')
    if entry > 0:
        entry -= 1
        args[0] = filelist[entry]
        print('Will execute: {} {}'.format(filelist[entry], args))
        os.execv(filelist[entry], args)
    
if __name__ == "__main__":
    main()    
