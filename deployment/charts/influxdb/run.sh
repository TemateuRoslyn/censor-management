kubectl apply  -f pv.yaml 
helm install censor-influxdb-deployment -f value.yaml bitnami/influxdb -n censor
