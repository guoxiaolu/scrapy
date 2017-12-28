import os, shutil
from random import sample
path = './single_people'
save_path = './select'
prefix = 'single_people_'

if not os.path.exists(save_path):
    os.mkdir(save_path)
imgs = os.listdir(path)
samples = sample(imgs, 200)

for i, img in enumerate(samples):
    src_name = os.path.join(path, img)
    dst_name = os.path.join(save_path, '%s%04d.jpg'%(prefix, i))
    shutil.copy(src_name, dst_name)
