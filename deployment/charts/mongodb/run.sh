kubectl apply -f pv.yaml
helm install censor-mongodb-deployment bitnami/mongodb -n censor