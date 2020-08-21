# Kill running containers
docker container kill $(docker ps -q)

# Start a container in interactive mode, mount the local volume, connect container port 8888 to local port 8888 and start jupyter lab
docker run -it -p 8888:8888 -v $(pwd):/workdir intro-to-ml-ops jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root
