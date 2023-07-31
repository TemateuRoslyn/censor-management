kubectl apply -f nodeport.yaml

helm install censor-mongodb-deployment -f values.yaml bitnami/mongodb -n censor

# mise a jour d'une chart (pas besoin de l ereinstaller)
helm upgrade censor-mongodb-deployment -f values.yaml bitnami/redis -n censor
