from flask_restplus import Namespace, Resource
from app.tools.routes import filecontent_thread
from .. import api

nsFile = Namespace('filecontents', description='Fetch some DNA sequences')

@nsFile.route('/')
class FileContent(Resource):
    def get(self):
        """
        Retrieve part of fasta file
        """
        return filecontent_thread()
