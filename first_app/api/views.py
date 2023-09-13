from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from first_app.models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins,generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminReadOnly, IsOrderedUser
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from.throttling import RatingDetailThrottler, RatingListThrottler
from django_filters.rest_framework import DjangoFilterBackend
from.paginations import CustomPagination, CustomLimitsetPagination, CustomCursorPagination


class ProductDetailFilter(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','price']

class ProductDetailSearch(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','price']

class ProductDetailOrdering(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name','price']

class ThrottleRatingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [RatingDetailThrottler]
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class ThrottleRatingList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    throttle_classes = [RatingListThrottler]
    """throttle_classes = [RatingListThrottler] and below commented code will do same functionality"""
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'rating-list'
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class PageRatingList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    pagination_class = CustomCursorPagination #CustomLimitsetPagination #CustomPagination
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class UserRatingDetail(generics.ListAPIView):
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    # def get_queryset(self):
    #     user_name = self.kwargs['username']
    #     return Ratings.objects.filter(user__username = user_name)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        
        if username is not None:
            return Ratings.objects.filter(user__username = username)
        else:
            return Response({'error':'Not Found'})



class RatingList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class RatingCreate(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        product=Product.objects.get(id=self.kwargs['pk'])
        
        if Ratings.objects.filter(user=self.request.user,product=product).exists():
            raise ValidationError('Already rated')
        total_rating = product.num_of_rating + 1
        total_sum = product.total_rating_sum + serializer.validated_data['rating']
        product.rating = total_sum / total_rating
        product.num_of_rating += 1
        product.total_rating_sum += serializer.validated_data['rating']
        product.save()
        serializer.save(user=self.request.user,product=product,rating=serializer.validated_data['rating'])

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer


class Product_ViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        try:
            queryset = Product.objects.get(pk=pk)
            serializer = ProductSerializer(queryset)
            return Response(serializer.data)
        except:
            return Response("Product Doesn't Exists",status=status.HTTP_404_NOT_FOUND)
        
class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,product=serializer.validated_data['product'])

class OrderUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def perform_update(self, serializer):
    #     p = Product.objects.get(id=self.kwargs['pk'])
    #     instance = serializer.save(product=p)

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# class OrderList(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
    
#     def get_queryset(self):
#         pk=self.kwargs['pk']
#         return Order.objects.filter(product=pk)

# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsOrderedUser]
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

class OrderDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [IsOrderedUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
                            
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request,*args, **kwargs)

# class OrderList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class RatingLst(APIView):
    def get(self,reqest):
        rating = Ratings.objects.all()
        serializer = RatingSerializer(rating, many=True)
        return Response(serializer.data)
    def post(self, request):
        if request.method=='POST':
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

class RatingDetaill(APIView):
    def get(self,request,id):
        rating = Ratings.objects.get(id=id)
        serializer=RatingSerializer(rating)
        return Response(serializer.data)

    def put(self,request,id):
        rating = Ratings.objects.get(id=id)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class GetProducts(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

# class GetProducts(APIView): 
    # def get(self,request):
    #     product = Product.objects.all()
    #     serializer = ProductSerializer(product, many=True)
    #     return Response(serializer.data)
    # def post(self,request):
    #     if request.method=='POST':
    #         serializer=ProductSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors)

class GetProduct(APIView):
    def get(self,request,id):
        try:
            product = Product.objects.get(id=id)
        except:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,id):
        product = Product.objects.get(id=id)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,id):
        Product.objects.get(id=id).delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

class GetCategories(APIView):
    def get(self,request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True,context={'request': request})
        return Response(serializer.data)
    def post(self,request):
        if request.method=='POST':
            serializer=CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
 
class GetCategory(APIView):
    def get(self,request,id):
        try:
            category = Category.objects.get(id=id)
        except:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category,context={'request': request})
        return Response(serializer.data)
    def put(self,request,id):
        category = Category.objects.get(id=id)
        serializer=CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self,request,id):
        Category.objects.get(id=id).delete()
        return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(['GET','POST'])
def get_products(request):
    if request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if request.method=='GET':
        movie = Product.objects.all()
        serializer = ProductSerializer(movie, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def get_movie(request,id):
    if request.method=='GET':
        try:
            movie = Product.objects.get(id=id)
        except:
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(movie)
        return Response(serializer.data)
    if request.method=='PUT':
        movie = Product.objects.get(id=id)
        serializer=ProductSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if request.method == 'DELETE':
        Product.objects.get(id=id).delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
