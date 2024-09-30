from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Label
from .serializers import LabelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def label_list(request, pk):
    labels = Label.objects.filter(created_by=pk)
    serializer = LabelSerializer(labels, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_label(request):
    serializer = LabelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_label(request, label_id):
    try:
        label = Label.objects.get(id=label_id)
    except Label.DoesNotExist:
        return Response({"error": "Label not found"}, status=status.HTTP_404_NOT_FOUND)

    if label.created_by != request.user:
        return Response({"error": "You do not have permission to delete this label"}, status=status.HTTP_403_FORBIDDEN)

    label.delete()

    return Response({'message': 'Label deleted successfully'}, status=status.HTTP_200_OK)
