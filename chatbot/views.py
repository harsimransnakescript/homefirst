from django.shortcuts import render
from django.http import JsonResponse
import openai
from chatbot.models import Patient_Query,Products
from django.conf import settings

def open_file(filepath):
    with open(filepath,'r',encoding='utf-8') as infile:
        return infile.read()
    
def gpt3(text,request):
   
    openai.api_key = settings.OPENAI_API_KEY 

    response = openai.Completion.create(
        model="text-davinci-003", # The pre trained ai model, which helps us to generate the results. #NAME OF THE MODEL
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
        print("chats----",chats)
        data = request.POST["raw"]
        print("dataa======",data)
       
        if "products" in data:
            products = Products.objects.all()
            product_info_list = []

            for product in products:
                product_info = f"Product Name: {product.product_name}\n"
                product_info += f"Product Group: {product.product_group}\n"
                product_info += f"Product Features: {product.product_features}\n"
                product_info += f"Product Specifications: {product.product_specifications}\n"
                product_info += f"Product More Information: {product.product_more_information}\n"
                product_info += f"Product Image: {product.product_image.url}\n"
                product_info_list.append(product_info)
                result = "Available products:\n\n" + "\n".join(product_info_list)

            chats.append('USER: %s' % data)
            chats.append('Guide: %s' % result)
           
        else:
            result = "I'm sorry, I don't understand that."
            
        chats.append('USER: %s' % data)
        text_block = '\n'.join(chats)
        print(">>>>>>.",text_block)
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

    

        
