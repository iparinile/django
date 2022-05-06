import json
import pickle
from os import path, mkdir

import keras
import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import FileResponse
from keras_preprocessing.text import tokenizer_from_json
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import get_lower, text_update_key, onlygoodsymbols
from .serializers import UploadFileSerializer, AuthUserSerializer
from .token import create_token, read_token, ReadTokenException


class AuthUserView(APIView):
    def post(self, request: Request):
        serializer = AuthUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            request_body = request.data
            try:
                user: User = User.objects.get(username=request_body["login"])
            except DoesNotExist:
                return Response(status=404)

            user_obj = user.save()
            if user.check_password(request_body["password"]):
                payload = {
                    'user_id': user.id
                }

                token = create_token(payload)

                response_body = {
                    'user_id': user.id,
                    'Authorization': token
                }

                return Response(data=response_body, status=200)
            else:
                return Response(status=401)


class UploadFileView(APIView):
    def get(self, request: Request):

        token = request.headers.get('Authorization')
        try:
            read_token(token)
        except ReadTokenException:
            return Response(status=401)

        excel_path = "src/excel/output.xlsx"

        response_excel_file = open(excel_path, mode="rb")
        return FileResponse(response_excel_file)

    def post(self, request: Request):

        token = request.headers.get('Authorization')
        try:
            read_token(token)
        except ReadTokenException:
            return Response(status=401)

        serializer = UploadFileSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            files = request.FILES

            excel_file: InMemoryUploadedFile = files.get('file')
            excel_body: bytes = excel_file.file.getvalue()

            folder_path = "src/excel"
            exel_name = excel_file.name
            if not path.isdir(folder_path):
                mkdir(folder_path)
            excel_path = folder_path
            excel_path += "/" + exel_name

            new_excel_file = open(excel_path, mode="wb")
            new_excel_file.write(excel_body)
            new_excel_file.close()

            model = keras.models.load_model('main_model')

            excel_file = pd.read_excel(excel_path)
            obrashenie = excel_file['Tекст обращения']

            obrashenie.apply(get_lower)
            obrashenie.apply(text_update_key)
            obrashenie.apply(onlygoodsymbols)

            with open('tokenizer.json') as f:
                data = json.load(f)
                t = tokenizer_from_json(data)

            with open('categories.txt', 'rb') as fp:
                categories = pickle.load(fp)
                ly = categories

            obr_t = t.texts_to_matrix(obrashenie, mode='binary')
            pred = (model.predict(obr_t))

            predicts = []
            for i in np.argmax(pred, axis=-1):
                predicts.append(ly[i])

            excel_file["Категория"] = predicts
            # create excel writer object
            output_excel_file = folder_path
            output_excel_file += "/output.xlsx"
            writer = pd.ExcelWriter(output_excel_file)
            # write dataframe to excel
            excel_file.to_excel(writer)
            # save excel
            writer.save()
            return Response(status=201)
