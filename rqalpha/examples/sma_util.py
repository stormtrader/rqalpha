
class SMAUtil:
    #pandas?

    def __init__(self, sma_data):
        self.sma_data = sma_data

    #获取top和bottom
    def get_top_bottom(self, a):
        h = []
        l = []
        for i in range(len(a)-1, -1, -1):
            if i - 2 < 0:
                al2 = 0
            else:
                al2 = a[i-2]

            if i - 1 < 0:
                al1 = 0
            else:
                al1 = a[i - 1]

            if i + 1 > len(a)-1:
                ar1 = 0
            else:
                ar1 = a[i + 1]

            if i + 2 > len(a)-1:
                ar2 = 0
            else:
                ar2 = a[i + 2]

            if al2 < a[i] and al1 < a[i] and ar1 < a[i] and ar2 < a[i]:
                h.append((i, a[i]))

        for i in range(len(a) - 1, -1, -1):
            if i - 2 < 0:
                al2 = 99999
            else:
                al2 = a[i - 2]

            if i - 1 < 0:
                al1 = 99999
            else:
                al2 = a[i - 1]

            if i + 1 > len(a) - 1:
                ar1 = 99999
            else:
                ar1 = a[i + 1]

            if i + 2 > len(a) - 1:
                ar2 = 99999
            else:
                ar2 = a[i + 2]

            if al2 > a[i] and al1 > a[i] and ar1 > a[i] and ar2 > a[i]:
                l.append((i, a[i]))

        return h, l

    def get_nearest_top(self):
        h, l = self.get_top_bottom(self.sma_data)
        return h[0]




