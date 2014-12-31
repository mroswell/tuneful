import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def testGetSongs(self):
        """ Getting songs from a populated database """
        songA = models.Song(id=1)
        songB = models.Song(id=2)

        FileA = models.File(id=1, name = "joy_to_the_world.mp3")
        FileB = models.File(id=2, name = "three_blind_mice.mp3")

        songA.file = FileA
        songB.file = FileB

        session.add_all([songA, songB])
        session.commit()

        response = self.client.get("/api/songs",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

        postA = data[0]
        self.assertEqual(songA.id, 1)
#        self.assertEqual(songA["body"], "Just a test")

        postB = data[1]
        self.assertEqual(songB.id, 2)
        # self.assertEqual(songB["body"], "Still a test")

