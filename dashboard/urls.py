from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Authentication
    path('', views.loginStudent, name="login"),
    path('register/', views.registerStudent, name="register"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('logout/', views.logoutStudent, name="logout"),

    # Home page
    path('home/', views.index, name="homepage"),

    # Profile page
    path('profile/', views.Profile, name="profilepage"),

    # Notes page
    path('notes/', views.createNotes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),

    # Homework Page
    path('homework/', views.addHomework, name="homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete_homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update_homework"),

    #Todo page
    path('todo/', views.createTodo, name="todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete_todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update_todo"),

    # Youtube Page
    path('youtube/', views.Youtube, name="youtube"),

    # Books Page
    path('books/', views.Books, name="books"),

    # Dictionary Page
    path('dictionary/', views.Dictionary, name="dictionary"),

    # Wikipedia Page
    path('wikipedia/', views.Wikipedia, name="wikipedia"),

    # Conversion Page
    path('conversion/', views.Conversion, name="conversion"),

    # Code Editor Page
    path('editor/', views.Editor, name="editor"),

    # ChatBot 
    path('chatbot/', views.chatbot, name="chatbot"),

    #Community Page
    path('community/<int:pk>', views.communityView, name="community"),

    # Upvote Toggle
    path('post/<int:post_id>/upvote/', views.toggle_upvote, name="toggle_upvote"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)