from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer


class TodoView(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        todo = request.data
        # Create an article from the above data
        serializer = TodoSerializer(data=todo)
        if serializer.is_valid(raise_exception=True):
            todo_saved = serializer.save()
        return Response({"success": "Task '{}' created successfully".format(todo_saved.title)})
