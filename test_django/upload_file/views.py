from os import path, mkdir

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UploadFileSerializer


class UploadFileView(APIView):
    def post(self, request: Request):
        print(request)

        serializer = UploadFileSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            files = request.FILES

            excel_file: InMemoryUploadedFile = files.get('file')
            excel_body: bytes = excel_file.file.getvalue()

            excel_path = "src/excel"
            exel_name = excel_file.name
            if not path.isdir(excel_path):
                mkdir(excel_path)
            excel_path += "/" + exel_name

            new_excel_file = open(excel_path, mode="wb")
            new_excel_file.write(excel_body)
            new_excel_file.close()
            a = 3

            response = [1, 2, 3, 4, 5]
        return Response(data=response)
