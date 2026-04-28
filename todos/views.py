from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Todo
from .serializers import TodoSerializer


@api_view(['GET', 'POST']) #get le fetch,post le create todo
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all() #fetch all todo from db

        # Filter by completed status: ?completed=true / ?completed=false
        completed = request.query_params.get('completed')
        if completed is not None:
            todos = todos.filter(completed=completed.lower() == 'true')

        # Filter by priority: ?priority=high
        priority = request.query_params.get('priority')
        if priority:
            todos = todos.filter(priority=priority)

        serializer = TodoSerializer(todos, many=True)
        return Response({'count': todos.count(), 'results': serializer.data})

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data) #takes json from user
        if serializer.is_valid(): #validates using json rules 
            serializer.save() #if valid saves to db
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def todo_detail(request, pk): #works on single todo
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'GET':
        return Response(TodoSerializer(todo).data)

    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response({'message': 'Todo deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def todo_toggle(request, pk):
    """Shortcut to flip the completed status."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return Response(TodoSerializer(todo).data)