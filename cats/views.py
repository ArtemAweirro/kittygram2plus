from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.throttling import ScopedRateThrottle
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    throttle_scope = 'low_request'  # Использование скоупа
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None  # Временно отключим пагинацию
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
