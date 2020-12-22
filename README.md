This is the repo for the microservice that will allow communication between tenant and management.

To run the Dynamo service, export ACCESS_ID=<access key> and export ACCESS_KEY=<secret key>
Where <access key> is your IAM access key and <secret key> is your IAM secret key. 
  
To run, enter python app.py into the terminal and it'll start on 0.0.0.0:8000

To run locally run:
```
docker run -p 80:80 -e ACCESS_ID=<insert access id> -e ACCESS_KEY=<insert access key> e6156-comments-service
```

To make changes to image:
```
docker build -t 6156-comments-service .
```

To push changes to docker file:
```
docker tag e6156-comments-service 318810397967.dkr.ecr.us-east-1.amazonaws.com/e6156:e6156-comments-service
```

```
docker push 318810397967.dkr.ecr.us-east-1.amazonaws.com/e6156
```
