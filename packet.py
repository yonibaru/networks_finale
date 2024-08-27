class packet:
    def __init__(self, file_name, size, stream_id, file_data):
        self.file_name = file_name
        self.size = size
        self.stream_id = stream_id
        self.data = file_data 
        