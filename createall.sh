#!/bin/bash
read -p "Desired name of cluster: " clustername
read -p "Zone to spawn cluster (default is europe-west1-b): " zone
zone=${zone:-europe-west1-b}
read -p "Number of nodes (default is 2): " num_nodes
num_nodes=${num_nodes:-2}
read -p "Machine type (default is n1-standard-2): " machine_type
machine_type=${machine_type:-n1-standard-2}
read -p "Full path to pem file: " path_to_pem

docker volume create --name makeclusterv
docker_volume_dest=$(docker inspect makeclusterv | grep -Po '(?<="Mountpoint": ")[^"]*')
sudo cp $path_to_pem $docker_volume_dest/
docker run -a STDOUT -v makeclusterv:/shared -e ZONE=$zone -e CLUSTERNAME=$clustername -e NUM_NODES=$num_nodes -e MACHINE_TYPE=$machine_type -e PATH_TO_PEM=$path_to_pem --name makecluster firog/test-makecluster
