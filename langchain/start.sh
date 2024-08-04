#!/bin/sh

docker run -it -v `pwd`:/myapp langchain:latest python /myapp/agent_math.py
