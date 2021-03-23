# Digit  recognition

## Model

Model files and training notebook can be found under respective folder. For training I have used image augmentation to achieve better model regularisation. Model architecture is very common CNN architecture: feature extraction is done by 2 * (Conv2D + MaxPool) and classification part of the architecture is fully conntected with dropout more further regularisation. 

## Serving the model

For this project I used FastAPI to serve the model. [App.py](master/app/app,py) in app folder consists of 3 functions: 1) load_model, 2)read_imagefile, and 3)predict. API support post method that returns prediction (0-9) and the confidence (%) that model has for this prediction. 

## How to use

1. Clone repo

2. Build image using [dockerfile](master/Dockerfile) ` docker build -t digitapi:v1 . `
   1. Image should be showing under ` docker images`

3. Run container ` docker run -d --name mycontainer -p 8000:5000 digitapi:v1`
   1. ` docker ps` to check your containers

App should now be running on `locahost:8000`.  Navigating to `localhost:8000/docs` will reveal swaggerUI of the endpoint. And you can test `POST` method. I have included one test image of [zero](naster/app/test.png). You can also use cURL

```bash
curl -X 'POST' \
  'http://localhost:8000/predict/image' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.png;type=image/png'
```

 Server will respond with

```json
{
  "prediction": 0,
  "probability": 0.9791600108146667
}
```

![test](master/app/test.png)





