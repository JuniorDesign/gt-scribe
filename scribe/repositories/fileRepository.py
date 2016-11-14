from scribe.model.file import File
from scribe.repositories.baseRepository import BaseRepository

class FileRepository(BaseRepository):
    def __init__(self):
        print("file created")
        super(FileRepository, self).__init__(File)

    def add_or_update(self, entity):
        return super(FileRepository, self).add_or_update(entity)