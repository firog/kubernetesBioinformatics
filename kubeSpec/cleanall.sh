#!/bin/bash
kubectl delete rc --all
kubectl delete ing --all
kubectl delete services --all
kubectl delete deployments --all
kubectl delete pods --all
