kubectl apply  -f storageclass.yaml -f nodeport.yaml
helm install censor-redis-deployment -f value.yaml bitnami/redis -n censor

# mise a jour d'une chart (pas besoin de l ereinstaller)
helm upgrade censor-redis-deployment -f values.yaml bitnami/redis -n censor
