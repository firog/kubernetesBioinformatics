import os
from flask import jsonify, current_app
from flask_restplus import Namespace, Resource
from app import config
from ..serializers import filecontent
from .. import api

nsFile = Namespace('filecontents', description='Fetch some DNA sequences')

@nsFile.route('/')
class FileContent(Resource):
    @nsFile.marshal_list_with(filecontent)
    def get(self):
        """
        Retrieve part of fasta file
        """
        fastafile = os.path.join(current_app.config['UPLOAD_FOLDER']) +'/newfa.fa'

        # d = {'sequence_header': '', 'read_content': ''}
        file_content = []

        with open(fastafile, 'r') as f:
            for n in range(400):
                d = {'read_id':'', 'read': ''}
                d['read_id'] = f.readline().rstrip()
                d['read'] = f.readline().rstrip()
                file_content.append(d)
        return file_content
