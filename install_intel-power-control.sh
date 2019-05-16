#!/bin/bash

git clone https://github.com/jmechnich/intel-power-control.git
cd intel-power-control
make
sudo make install
gnome-terminal -e intel-power-control
