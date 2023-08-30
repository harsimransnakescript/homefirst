from django.shortcuts import render
from django.http import JsonResponse
import openai
from chatbot.models import Patient_Query
from django.conf import settings

def open_file(filepath):
    with open(filepath,'r',encoding='utf-8') as infile:
        return infile.read()
    
def gpt3(text,request):
   
    openai.api_key = settings.OPENAI_API_KEY # the key from the open ai website.
    # the key from the open ai website.
    response = openai.Completion.create(
        engine="text-davinci-003", # The pre trained ai model, which helps us to generate the results. #NAME OF THE MODEL
        prompt=text, # The query or the question asked.
        temperature=0.2, # Higher the value, large and different results. Lesser values results in deterministic and repetition.
        max_tokens=1000, # One token is roughly 4 characters of english
        top_p=0, # controls diversity
        frequency_penalty=0, # decreases the models likelihood to repeat same answers.
        presence_penalty=0 # increases the models likelihood to talk about new topics
    )
    # content = response.choices[0].text.split('.')
    return response.choices[0].text#to get the results from the open ai


def index(request):
    ''' create session data if not exists '''
    if not request.session.get('data'):
        print('data not found')
        request.session['data'] = []


    if request.method=="POST":
        if not request.session.get('data'):
            print('data not found')
            request.session['data'] = []
        chats = request.session['data']

        data = request.POST["raw"]

        chats.append('USER: %s' % data)
        text_block = '\n'.join(chats)

        prompt = open_file('prompt.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nGuide:'
        try:
            result=gpt3(prompt, request).lstrip()
        except openai.error.RateLimitError:
            result = "[ INFO ] The server is currently overloaded with other requests. Sorry about that! You can retry your request."
        except openai.error.ServiceUnavailableError:
            result = "[ INFO ] The server is overloaded or not ready yet."

        chats.append('Guide: %s' % result)
        request.session['data'] = chats

        return JsonResponse({"fetch":result})

    elif request.method == "GET":
        response = Patient_Query.objects.all()
        final = request.GET.get('raw')
        if final:
            request.session['data'] = []
        return render(request,'templates/index.html',{"questions":response})     

    

        
