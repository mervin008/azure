apiVersion: apps/v1
kind: Deployment
metadata:
  name: certhub-notification-api
  namespace: notify-app
spec:
  replicas: 1 # Adjust as needed
  selector:
    matchLabels:
      app: certhub-notification-api
  template:
    metadata:
      labels:
        app: certhub-notification-api
    spec:
      imagePullSecrets:
        - name: regcred 
      containers:
        - name: certhub-notification-api
          image: certhub-notification-api:latest  # Replace with your image
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: secret-volume
              mountPath: /etc/secret
              readOnly: true
      volumes:
        - name: secret-volume
          secret:
            secretName: api-key
---
apiVersion: v1
kind: Service
metadata:
  name: certhub-notification-api-service
  namespace: notify-app
spec:
  selector:
    app: certhub-notification-api
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
---
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: certhub-notification-api-gateway
  namespace: notify-app
spec:
  selector:
    istio: ingressgateway # Assumes your ingress gateway has this label
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE 
        credentialName: tls-keys 
      hosts:
        - api.email.at.com
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: certhub-notification-api-virtualservice
  namespace: notify-app
spec:
  hosts:
    - api.email.at.com
  gateways:
    - certhub-notification-api-gateway
  http:
    - match:
      - uri:
          prefix: /
      route:
        - destination:
            host: certhub-notification-api-service
            port:
              number: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: certhub-notification-api
  namespace: notify-app
spec:
  replicas: 1 
  selector:
    matchLabels:
      app: certhub-notification-api
  template:
    metadata:
      labels:
        app: certhub-notification-api
    spec:
      imagePullSecrets:
        - name: regcred 
      containers:
        - name: certhub-notification-api
          image: certhub-notification-api:latest
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: secret-volume
              mountPath: /etc/secret # Mount the secret here
              readOnly: true 
      volumes:
        - name: secret-volume
          secret:
            secretName: api-key  # Your secret name
