
import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine


# The Song model: This should have an integer id column, and a column specifying a one-to-one relationship with a File.
# The File model: This should have an integer id column, a string column for the file name, and the backref from the one-to-one relationship with the Song.

# {
#     "id": 1,
#     "file": {
#         "id": 7,
#         "name": "Shady_Grove.mp3"
#     }
# }


# The File.as_dictionary method should just return the file element of the song dictionary (i.e. {"id": 7, "name": "Shady_Grove.mp3"}).


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    file = relationship("File", uselist=False, backref="song")

    def as_dictionary(self):
        song = {
            "id": self.id,
            # "file": {
            #     "id": self.file.id,
            #     "body": self.file.name
            # }
            "file": self.file.as_dictionary()
        }
        return song

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)

    def as_dictionary(self):
        file = {
                "id": self.id,
                "body": self.name
        }
        return file
