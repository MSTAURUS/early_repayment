docker build -t opencalc ./ && \
docker save -o ./opencalc.tar opencalc && \
docker stop $(docker ps -a -q) && \
docker rm $(docker ps -a -q) && \
docker rmi $(docker images -a -q) 
