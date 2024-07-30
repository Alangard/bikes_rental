from rest_framework import status, generics, permissions, serializers
from django.utils import timezone
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from celery.result import AsyncResult


from .models import Bike, Rental
from .serializers import BikeSerializer, RentalSerializer
from .tasks import calculate_total_cost 


@extend_schema(
    description="Retrieve a list of available bikes",
    parameters=[
            OpenApiParameter(
                name='status',
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by status of the bike (e.g., 'available', 'rented')"
            )
    ],
    responses={200: BikeSerializer(many=True)},
)
class BikeListView(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', 'available')
        if status:
            return Bike.objects.filter(status=status)
        return Bike.objects.all()

@extend_schema(
    description="Create a rental record",
    request=RentalSerializer,
    responses={
        201: RentalSerializer,
        400: 'Bike is already rented or end_time is not valid'
    },
    examples=[
        OpenApiExample(
            'Create Rental Example',
            description='Example of a successful rental creation request',
            value={
                "bike": 1,  # ID of the bike being rented
                "end_time": "2024-07-30T18:30:00Z"  # End time of the rental
            },
            request_only=True
        ),
        OpenApiExample(
            'Successful Rental Response',
            description='Example response when a rental record is created successfully',
            value={
                "id": 1,
                "bike": 1,
                "user": 1,
                "start_time": "2024-07-30T15:30:00Z",
                "end_time": "2024-07-30T18:30:00Z",
                "total_cost": '300.00'
            }
        ),
    ]
)
class RentalCreateView(generics.CreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def perform_create(self, serializer):
        bike = serializer.validated_data['bike']
        end_time = serializer.validated_data['end_time']
        
        if end_time <= timezone.now():
            raise serializers.ValidationError("End time must be in the future.")
        
        if bike.status == 'available':
            bike.status = 'rented'
            bike.save()
            
            rental = serializer.save(user=self.request.user)
            
            # Schedule the calculation of total cost
            calculate_total_cost.delay(rental.id)
        else:
            raise serializers.ValidationError("Bike is already rented.")


@extend_schema(
    description="Return a rented bike by bike ID",
    request=None,
    responses={
        202: {'status_url': ''}, 
        400: 'Bike ID is required or bike is not currently rented',
        403: 'Not authorized to return this bike',
        404: 'Rental not found for this bike ID',
    },
    examples=[
        OpenApiExample(
            'Successful Return Example',
            description='Example of a successful bike return',
            value={
                "id": 1,
                "bike": 1,
                "user": 1,
                "start_time": "2024-07-30T15:30:00Z",
                "end_time": "2024-07-30T16:30:00Z",
                "total_cost": "300.00"  # Example total cost
            }
        ),
    ],
    methods=['PUT']
)
class RentalBackView(generics.UpdateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        bike_id = kwargs.get('pk')
        if not bike_id:
            return Response({"error": "Bike ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rental = Rental.objects.get(bike_id=bike_id, user=request.user, end_time__isnull=False)
        except Rental.DoesNotExist:
            return Response({"error": "Rental not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if rental.bike.status != 'rented':
            return Response({"error": "Bike is not currently rented"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        rental.end_time = timezone.now()
        rental.save()
        rental.bike.status = 'available'
        rental.bike.save()
        
        # Schedule recalculation of total cost
        task = calculate_total_cost.delay(rental.id) # need a endpoint to check a task status
        task_id = task.id
        # result = calculate_total_cost.delay(rental.id) # sync task execution blocks the main thread
        # result = calculate_total_cost(rental.id) #sync too, but it's simply than celery solution. not suitable for heavy computing
        # result = await calculate_total_cost(rental.id)
        # websocket or polling use?
        
        check_status_url = reverse('task-status', args=[task_id])
        return Response({"status_url": check_status_url}, status=status.HTTP_202_ACCEPTED)
    


@extend_schema(
    description="Return a status of computing a total_cost",
    request=None,
    responses={
        200: RentalSerializer,
        202: 'Task is still processing', 
        404: 'Rental not found',
        500: 'Task failed'
    },
    examples=[
        OpenApiExample(
            'Successful Return Example',
            description='Example of a successful bike return',
            value={
                "id": 1,
                "bike": 1,
                "user": 1,
                "start_time": "2024-07-30T15:30:00Z",
                "end_time": "2024-07-30T16:30:00Z",
                "total_cost": "300.00"  # Example total cost
            }
        ),
    ],
    methods=['GET']
)
class RentalCostStatusView(APIView):

    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            return Response({"status": "Task is still processing"}, status=status.HTTP_202_ACCEPTED)
        
        if task_result.state == 'SUCCESS':
            rental_id = task_result.result
            try:
                rental = Rental.objects.get(id=rental_id)
            except Rental.DoesNotExist:
                return Response({"error": "Rental not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response(RentalSerializer(rental).data, status=status.HTTP_200_OK)
        
        if task_result.state == 'FAILURE':
            return Response({"error": "Task failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"error": "Unknown task state"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)