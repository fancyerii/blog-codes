from tensorflow import keras
import numpy as np

import tqdm
import os
from preprocessor import CtrLabelEncoder, CtrMinMaxScaler
from datetime import datetime

class CtrDataSequence(keras.utils.Sequence):
    def __init__(self, file_path, encoder, scaler, feats, batch_size=256,
                 splits=None, shuffle=True, debug=False):
        self.file_path = file_path
        self.shuffle = shuffle
        self.encoder = encoder
        self.scaler = scaler
        self.debug =  debug
        self.feat_dict = {}
        for i in range(len(feats)):
            self.feat_dict[feats[i]] = i

        self.batch_size = batch_size
        file_size = os.path.getsize(file_path)
        if splits is None:
            self.splits = int(np.floor(file_size / (1024 * 1024 * 1024)))
            if self.splits == 0:
                self.splits = 1
        else:
            self.splits = splits

        self.split_linenumbers = []
        self.split_filepositions = []

        with tqdm.tqdm(total=file_size) as pbar:
            with open(file_path) as file:
                split_idx = 0
                split_bytes = int(np.floor(file_size / self.splits))
                line_number = 0

                while True:
                    line_start_pos = file.tell()
                    line = file.readline()
                    if not line:
                        break

                    pbar.update(file.tell() - line_start_pos)
                    if line_start_pos >= split_bytes*(split_idx+1):
                        split_idx += 1
                        self.split_linenumbers.append(line_number)
                        self.split_filepositions.append(line_start_pos)

                    line_number += 1

                self.total_linenumber = line_number

        #print(self.split_linenumbers)
        #print(self.split_filepositions)
        self.current_split = 0
        self._read_current_split()

    def __len__(self):
        return int(np.ceil(len(self.lines) / self.batch_size))

    def __getitem__(self, index):
        if self.debug:
            print("{} getitem {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index))
        start_idx = index * self.batch_size
        end_idx = min(start_idx + self.batch_size, len(self.lines))
        batch_lines = self.lines[start_idx: end_idx]


        y = []
        X = []
        for i in range(39):
            X.append([])
        dtypes = [np.int32] * 26 + [np.float32] * 13
        for line in batch_lines:
            tks = line.split("\t")
            y.append(int(tks[0]))
            for i in range(1, 14):
                col_name = "I" + str(i)
                col_idx = self.feat_dict[col_name]
                tk = int(tks[i]) if tks[i] != '' else None
                X[col_idx].append(self.scaler.transform(col_name, tk))

            for i in range(1, 27):
                col_name = "C" + str(i)
                col_idx = self.feat_dict[col_name]
                X[col_idx].append(self.encoder.transform(col_name, tks[i+13]))
        for i in range(len(X)):
            X[i] = np.array(X[i], dtype=dtypes[i])
        X = [np.array(x) for x in X]
        if self.debug:
            print("{} getitem {} len={}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), index, len(y)))
        return X, y

    def on_epoch_end(self):
        self.current_split = (self.current_split + 1) % self.splits
        self._read_current_split()
        if self.debug:
            print("curr_split {}, lines: {}".format(self.current_split, len(self.lines)))

    def _read_current_split(self):
        if self.current_split == 0:
            start_pos = 0
            start_line = 0
        else:
            start_pos = self.split_filepositions[self.current_split-1]
            start_line = self.split_linenumbers[self.current_split-1]

        if self.current_split < len(self.split_linenumbers):
            end_line = self.split_linenumbers[self.current_split]
        else:
            end_line = self.total_linenumber

        #print("read split[{}], start_pos[{}], start_line[{}], end_line[{}]".format(
        #        self.current_split, start_pos, start_line, end_line
        #    ))

        self.lines = []
        with open(self.file_path) as file:
            file.seek(start_pos)
            while True:
                line = file.readline()
                if not line:
                    break

                self.lines.append(line.rstrip("\n"))
                if len(self.lines) == end_line - start_line:
                    break

            if len(self.lines) != end_line - start_line:
                raise Exception("algo bug: self.lines={}, end_line={}, start={}"
                                .format(len(self.lines), end_line, start_line))
        #print("finish read split")
        if self.shuffle:
            np.random.shuffle(self.lines)


if __name__ == '__main__':
    seq = CtrDataSequence("/home/lili/data/ctr-train.small", None, None, splits=4)
    from keras.utils import Sequence
    print(isinstance(seq, Sequence))
