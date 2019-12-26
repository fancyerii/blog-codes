import pandas as pd
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from deepctr.models import *
from deepctr.inputs import  SparseFeat, DenseFeat, get_feature_names
from tensorflow import keras
from datetime import datetime
from ctr_data3 import CtrDataSequence
from preprocessor import CtrLabelEncoder, CtrMinMaxScaler
from auc import roc_auc_callback
if __name__ == "__main__":
    names = "label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26".split(",")
    feats = ["C"+str(i) for i in range(1, 27)] + ["I"+str(i) for i in range(1, 14)]
    encoder = CtrLabelEncoder()
    encoder.load("/home/lili/data/train-label-encoder.pkl")
    scaler = CtrMinMaxScaler()
    scaler.load("/home/lili/data/train-minmax-scaler.pkl")
    seq = CtrDataSequence("train", "/home/lili/data/ctr-train.txt", encoder, scaler, splits=10, feats=feats, batch_size=2048,
                          shuffle=True, debug=False, use_cache=False)
    seq_test = CtrDataSequence("test","/home/lili/data/ctr-dev.txt", encoder, scaler, splits=1, feats=feats, batch_size=2048,
                               shuffle=False, debug=False, use_cache=False)

    sparse_features = ['C' + str(i) for i in range(1, 27)]
    dense_features = ['I' + str(i) for i in range(1, 14)]



    # 2.count #unique features for each sparse field,and record dense feature field name

    fixlen_feature_columns = [SparseFeat(feat, vocabulary_size=len(encoder.get_labels(feat)), embedding_dim=4)
                           for i, feat in enumerate(sparse_features)] + [DenseFeat(feat, 1,)
                          for feat in dense_features]

    dnn_feature_columns = fixlen_feature_columns
    linear_feature_columns = fixlen_feature_columns

    feature_names = get_feature_names(linear_feature_columns + dnn_feature_columns)

    # 3.generate input data for model

    #train, test = train_test_split(data, test_size=0.2)

    # 4.Define Model,train,predict and evaluate
    model = DeepFM(linear_feature_columns, dnn_feature_columns, task='binary')
    model.compile("adam", "binary_crossentropy",
                  metrics=['binary_crossentropy'], )
    model.summary()
    mc = keras.callbacks.ModelCheckpoint('ctr-weights-best.h5', save_best_only=True,
                                         save_weights_only=True, period=1, monitor="roc_auc_val", mode="max")

    y_list = []
    class LossHistory(keras.callbacks.Callback):
        def on_batch_end(self, batch, logs={}):
            print("{} batch {}, loss {:.6f}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                   batch+1, logs.get('loss').item()))


    model.fit_generator(seq, epochs=10, verbose=2, callbacks=[LossHistory(), roc_auc_callback(seq_test), mc],
                        max_queue_size=50, shuffle=False)
