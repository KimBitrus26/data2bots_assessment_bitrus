from rest_framework.response import Response
from rest_framework import status
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated


from .models import User
from .serializers import CustomUserDetailsSerializer


class UpdateUserView(generics.UpdateAPIView):
    """View to update users information"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserDetailsSerializer
    lookup_field = "pk"
    http_method_names = ("patch",)

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()
        if instance.is_staff or instance.is_superuser:
            return Response("Permission denied", status=status.HTTP_401_UNAUTHORIZED)
        if instance != request.user:
            return Response("Permission denied", status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(
                                    data=request.data, instance=instance, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "User updated successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
