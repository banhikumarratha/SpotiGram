class ChromaClientMock:
    def __init__(self):
        self.connected = True
        
    def search(self, query: str):
        return [{"id": "track123", "score": 0.9}]
