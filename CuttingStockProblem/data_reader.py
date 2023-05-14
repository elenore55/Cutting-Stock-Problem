class DataReader(object):

    @staticmethod
    def read(path):
        with open(path) as f:
            lines = f.readlines()
            stock_length = int(lines[0])
            l_arr = []
            d_arr = []
            for i in range(1, len(lines)):
                l, d = lines[i].split(',')
                l_arr.append(int(l))
                d_arr.append(int(d))
            return stock_length, l_arr, d_arr
