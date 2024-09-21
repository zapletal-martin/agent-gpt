
FROM python:3.11-slim-bookworm

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get update && apt-get -y update
RUN apt-get install -y sudo git npm vim nano curl wget git-lfs

RUN adduser --disabled-password --gecos '' langchain
RUN adduser langchain sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER langchain
WORKDIR /home/langchain

RUN pip install --upgrade pip
RUN pip install langchain langchain-core langchain-community langchain-experimental langgraph langchain-openai langchainhub
RUN pip install faiss-cpu
RUN pip install numpy pandas matplotlib seaborn scikit-learn requests urllib3 nltk pillow pytest beautifulsoup4 python-dotenv

ADD ./data/products.txt ./data/products.txt

CMD ["/bin/bash"]
