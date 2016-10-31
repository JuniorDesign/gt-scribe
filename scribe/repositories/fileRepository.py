from scribe.model.file import File
from scribe.repositories.baseRepository import BaseRepository

class FileRepository(BaseRepository):
        def __init__(self):
        	print("file created")
            super(FileRepository, self).__init__(File)