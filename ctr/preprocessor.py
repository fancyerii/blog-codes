try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

import tqdm
import os
from collections import defaultdict

class CtrLabelEncoder:
    def __init__(self):
        self.label_id_dicts = None
        self.id_label_dicts = None
        self.na = None

    def fit(self, tsv_file, col_idxs, col_names, sep="\t", na="N/A",
            add_na=True, check_column_count=None, min_freq=10):
        if not col_names or len(col_idxs) != len(col_names):
            raise Exception("col_names and col_idxs mismatch or empty")
        self.na = na
        self._init_map(col_names, add_na)


        na_cols = set()
        counter_dict = {}
        for col_name in col_names:
            counter_dict[col_name] = defaultdict(int)


        with tqdm.tqdm(total=os.path.getsize(tsv_file)) as pbar:
            with open(tsv_file, "r") as file:
                for line in file:
                    pbar.update(len(line)) # only works with ascii
                    line = line.rstrip("\n")
                    tks = line.split(sep)
                    if check_column_count and len(tks) != check_column_count:
                        for i, tk in enumerate(tks):
                            print("{}, {}".format(i, tk))
                        raise Exception("check_column_count={}, len(tks)={}".
                                        format(check_column_count, len(tks)))

                    for idx, col_name in zip(col_idxs, col_names):
                        tk = tks[idx]
                        if tk == '':
                            tk = na
                            na_cols.add(col_name)
                        counter = counter_dict[col_name]
                        counter[tk] += 1

        print("na cols: {}".format(na_cols))

        for col, dict in counter_dict.items():
            label_dict = self.label_id_dicts[col]
            for tk, count in dict.items():
                if count >= min_freq and tk != self.na:
                    label_dict[tk] = len(label_dict)

        self._build_idmap_from_labelmap()

    def transform(self, col_name, label, check_exist=False):
        if label == '':
            label = self.na
        exist = label in self.label_id_dicts[col_name]
        if check_exist and not exist:
            return None
        if exist:
            return self.label_id_dicts[col_name][label]
        else:
            return self.label_id_dicts[col_name][self.na]

    def inverse_transform(self, col_name, idx, na_to_empty=True):
        v = self.id_label_dicts[col_name][idx]
        if na_to_empty and v == self.na:
            return ''
        else:
            return v

    def get_cols(self):
        return list(self.id_label_dicts.keys())

    def get_labels(self, col_name):
        return self.id_label_dicts[col_name]

    def _init_map(self, col_names, add_na):
        self.label_id_dicts = {}
        self.id_label_dicts = {}
        for col_name in col_names:
            self.label_id_dicts[col_name] = {}
            self.id_label_dicts[col_name] = []
            if add_na:
                self.label_id_dicts[col_name][self.na] = 0
                self.id_label_dicts[col_name].append(self.na)

    def _build_idmap_from_labelmap(self):
        self.id_label_dicts = {}
        for col_name, label_id_map in self.label_id_dicts.items():
            id_list = [None] * len(label_id_map)
            self.id_label_dicts[col_name] = id_list
            for label, idx in label_id_map.items():
                id_list[idx] = label

    def _build_labelmap_from_idmap(self):
        self.label_id_dicts = {}
        for col_name, id_label_map in self.id_label_dicts.items():
            self.label_id_dicts[col_name] = {}
            for i in range(len(id_label_map)):
                self.label_id_dicts[col_name][id_label_map[i]] = i

    def save(self, file):
        if self.id_label_dicts is None:
            raise Exception("id_label_maps is None, maybe you need call fit before to_json")
        data = (self.na, self.id_label_dicts)
        with open(file, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    def load(self, file):
        with open(file, 'rb') as f:
            self.na, self.id_label_dicts = pickle.load(f)
        self._build_labelmap_from_idmap()


class CtrMinMaxScaler:
    def __init__(self, feature_range=(0, 1)):
        self.scaler_dicts = None
        self.na = None
        self.feature_range = feature_range

    def fit(self, tsv_file, col_idxs, col_names, sep="\t", na=0, check_column_count=None):
        if not col_names or len(col_idxs) != len(col_names):
            raise Exception("col_names and col_idxs mismatch or empty")
        self.na = na
        self.scaler_dicts = {}
        for col_name in col_names:
            self.scaler_dicts[col_name] = {"data_min": float('inf'), "data_max": float('-inf')}
        with tqdm.tqdm(total=os.path.getsize(tsv_file)) as pbar:
            with open(tsv_file, "r") as file:
                for line in file:
                    pbar.update(len(line))
                    line = line.rstrip("\n")
                    tks = line.split(sep)
                    if check_column_count and len(tks) != check_column_count:
                        for i, tk in enumerate(tks):
                            print("{}, {}".format(i, tk))
                        raise Exception("check_column_count={}, len(tks)={}".
                                        format(check_column_count, len(tks)))

                    for idx, col_name in zip(col_idxs, col_names):
                        tk = tks[idx]
                        if tk == '':
                            tk = na
                        else:
                            tk = float(tk)

                        sd = self.scaler_dicts[col_name]
                        sd["data_max"] = max(sd["data_max"], tk)
                        sd["data_min"] = min(sd["data_min"], tk)

        for sd in self.scaler_dicts.values():
            data_range = sd["data_max"] - sd["data_min"]
            if data_range == 0:
                data_range = 1
            sd["scale"] = (self.feature_range[1] - self.feature_range[0]) / data_range
            sd["min"] = self.feature_range[0] - sd["data_min"] * sd["scale"]



    def transform(self, col_name, data, force_in_range=False):
        if not data:
            data = self.na

        sd = self.scaler_dicts[col_name]
        data *= sd["scale"]
        data += sd["min"]

        if force_in_range:
            if data < self.feature_range[0]:
                data = self.feature_range[0]
            elif data > self.feature_range[1]:
                data = self.feature_range[1]

        return data

    def inverse_transform(self, col_name, x):
        sd = self.scaler_dicts[col_name]
        x -= sd["min"]
        x /= sd["scale"]
        return x

    def get_cols(self):
        return list(self.scaler_dicts.keys())

    def get_info(self, col_name):
        return self.scaler_dicts[col_name]

    def save(self, file):
        if self.scaler_dicts is None:
            raise Exception("scaler_dicts is None, maybe you need call fit before save")
        data = (self.na, self.feature_range, self.scaler_dicts)
        with open(file, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    def load(self, file):
        with open(file, 'rb') as f:
            self.na, self.feature_range, self.scaler_dicts = pickle.load(f)



if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("need 3 args: input-csv label-encoder.pkl minmaxscalar.pkl".format())
        sys.exit(-1)


    encoder = CtrLabelEncoder()
    col_idxs = list(range(14, 40))
    col_names = ["C"+str(i) for i in range(1, 27)]
    print("CtrLabelEncoder fit from {} to {}".format(sys.argv[1], sys.argv[2]))
    encoder.fit(sys.argv[1], col_idxs, col_names, check_column_count=40)
    encoder.save(sys.argv[2])



    encoder = CtrMinMaxScaler()
    col_idxs = list(range(1, 14))
    col_names = ["I"+str(i) for i in range(1, 14)]
    print("CtrMinMaxScaler fit from {} to {}".format(sys.argv[1], sys.argv[3]))
    encoder.fit(sys.argv[1], col_idxs, col_names)
    encoder.save(sys.argv[3])

