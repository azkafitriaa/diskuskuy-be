from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register('week', views.WeekViewSet)
router.register('thread', views.ThreadViewSet)
router.register('reference-file', views.ReferenceFileViewSet)
router.register('breadcrumb', views.BreadcrumbViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('thread-this-month/', views.ThreadThisMonthView.as_view()),
    path('thread-today/', views.ThreadTodayView.as_view()),
    path('analytics/<int:thread_id>/', views.DiscussionAnalytics.as_view(), name="analytics"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
