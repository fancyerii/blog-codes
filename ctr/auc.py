from tensorflow import keras
from datetime import datetime
import numpy as np
from sklearn.metrics import log_loss, roc_auc_score

class roc_auc_callback(keras.callbacks.Callback):
    def __init__(self, validation_generator):
        self.validation_generator = validation_generator

    def on_train_begin(self, logs={}):
        return

    def on_train_end(self, logs={}):
        return

    def on_epoch_begin(self, epoch, logs={}):
        return

    def on_epoch_end(self, epoch, logs={}):
        print("epoch {}, {} start auc calcing...".format(epoch + 1, datetime.now()))
        y_pred_list = []

        y_pred = self.model.predict_generator(self.validation_generator)
        print(y_pred.shape)
        y_pred_list.append(y_pred)

        y_pred_array = np.concatenate(y_pred_list)

        y_list = []

        for batch_idx in range(len(self.validation_generator)):
            print("{} batch {}".format(datetime.now(), batch_idx))
            X, y = self.validation_generator[batch_idx]
            print(len(y))
            y_list.append(y)

        y_array = np.concatenate(y_list)

        roc_val = roc_auc_score(y_array, y_pred_array)
        print("{} roc={}".format(datetime.now(), roc_val))
        logs['roc_auc_val'] = roc_val

        print("{} end auc calcing...".format(datetime.now()))

    def on_epoch_end2(self, epoch, logs={}):
        print("{} start auc calcing...".format(datetime.now()))
        y_list = []
        y_pred_list = []

        for epoch in range(self.validation_generator.splits):
            for batch_idx in range(len(self.validation_generator)):
                print("{} batch {}".format(datetime.now(), batch_idx))
                X, y = self.validation_generator[batch_idx]
                y_pred = self.model.predict(X)
                y_list.append(y)
                y_pred_list.append(y_pred)
        y_pred_array = np.concatenate(y_pred_list)
        y_array = np.concatenate(y_list)
        roc_val = roc_auc_score(y_array, y_pred_array)
        print("{} roc={}".format(datetime.now(), roc_val))
        logs['roc_auc_val'] = roc_val

if __name__ == '__main__':
    y_pred1 = [0.8, 0.7, 0.65, 0.55]
    y_list = [1, 1, 0, 1]
    print(roc_auc_score(y_list, y_pred1))