#!/bin/bash

echo 550 | sudo tee /sys/class/drm/card0/gt_max_freq_mhz /sys/class/drm/card0/gt_boost_freq_mhz
