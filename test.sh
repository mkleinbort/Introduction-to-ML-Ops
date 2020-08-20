#docker run -p 8888:8888 -v $(pwd):/workdir intro-to-ml-ops

docker run -it -p 8888:8888 -v $(pwd):/workdir intro-to-ml-ops pytest tests.py
