from django.shortcuts import get_object_or_404
from gc import collect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Collection, LearningNote, User, Label
from .serializers import CollectionSerializer, LearningNoteSerializer, UserSerializer, UserSerializerWithToken, LabelSerializer
from django.http import HttpResponse
import json


def home(request):
    return HttpResponse("Welcome to the Home Page!")

#################
# USER SECTION


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


###########
# LABELS

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


#######################
# LEARNING NOTE SECTION

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_timeline(request, user_id):
    """
    Fetch learning notes by collection and optionally filter by labels.
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

    # First, fetch learning notes based on the selected collection (if provided)
    if collection_id is not None:
        if collection_id == 0: # default category that indicates fetching all notes
            learning_notes = LearningNote.objects.filter(archived=False, user=user_id)
        else:
            collection = get_object_or_404(Collection, id=collection_id, created_by=user_id)
            learning_notes = LearningNote.objects.filter(user=user_id, collection=collection, archived=False)
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

    serializer = LearningNoteSerializer(learning_notes, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


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
            if learning_note_labels:
                learning_note.labels.set(learning_note_labels)
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
def remove_label_to_learning_note(request, note_id):
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


####################
# COLLECTION SECTION

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
