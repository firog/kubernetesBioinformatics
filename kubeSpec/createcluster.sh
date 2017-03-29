#!/bin/bash

kubectl delete services rabbitmq-service
kubecl delete services myapp
kubectl delete rc rabbitmq-controller
kubectl delete rc celery-controller
kubectl delete deployments myapp

#./cleanall.sh

kubectl create -f rabbitmq-service.yaml
kubectl create -f rabbitmq-controller.yaml
#sleep 10
kubectl create -f app-service.yaml
kubectl create -f app-deployment.yaml
#kubectl create -f app-controller.yaml
#kubectl run test-app --image=firog/test-app --port=5000
#kubectl expose deployment test-app --type=NodePort
