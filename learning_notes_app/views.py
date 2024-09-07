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
from .models import LearningNote, User, Label
from .serializers import LearningNoteSerializer, UserSerializer, UserSerializerWithToken, LabelSerializer
from django.http import HttpResponse

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

    if not request.user.has_perm('learning_notes_app.remove_label', label):
        return Response({"error": "You do not have permission to remove this label"}, status=status.HTTP_403_FORBIDDEN)

    label.delete()

    return Response({'message': 'Label deleted successfully'}, status=status.HTTP_200_OK)


##########################
# LEARNING NOTE SECTION

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_timeline(request, pk):
    learning_notes = LearningNote.objects.filter(
        archived=False, user=pk).order_by('-created_at')
    serializer = LearningNoteSerializer(learning_notes, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def archive_learning_note(request, pk):
    try:
        learning_note = LearningNote.objects.get(pk=pk)
    except LearningNote.DoesNotExist:
        return Response({"error": "Learning note not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to archive the learning note (optional)
    if not request.user.has_perm('learning_notes_app.archive_learning_note', learning_note):
        return Response({"error": "You do not have permission to archive this learning note."}, status=status.HTTP_403_FORBIDDEN)

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

    # Check if the user has permission to delete the learning note
    if not request.user.has_perm('learning_notes_app.delete_learning_note', learning_note):
        return Response({"error": "You do not have permission to delete this learning note."}, status=status.HTTP_403_FORBIDDEN)

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
