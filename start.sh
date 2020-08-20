#docker run -p 8888:8888 -v $(pwd):/workdir intro-to-ml-ops

docker run -it -p 8888:8888 -v $(pwd):/workdir intro-to-ml-ops jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root
