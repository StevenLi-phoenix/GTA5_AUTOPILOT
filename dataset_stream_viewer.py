import numpy as np
import c
import os.path as osp
import os
import threading


class dataStream:
    def __int__(self, name):
        # load dataSet as a stream
        self.max_index, self._indexs = self.check_dataset()
        if self.max_index is None:
            raise ValueError("No data found")
        self.current_batch = self.load_single(0)
        self.batch_count = 0
        self.index = 0
        self.next_batch = self.load_next()

    def check_dataset(self):
        dirs = os.listdir(c.recoreding_output_directionary)
        indexs = [int(dir.split(".")[0]) for dir in dirs]
        return max(indexs), indexs

    def load_single(self, name):
        data = np.load(osp.join(c.recoreding_output_directionary, str(name)+".npy"), allow_pickle=True)
        return data

    def load_next(self):
        self.batch_count += 1
        if self.batch_count <= self.max_index:
            return self.load_single(self.batch_count)
        else:
            return False

    def gen(self):
        self.index += 1
        if self.index < len(self.current_batch):
            yield self.current_batch[self.index]
        else:
            self.current_batch = self.next_batch
            self.next_batch = self.load_next()
            yield self.gen()

if __name__ == '__main__':
    ds = dataStream()