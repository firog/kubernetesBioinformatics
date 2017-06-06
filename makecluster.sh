#!/bin/bash
read -p "Full path to service account key (credentials file created on the google cloud dashboard): " path_to_pem
if [ -f $path_to_pem ]
then
  read -p "Desired name of cluster: " clustername
  read -p "Zone to spawn cluster (default is europe-west1-b): " zone
  zone=${zone:-europe-west1-b}
  read -p "Number of nodes (default is 2): " num_nodes
  num_nodes=${num_nodes:-2}
  read -p "Machine type (default is n1-standard-2): " machine_type
  machine_type=${machine_type:-n1-standard-2}

  volumename=$clustername"container"
  docker volume create --name $volumename
  docker_volume_dest=$(docker inspect $volumename | grep -Po '(?<="Mountpoint": ")[^"]*')
  sudo cp $path_to_pem $docker_volume_dest/
  echo "Creating temporary container."
  docker run -a STDOUT -v $volumename:/shared -e ZONE=$zone -e CLUSTERNAME=$clustername -e NUM_NODES=$num_nodes -e MACHINE_TYPE=$machine_type -e PATH_TO_PEM=$path_to_pem --name makecluster$clustername firog/test-makecluster
else
  echo "Please enter existing path to service account key."
fi

docker rm makecluster$clustername
docker volume rm $volumename
