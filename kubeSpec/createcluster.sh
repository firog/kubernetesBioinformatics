#!/bin/bash

kubectl delete service rabbitmq-service
kubectl delete rc rabbitmq-controller
kubectl delete rc celery-controller
kubectl delete deployments test-app

kubectl create -f rabbitmq-service.yaml
kubectl create -f rabbitmq-controller.yaml
#kubectl create -f app-controller.yaml
kubectl run test-app --image=firog/test-app --port=5000
#kubectl expose deployment test-app --type=NodePort
