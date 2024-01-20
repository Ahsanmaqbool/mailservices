from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Train, Parcel, Line, Booking
from .serializers import TrainSerializer, ParcelSerializer, LineSerializer, BookingSerializer
from .utils import assign_parcels_to_trains, optimize_parcel_assignment


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ProcessShipmentsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # using greedy algorithm for optimization
            # assign_parcels_to_trains()

            # using linear programming optimization technique
            optimize_parcel_assignment()

            return Response({"message": "Shipments processed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
