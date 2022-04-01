import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import model_from_json

#print(tf.__version__)

# Load the saved model
json_file = open('models/model2.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
# load weights into new model
model.load_weights("models/weights2.h5")
print("Loaded saved model from disk.")

# Load model to predict 1 and 7 
json_file = open('models/model.json', 'r')
model_json = json_file.read()
json_file.close()
model_17 = model_from_json(model_json)
# load weights into new model
model_17.load_weights("models/weights.h5")
print("Loaded saved model_17 from disk.")

#model = tf.keras.models.load_model('./models/cnn.h5')
#print("Loaded saved model from disk.")
print(model.summary())

 
# evaluate loaded model on test data
def identify_number(image):
    image_resized = cv2.resize(image, (28,28))    # For plt.imshow
    image_reshaped = image_resized.reshape(-1,28,28,1)    # For input to model.predict_classes
    #cv2.imshow('number', image_test_1)
    model_preds = model.predict(image_reshaped)
    print(model_preds)
    model_pred = np.argmax(model_preds, axis=-1)
    print("Predicted number: {}".format(model_pred[0]))
    if model_pred[0] == 7:
        model_pred[0] = model_17.predict_classes(image_reshaped)[0]
    return model_pred[0]

def extract_number(sudoku):
    sudoku = cv2.resize(sudoku, (450,450))
#    cv2.imshow('sudoku', sudoku)

    # split sudoku
    grid = np.zeros([9,9])
    for i in range(9):
        for j in range(9):
            image = sudoku[i*50:(i+1)*50,j*50:(j+1)*50]
            if image.sum() > 80000:
                #filename = "images/sudoku/file_{}_{}.jpg".format(1*9+i, 1*9+j)
                #cv2.imwrite(filename, image)
                grid[i][j] = identify_number(image)
            else:
                grid[i][j] = 0
    return grid.astype(int)