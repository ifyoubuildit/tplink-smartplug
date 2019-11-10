from os import path
import os
import sys
os.chdir("/Users/branclx1/GitHub/forked/tplink-smartplug")
sys.path.append(path.abspath('../../../GitLab/personal/utils'))
from common import misc

f_list = misc.dir_list(file_dir='./output/energy',file_ext='.json')

for f in f_list:
  data = misc.file_read(fname=f,fformat='json')
  # print(data)
  for o in data:
    if len(data) == 1:
      data = data[o]
      data.update({"device":{"ip":o}})
      print(f)
      # print(data)
      misc.file_write(fname=f,fformat='json',data=data,pprint=True)


