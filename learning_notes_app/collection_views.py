from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Collection
from .serializers import CollectionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_collections(request, pk):
    collections = Collection.objects.filter(created_by=pk, is_archived=False)
    serializer = CollectionSerializer(collections, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_collection(request):
    user = request.user
    name = request.data.get('name')

    if name:
        collection = Collection.objects.create(created_by=user, name=name)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    else:
        return Response({'error': 'Collection name is required'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def archive_collection(request, collection_id):
    try:
        collection = Collection.objects.get(
            id=collection_id, created_by=request.user)
        collection.archive_collection()

        return Response({"message": "Collection archived successfully"})
    except Collection.DoesNotExist:
        return Response({"error": "Collection not found"}, status=404)
