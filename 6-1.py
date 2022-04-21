import os
import argparse

path = 'Z:/Алгоритмизация и программирование/1-МД-19/Каргин/file'
if not os.path.exists(path):
    os.mkdir(path)
parser = argparse.ArgumentParser(description='A tutorial of argparse')
parser.add_argument('-n', '--name', nargs='?', default='Anonymous', help="Here's your name")
parser.add_argument('-p', '--path', help="Here's the path to your file")
parser.add_argument('-nQ', '--noQ', action="store_true", help="No more questions, mate")
parser.add_argument('-cF', '--crFile', action="store_true", help="Do u want to create file? ")
args = parser.parse_args()
print(f'Hi {args.name}!')
print(args)

if os.path.exists(args.path):
    print("U have this file\n")
else:
    if args.crFile:
        name = input("Write something\n")
        with open(args.path, "w+") as f:
            f.write(name)
    else:
        quest = input(f'\n{args.name}, do u want to create this file? (Y/N) \n').capitalize()
        if quest[0] == 'Y':
            name = input("Write something\n")
            with open(args.path, "w+") as f:
                f.write(name)
        else:
            print('Look!')

if os.path.exists(args.path):
    if args.noQ:
        os.remove(args.path)
        exit(0)
    else:
        ag = input(f'\n{args.name}, do u want to remove this file? (Y/N) ').capitalize()
        if ag[0] == 'Y':
            os.remove(args.path)
        else:
            print('Very well, I do nothing')
else:
    print("\nSorry, mate, but your file doesn't exist :P")
