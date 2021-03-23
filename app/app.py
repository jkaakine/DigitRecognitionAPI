from fastapi import FastAPI, File, UploadFile
import keras
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
from keras.preprocessing.image import ImageDataGenerator
import uvicorn


app = FastAPI(title = "Digit Recognizer")

model = None

@app.get('/index')
def hello():
	return "Hello!"


@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
	if file.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
		return "Image must be in jpeg or png format"
	image = read_imagefile(await file.read())
	prediction, proba = predict(image)
	return {'prediction': prediction, 'probability': proba}


def load_model():
	json_file = open(r'./model/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = keras.models.model_from_json(loaded_model_json)
	loaded_model.load_weights(r"./model/model_weights.h5")
	return loaded_model


def read_imagefile(file) -> Image.Image:
	image = Image.open(BytesIO(file))
	return image

def predict(image: Image.Image):
	global model
	if model is None: model = load_model()
	img = np.asarray(image)
	img = cv2.resize(((cv2.bitwise_not(img)) / 255), dsize=(28,28))
	img = cv2.cvtColor(img.astype("float32"), cv2.COLOR_BGR2GRAY)
	img = img.reshape((1,28,28,1))
	gen = ImageDataGenerator()
	pred_vector = model.predict(gen.flow(img, batch_size = 1))
	return np.asscalar(np.argmax(pred_vector)), np.asscalar(np.max(pred_vector))



if __name__ == "__main__":
	uvicorn.run(app, debug=True, host='0.0.0.0', port='5000')

	


