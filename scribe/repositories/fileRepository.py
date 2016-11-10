from scribe.model.file import File
from scribe.repositories.baseRepository import BaseRepository

from sqlalchemy import desc

class FileRepository(BaseRepository):
    def __init__(self):
        super(FileRepository, self).__init__(File)

    def add_or_update(self, entity):
        return super(FileRepository, self).add_or_update(entity)

    def get_file(self, file_id):
        return super(FileRepository, self).find(file_id)

    def get_files_for_course(self, course_id):
        files = File.query.filter_by(course_id=course_id).order_by(desc(File.timestamp)).all()
        return files

