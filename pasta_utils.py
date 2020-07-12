import email
import requests
import subprocess
import os

'''
patches = [
    'https://lore.kernel.org/lkml/20200710084841.1933254-1-yanziily@gmail.com/raw',
    'https://lore.kernel.org/lkml/8325438e25a3a5a7e6d12ef6ede8f4350e4c65be.1594500029.git.mail@maciej.szmigiero.name/raw',
    'https://lore.kernel.org/lkml/20200619224334.GA7857@embeddedor/raw',
    'https://lore.kernel.org/lkml/f4297017-1d27-741d-3abc-36b6918801f6@linuxfoundation.org/raw',
    'https://lore.kernel.org/lkml/20200710092035.28919-1-ethercflow@gmail.com/raw',
    'https://lore.kernel.org/lkml/20200708202650.GA3866@embeddedor/raw',
    'https://lore.kernel.org/lkml/20200710183350.GA8376@embeddedor/raw',
    'https://lore.kernel.org/lkml/20200707212954.26487-1-oshpigelman@habana.ai/raw',
    'https://lore.kernel.org/lkml/20200710051043.899291-1-kamalesh@linux.vnet.ibm.com/raw',
    'https://lore.kernel.org/lkml/20200710152559.1645827-1-vkuznets@redhat.com/raw'
]
'''
path_get_maintainer = "scripts/get_maintainer.pl"

src_tree_path = "/home/dark_matter/linux_work/linux_mainline/"

func = lambda s : s.strip()

def parse_one(id):
    id = id.strip()
    for i in list(id.split(' ')):
        if '@' in i:
            if i[0] == '<':
                i = i[1:]
            if i[-1] == '>':
                i = i[:-1]
            return i


def parse_all(text):
    l = list(text.split('\n'))
    l = list(map(func, l))
    ans = []
    for i in l:
        li = list(i.split(','))
        if len(li):
            for i in range(len(li)):
                li[i] = li[i].strip()
            ans += li
    l = []
    for i in ans:
        if len(i):
            l.append(i)
    
    ans = []
    for i in l:
        parsed_id = parse_one(i)
        if parsed_id:
            ans.append(parsed_id)
    
    return ans


def get_sent_ids(patch_url):
    
    mail = email.message_from_string(requests.get(patch_url).text)
    
    return parse_all(mail['To'])+parse_all(mail['Cc'])



def get_gm_ids(patch_url):
    
    with open(f'{src_tree_path}pasta-patches/buffer.patch', 'w') as f:
        f.write(requests.get(patch_url).text)
    
    proc = subprocess.Popen([f"{src_tree_path}{path_get_maintainer}", f"{src_tree_path}pasta-patches/buffer.patch"],  stdout=subprocess.PIPE)
    email_ids, err = proc.communicate()
    email_ids = str(email_ids.decode('utf-8'))
    os.system(f"rm {src_tree_path}pasta-patches/buffer.patch")
    
    return parse_all(email_ids)
