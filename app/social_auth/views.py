# from rest_framework import status,generics
# from rest_framework.response import Response
# from . import serializers


# class GoogleAuthView(generics.GenericAPIView):
#     serializer_class = serializers.GoogleAuthSerialier

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data,status=status.HTTP_200_OK)