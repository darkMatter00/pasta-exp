import os

path = '/home/dark_matter/linux_work/linux_mainline/challenge/patches/'

patches = os.listdir(path)

cnt = 1

for patch in patches:
    print(cnt, 'done')
    os.system(f'/home/dark_matter/linux_work/linux_mainline/scripts/get_maintainer.pl {path + patch} > /home/dark_matter/linux_work/linux_mainline/challenge/gm-ans/{patch}.ans')
    cnt += 1

