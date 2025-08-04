#! /bin/csh -fv
#ifort -mcmodel medium -shared-intel cea2.f -o cea2.x -w
gfortran cea2.f -o cea2.x -w
