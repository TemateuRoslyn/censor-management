kubectl apply -f storageclass.yaml -f nodeport.yaml

helm install censor-mongodb-deployment bitnami/mongodb -n censor

# mise a jour d'une chart (pas besoin de l ereinstaller)
helm upgrade censor-mongodb-deployment -f values.yaml bitnami/redis -n censor
