from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchRank
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Collection, LearningNote, Label
from .serializers import LearningNoteSerializer
from .learning_note_pagination import LearningNotePagination
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_timeline(request, user_id):
    """
    Fetch learning notes by collection and optionally filter by labels with pagination.
    """
    collection_id_str = request.GET.get('collection_id', 0)
    label_ids_str = request.GET.get('labels', None)

    try:
        collection_id = int(collection_id_str)
    except ValueError:
        return Response({'error': 'Invalid collection_id'}, status=status.HTTP_400_BAD_REQUEST)

    if label_ids_str:
        try:
            label_ids = json.loads(label_ids_str)
            label_ids = list(map(int, label_ids))
        except ValueError:
            return Response({'error': 'Invalid label ID in labels list'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        label_ids = []

    if collection_id is not None:
        if collection_id == 0:  # Default category that indicates fetching all notes
            learning_notes = LearningNote.objects.filter(
                archived=False, user=user_id)
        else:
            collection = get_object_or_404(
                Collection, id=collection_id, created_by=user_id)
            learning_notes = LearningNote.objects.filter(
                user=user_id, collection=collection, archived=False)
    else:
        return Response({'error': 'Invalid collection ID in collections list'}, status=status.HTTP_400_BAD_REQUEST)

    if label_ids:
        # Query all labels associated with this user
        user_labels = Label.objects.filter(created_by=user_id, id__in=label_ids)
        user_label_ids = set(user_labels.values_list('id', flat=True))

        # Check for any label IDs that are not associated with the user
        invalid_label_ids = set(label_ids) - user_label_ids

        if invalid_label_ids:
            return Response({"error": f"Invalid labels: {list(invalid_label_ids)}"}, status=status.HTTP_400_BAD_REQUEST)

        if len(label_ids) > 0:
            learning_notes = learning_notes.filter(labels__id__in=label_ids).distinct()

    learning_notes = learning_notes.order_by('-created_at')

    paginator = LearningNotePagination()
    paginated_learning_notes = paginator.paginate_queryset(learning_notes, request)

    serializer = LearningNoteSerializer(paginated_learning_notes, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_learning_note(request, pk):
    try:
        learning_note = LearningNote.objects.get(pk=pk)
    except LearningNote.DoesNotExist:
        return Response({"error": "Learning note not found."}, status=status.HTTP_404_NOT_FOUND)

    if learning_note.user_id != request.user.id:
        return Response({"error": "You do not have permission to delete this note"}, status=status.HTTP_403_FORBIDDEN)

    learning_note.archived = True
    learning_note.save()

    serializer = LearningNoteSerializer(learning_note)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_learning_note(request, userId):
    serializer = LearningNoteSerializer(data=request.data)

    if serializer.is_valid():
        user = request.user if request.user.is_authenticated else None

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            learning_note = serializer.save(user=user)
            learning_note_labels = request.data.get('labels')
            learning_note_category = request.data.get('selected_category')

            if learning_note_labels:
                learning_note.labels.set(learning_note_labels)

            if learning_note_category:
                collection = Collection.objects.get(id=learning_note_category, created_by=request.user)
                learning_note.collection = collection
                learning_note.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_learning_note(request, pk):
    try:
        learning_note = LearningNote.objects.get(pk=pk)
    except LearningNote.DoesNotExist:
        return Response({"error": "Learning note not found."}, status=status.HTTP_404_NOT_FOUND)

    if learning_note.user != request.user:
        return Response({"error": "You do not have permission to update this learning note."}, status=status.HTTP_403_FORBIDDEN)

    serializer = LearningNoteSerializer(
        learning_note, data=request.data, partial=True)
    if serializer.is_valid():
        learning_note = serializer.save()
        learning_note_labels = request.data.get('labels')
        learning_note.labels.set(learning_note_labels)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_learning_note(request, pk):
    try:
        learning_note = LearningNote.objects.get(pk=pk)
    except LearningNote.DoesNotExist:
        return Response({"error": "Learning note not found."}, status=status.HTTP_404_NOT_FOUND)

    if learning_note.user_id != request.user.id:
        return Response({"error": "You do not have permission to delete this note"}, status=status.HTTP_403_FORBIDDEN)

    learning_note.delete()

    serializer = LearningNoteSerializer(learning_note)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_label_to_learning_note(request, note_id):
    user = request.user
    note = LearningNote.objects.get(id=note_id, user=user)
    label_id = request.data.get('labelId')

    if label_id:
        label = Label.objects.get(id=label_id)
        note.labels.add(label)
        note.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def remove_label_from_learning_note(request, note_id):
    user = request.user
    note = LearningNote.objects.get(id=note_id, user=user)
    label_id = request.data.get('labelId')

    if label_id:
        label = Label.objects.get(id=label_id)
        note.labels.remove(label)
        note.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_note_to_collection(request, note_id):
    try:
        note = LearningNote.objects.get(id=note_id, user=request.user)
        collection_id = request.data.get('collectionId')

        if collection_id:
            collection = Collection.objects.get(
                id=collection_id, created_by=request.user)
            note.collection = collection
            note.save()

            return Response({"message": "Note added to collection successfully"})
        else:
            return Response({"error": "Collection ID is required"}, status=400)
    except LearningNote.DoesNotExist:
        return Response({"error": "Learning note not found"}, status=404)
    except Collection.DoesNotExist:
        return Response({"error": "Collection not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes_by_collection(request, collection_id):
    try:
        collection = Collection.objects.get(
            id=collection_id, created_by=request.user)
        notes = LearningNote.objects.filter(
            collection=collection, user=request.user)
        serializer = LearningNoteSerializer(notes, many=True)

        return Response(serializer.data)
    except Collection.DoesNotExist:
        return Response({"error": "Collection not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_learning_notes(request):
    query = request.GET.get('query', '')
    if query:
        search_query = SearchQuery(query)
        learning_notes = LearningNote.objects.annotate(
            rank=SearchRank('search_vector', search_query)
        ).filter(search_vector=search_query).order_by('-rank')[:10]
    else:
        learning_notes = []

    serializer = LearningNoteSerializer(learning_notes, many=True)

    return Response(serializer.data)
