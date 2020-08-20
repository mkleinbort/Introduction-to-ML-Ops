FROM python:3.8.5-buster

RUN apt-get update \
    && apt-get install -y git

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_12.x  | bash -
RUN apt-get -y install nodejs
RUN npm install

RUN jupyter labextension install jupyterlab-plotly  --minimize=False --no-build
RUN jupyter labextension install @aquirdturtle/collapsible_headings --minimize=False --no-build
RUN jupyter labextension install @ijmbarr/jupyterlab_spellchecker --minimize=False --no-build
RUN jupyter lab build --minimize=False


WORKDIR /workdir
CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
