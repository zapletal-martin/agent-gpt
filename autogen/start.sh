#!/bin/sh

docker run -it -v `pwd`:/myapp autogen_full_img:latest python /myapp/prisoner_dillema.py
