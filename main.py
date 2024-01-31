from os import mkdir, getenv, system
from subprocess import check_output
from os.path import isdir, isfile
from sys import argv, exit
from json import loads

def download_image(id: int):
    '''
    download_image(id) -> downloads the image of the comic corresponding to the id entered
    '''

    img_src = loads(check_output(["curl", "-s", f"https://xkcd.com/{id}/info.0.json"]).decode('utf-8'))['img']
    img_ext = img_src.split('.')[len(img_src.split('.')) - 1]

    # cache image
    if isdir(f"/home/{getenv('USER')}/.cache/kitty-xkcd") != True:
        mkdir(f"/home/{getenv('USER')}/.cache/kitty-xkcd")

    if isfile(f"/home/{getenv('USER')}/.cache/kitty-xkcd/{id}.{img_ext}") != True:
        prcs = check_output(['curl', '-s', img_src, '-o' , f'/home/{getenv("USER")}/.cache/kitty-xkcd/{id}.{img_ext}'])
    
    return system(f"kitty +kitten icat /home/{getenv('USER')}/.cache/kitty-xkcd/{id}.{img_ext}")

def local_cache(id: int):
    '''
    local_cache(id: int): check that if any image corresponds to the comic id is cached or not
    '''
    if isdir(f'/home/{getenv("USER")}/.cache/kitty-xkcd'):
        data = check_output(['ls', f'/home/{getenv("USER")}/.cache/kitty-xkcd']).decode('utf-8').split()
    else:
        return 1

    for i in data:
        if i.split('.')[0] == str(id):
            system(f"kitty +kitten icat /home/{getenv('USER')}/.cache/kitty-xkcd/{i}")
            return 0

    return 1

try:
    if __name__ == "__main__":
        '''
        We can use the TERM environment variable to get what terminal emulator we are using
        kitty sets the TERM environment variable to xterm-kitty and we are gonna get this env var and check it to see if its kitty
        This script is using kitty +kitten icat to view the comics
        '''
        if "kitty" not in getenv("TERM"):
            print(f"\x1b[31;1mError\x1b[0m: terminal emulator is not kitty")
            exit(1)

        if argv[1] not in ["help", "-h", "--help"]:
            if int(argv[1]) not in range(1, 2888):
                print(f"\x1b[31;1mError\x1b[0m: Please enter a number between 1 to 2887")
            else:
                if local_cache(int(argv[1])) == 1:
                    download_image(int(argv[1]))
        else:
            print("kitty-xkcd: view xkcd comics through kitty")
            print("==========================================")
            print("Usage: kitty-xkcd comic_id")
            print("  - comic_id is the id of the comic")
except (KeyboardInterrupt, Exception):
    print("\x1b[31;1mError\x1b[0m: An exception occured")
    exit(1)
