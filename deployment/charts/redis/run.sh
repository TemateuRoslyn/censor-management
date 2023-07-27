kubectl apply -f pv.yaml -f pvc.yaml
helm install censor-redis-deployment -f value.yaml bitnami/redis -n censor