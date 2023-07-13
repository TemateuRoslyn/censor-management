# sudo microk8s kubectl apply -f namespace.yml -f storageClass.yml -f pvc.yml
sudo microk8s kubectl apply -f namespace.yml -f storageClass.yml -f pvc.yml -f pods.yml -f loadbalancer.yml -f clusterIp.yml -f deployment.yml
# sudo microk8s kubectl apply -f all.yml
# sudo microk8s kubectl delete -f all.yml && sudo microk8s kubectl apply -f all.yml

# exposer dashbord pour l'utiliser dans le navigateur:
# sudo kubectl proxy

# kubectl describe pods redis-deployment-546694b5db-29747 -n censor-management-space

