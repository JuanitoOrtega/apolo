from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from core.api.serializers import CategorySerializers
from core.pos.models import Category


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    # def get_queryset(self):
    #     return self.get_serializer().Meta.model.objects.all()

    def get(self, request, *args, **kwargs):
        # print(self.request.query_params['name'])
        # print(self.request.query_params.get('name', 'William Vargas'))
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(self.queryset)
        # items = [i.toJSON() for i in Category.objects.all()]
        # queryset = self.get_serializer().Meta.model.objects.all()
        serializer = self.serializer_class(self.queryset.all(), many=True)
        # return self.list(request, *args, **kwargs)
        return Response(serializer.data)