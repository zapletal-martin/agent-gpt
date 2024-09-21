#!/bin/sh

docker run -it -v `pwd`:/myapp langchain:latest python /myapp/agent_rag.py
