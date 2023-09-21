from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register('Week', views.WeekViewSet)
router.register('Thread', views.ThreadViewSet)
router.register('ReferenceFile', views.ReferenceFileViewSet)
# router.register('Summary', views.SummaryViewSet)
# router.register('DiscussionGuide', views.DiscussionGuideViewSet)
router.register('Breadcrumb', views.BreadcrumbViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('thread-today/', views.thread_get_by_today),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('analytics/<int:thread_id>/', views.DiscussionAnalytics.as_view(), name="analytics"),
    # path('<int:thread_id>/discussion-guide/', views.discussion_guide_get_by_thread_id),
    # path('update-state/<int:pk>/', views.discussion_guide_update_state),
]
