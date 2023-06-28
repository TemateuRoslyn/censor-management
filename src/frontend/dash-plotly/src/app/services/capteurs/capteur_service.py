from services.APIRequest import APIRequest


class CapteurService:
    def __init__(self):
        self.request = APIRequest()

    def get_next(self):
        datas = self.request.get("/accelerometre1/next")
        if datas is not None:
            return datas
