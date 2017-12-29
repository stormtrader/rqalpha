

class SMSUtil:
    #pandas?

    def __init__(self, sma_data):
        self.sma_data = sma_data

    def check_nearest_top(self):
        for i in range(len(self.sma_data)):

