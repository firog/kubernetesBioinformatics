from flask_restplus import Namespace, Resource
from app.models import Task
from ..serializers import task
from .. import api
from app.tools.routes import task_update

nsTask = Namespace('tasks', description='List tasks')

@nsTask.route('/')
class TaskList(Resource):
    @nsTask.marshal_list_with(task)
    def get(self):
        """
        List all tasks
        """
        # for t in Task.query.all():
        #     task_update(task_id=t.task_id, task_name=t.task_name)
        for t in Task.query.all():
            if t.task_state != 'SUCCESS':
                task_update(t.task_id)
        return Task.query.all()
