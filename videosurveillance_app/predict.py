#variables
num_classes =2
batch_size = 100
epochs = 5
#------------------------------

import os, cv2
from keras.models import Sequential
from tensorflow.keras.models import load_model
import numpy as np

def read_dataset1(path):
    data_list = []
    file_path = os.path.join(path)
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
    data_list.append(res)
    return (np.asarray(data_list, dtype=np.float32))


# ------------------------------
# construct CNN structure

model = Sequential()
if not os.path.exists(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\model_burglary.h5"):
    model.save(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\model_burglary.h5")  # train for randomly selected one
else:
    model = load_model(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\model_burglary.h5")  # load weights


def predict_burglary(fn):
    dataset=read_dataset1(fn)
    dataset=dataset / 255
    (mnist_row, mnist_col, mnist_color) = 48, 48, 1
    dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
    mo = load_model(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\model_burglary.h5")
    yhat_classes = mo.predict_classes(dataset, verbose=0)
    return yhat_classes


# label_list=["Covid", "Lung Opacity", "Normal", "Viral Pneumonia"]
# pred=predictcnn(r"C:\Users\admin\PycharmProjects\covid19_biomarker\dataset\COVID\COVID-9.png")
# print("Folder index : ", pred)
# idx=pred[0]
# print("Prediction : ", label_list[idx])