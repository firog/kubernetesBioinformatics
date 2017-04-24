from flask_restplus import Namespace, Resource
from app.models import Task
from app.tools.routes import fib_task
from ..serializers import task, fib
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
        for t in Task.query.all():
            if t.task_state != 'SUCCESS':
                task_update(t.task_id)
        return Task.query.all()

@nsTask.route('/<int:n>')
class FibTask(Resource):
    @nsTask.marshal_list_with(fib)
    @api.response(201,'Job started')
    def post(self,n):
        """
        Fib task
        """
        t = fib_task(n)
        return t.get_data()
        # return None, 201
