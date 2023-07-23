kubectl apply -f pv.yaml
helm install censor-kafka-deployment bitnami/kafka -n censor
