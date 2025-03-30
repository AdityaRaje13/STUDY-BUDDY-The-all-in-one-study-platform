from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import Notes, Homework, Todo
from youtubesearchpython import VideosSearch
import requests
from django.http import JsonResponse
import wikipedia
import json

def index(request): 
    user = request.user

    # Homework counts
    pending_homework_count = Homework.objects.filter(user=user, is_finished=False).count()
    completed_homework_count = Homework.objects.filter(user=user, is_finished=True).count()
    total_homework_count = pending_homework_count + completed_homework_count

    # To-Do counts
    pending_todo_count = Todo.objects.filter(user=user, is_finished=False).count()
    completed_todo_count = Todo.objects.filter(user=user, is_finished=True).count()
    total_todo_count = pending_todo_count + completed_todo_count

    # Notes count
    notes_count = Notes.objects.filter(user=user).count()

    # Today's to-dos (for the to-do list)
    todos = Todo.objects.filter(user=user, is_finished=False)

    context = {
        'pending_homework_count': pending_homework_count,
        'completed_homework_count': completed_homework_count,
        'total_homework_count': total_homework_count,
        'pending_todo_count': pending_todo_count,
        'completed_todo_count': completed_todo_count,
        'total_todo_count': total_todo_count,
        'notes_count': notes_count,
        'todos': todos,
    }

    return render(request, 'dashboard/home.html', context)

#---------------------------------------------------------------------------------------------

#Profile page

def Profile(request):

    user = request.user

    notes_count = Notes.objects.filter(user=user).count()
    completed_todo_count = Todo.objects.filter(user=user, is_finished=True).count()
    pending_homework_count = Homework.objects.filter(user=user, is_finished=False).count()
    context = {
        'pending_homework_count': pending_homework_count,
        'completed_todo_count': completed_todo_count,
        'notes_count': notes_count,
    }

    return render(request, 'dashboard/profile.html', context)




#---------------------------------------------------------------------------------------------

#User authentication

def registerStudent(request):

    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username, email, password)
        user.save()

        return redirect('/')
    
    return render(request, 'dashboard/register.html')


def loginStudent(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return redirect('/')

    return render(request, 'dashboard/login.html')


def edit_profile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update the logged-in user
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return redirect('/profile')  # Redirect after saving

    return render(request, 'dashboard/profile.html')



def logoutStudent(request):
    logout(request)
    return redirect('/')


#---------------------------------------------------------------------------------------------


# Notes Functionalities

def createNotes(request):

    notes = Notes.objects.filter(user = request.user)
    context = {"notes":notes}

    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')

        if title and desc:
            note = Notes(user=request.user, title=title, description=desc)
            note.save()


    return render(request, 'dashboard/createnotes.html', context)



def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('/notes')


#---------------------------------------------------------------------------------------------


# Homework Functionalities

def addHomework(request):

    allHomeworks = Homework.objects.filter(user = request.user)

    context = {"homeworks" : allHomeworks}

    if request.method == "POST":
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due = request.POST.get('due')

        homework = Homework(user=request.user, subject=subject, title=title, description=description, due_date=due)
        homework.save()

        return redirect("/homework")

    return render(request, "dashboard/homework.html", context)


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('/homework')


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else :
        homework.is_finished = True
    homework.save()
    return redirect('homework')


#---------------------------------------------------------------------------------------------


# ToDo page

def createTodo(request):

    todos = Todo.objects.filter(user=request.user)
    context = {"todos": todos}

    if request.method == "POST":
        task = request.POST.get('task')

        todo = Todo(user=request.user, task=task)
        todo.save()

        return redirect('/todo')

    return render(request, 'dashboard/todo.html', context)


def delete_todo(requst, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('/todo')


def update_todo(request, pk=None):

    todo = Todo.objects.get(id=pk)

    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    
    todo.save()
    return redirect('/todo')


#---------------------------------------------------------------------------------------------


# Youtube page
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def Youtube(request):
    result_list = []

    if request.method == "POST":
        query = request.POST.get('query')

        if not query:
            return render(request, 'dashboard/youtube.html', {'error': 'Query parameter is missing'})

        try:
            logger.debug(f"Searching YouTube for query: {query}")
            videos_search = VideosSearch(query, limit=20)
            results = videos_search.result()['result']
            logger.debug(f"Found {len(results)} results")

            for item in results:
                result_dict = {
                    'input': query,
                    'title': item['title'],
                    'description': item['descriptionSnippet'],
                    'thumbnail': item['thumbnails'][0]['url'],
                    'channel': item['channel']['name'],
                    'link': item['link'],
                    'published': item['publishedTime'],
                }
                result_list.append(result_dict)

        except Exception as e:
            logger.error(f"Error fetching YouTube results: {str(e)}", exc_info=True)
            return render(request, 'dashboard/youtube.html', {
                'error': f'Failed to fetch YouTube results: {str(e)}'
            })

    context = {'results': result_list}
    return render(request, 'dashboard/youtube.html', context)



#---------------------------------------------------------------------------------------------


# Books Page


def Books(request):
    result_list = []

    if request.method == "POST":
        query = request.POST.get('query')

        if not query:
            return JsonResponse({"error": "Query parameter is missing"}, status=400)

        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

        try:
            r = requests.get(url)
            answer = r.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)
        except ValueError:
            return JsonResponse({"error": "Invalid JSON response from Google Books API"}, status=500)

        if "items" not in answer:
            return JsonResponse({"error": "No books found"}, status=404)

        for i in range(min(15, len(answer["items"]))):  
            volume_info = answer["items"][i]["volumeInfo"]
            result_dict = {
                'title': volume_info.get('title'),
                'subtitle': volume_info.get('subtitle'),
                'description': volume_info.get('description'),
                'count': volume_info.get('pageCount'),
                'categories': volume_info.get('categories'),
                'rating': volume_info.get('averageRating'),  
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail'),
                'preview': volume_info.get('previewLink'),
            }

            result_list.append(result_dict)

    context = {"results": result_list}
    return render(request, 'dashboard/books.html', context)


#---------------------------------------------------------------------------------------------


# Dictionary page

def Dictionary(request):
    context = {}

    if request.method == "POST":
        query = request.POST.get('query')

        if not query:
            return JsonResponse({"error": "Word parameter is missing"}, status=400)

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}"  # Correct API URL

        try:
            r = requests.get(url)
            answer = r.json()

            if isinstance(answer, dict) and "title" in answer:
                return JsonResponse({"error": "Word not found"}, status=404)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)
        except ValueError:
            return JsonResponse({"error": "Invalid JSON response from API"}, status=500)

        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
            "input": query,
            "phonetics": phonetics if phonetics else "No phonetics available",
            "audio": audio,
            "definition": definition,
            "example": example,
            "synonyms": synonyms if synonyms else "No synonyms available",
            }

        except:
            context = {
            "input": 'Information Not available for this word',
        }

    return render(request, 'dashboard/dictionary.html', context)


#---------------------------------------------------------------------------------------------


# Wikipedia page

def Wikipedia(request):

    context = {}

    if request.method == "POST":
        query = request.POST.get('query')

        if not query:
            return JsonResponse({"error": "Word parameter is missing"}, status=400)

        search = wikipedia.page(query)

        try:
            context = {
            "input": query,
            "title": search.title,
            "link": search.url,
            "details": search.summary, 
            }

        except:
            context = {
            "input": 'Information Not available for this search',
        }
            
    return render(request, 'dashboard/wikipedia.html', context)


#---------------------------------------------------------------------------------------------


# Conversion Page 

def Conversion(request):
    return render(request, 'dashboard/conversion.html')

#---------------------------------------------------------------------------------------------


# Editor page

def Editor(request):
    return render(request, 'dashboard/editor.html')


#---------------------------------------------------------------------------------------------


# Ai Integration

from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get('query')
        
            genai.configure(api_key="AIzaSyDvD7mFgfDqqBmO3GQ9mVQV1xF4lol-Iwo")

            model = genai.GenerativeModel("gemini-1.5-flash")

            response = model.generate_content(query)

            return JsonResponse({"response": response.text})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return JsonResponse({"error": "Invalid request"}, status=405)




