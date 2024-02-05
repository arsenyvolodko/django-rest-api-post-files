from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from .models import File
from .serializers import FileSerializer
from .tasks import process_file

MAX_UPLOAD_SIZE = 30 * 1024 * 1024  # 30 MB


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        uploaded_file = request.FILES.get('file', None)
        if not uploaded_file:
            return Response({'detail': 'No file was submitted.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if uploaded_file.size > MAX_UPLOAD_SIZE:
            return Response({'detail': 'File size should be less than 20MB.'},
                            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            saved_file = file_serializer.save()

            process_file.delay(saved_file.id)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
