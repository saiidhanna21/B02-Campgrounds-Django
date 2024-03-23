from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('campgrounds/',views.campgrounds,name='campgrounds'),
    path('campgrounds/<str:camp_id>/',views.show_campground,name='showCampground'),
    path('addCampground/',views.add_campground,name='addCampground'),
    path('editCampgound/<str:camp_id>/',views.edit_campground,name='editCampground'),
    path('deleteCampground/<str:camp_id>/',views.delete_campground,name='deleteCampground'),
    path('campgrounds/<str:camp_id>/addReview/',views.add_review,name='addReview'),
    path('campgrounds/<str:camp_id>/editReview/<str:review_id>/',views.edit_review,name='editReview'),
    path('campgrounds/<str:camp_id>/deleteReview/<str:review_id>/',views.delete_review,name='deleteReview'),
    path('campgrounds/<str:camp_id>/bookCampground/',views.book_campground,name='bookCampground'),
    path('bookedCampgrounds/',views.booked_campgrounds,name='bookedCampgrounds'),
]
