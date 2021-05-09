#!/bin/sh

#sudo find / -type f -name "JRE"
cwd=$(pwd)

# go to home and 
cd $HOME
printf "export =$cwd" >> .zshrc
#echo $cwd > .zshrc
