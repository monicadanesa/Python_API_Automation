class Data():
    def __init__(self):
        self.url = 'http://localhost:51544'

    def generate_endpoint(self, path=None):
        return self.url + str(path)

    def payload_order(self, stops_dict=None):
        payloads = {
            "stops": stops_dict
        }
        return payloads

    def payload_order_time(self, time=None, stops_dict=None):
        payloads = {
            "orderAt":  time,
            "stops": stops_dict
        }
        return payloads
