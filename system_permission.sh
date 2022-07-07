#!/bin/bash

cd
# Here is your scripts' installation path
search_dir=/user/local/lib/python3.8

# or find it by using python command
# python_site_dir=$(python3 -c 'import iwb_ros.setting; iwb_ros.setting.get_script_dir()')
python_site_dir=$(python3 -c 'import iwb_ros.setting; iwb_ros.setting.bash_strout("script_dir")')

echo "$python_site_dir"
# python_site_dir=$(python3 -c 'import os; import iwb_ros; print(os.path.abspath(iwb_ros.__path__))')
# python_site_dir=$(python3 -c 'import os; import iwb_ros; print(os.path.abspath(iwb_ros.__file__)site.getsitepackages())')

for entry in "$python_site_dir"/*
do
  echo "$entry"
  sudo chmod +x $entry
done


#local_script=$HOME/my_pkg/iwb_ros/script

#for entry in "$local_script"/*
#do
#  echo "$entry"
#  sudo chmod +rwx $entry
#done

# don not use sudo to run this script!!!
echo $HOME

# calcmodpara

