from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
import openai
from django.views import View

from chatbot.models import Patient_Query,Products
from django.conf import settings
import json
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
        presence_penalty=0,# increases the models likelihood to talk about new topics
        stream=True
    )
    # content = response.choices[0].text.split('.')
    # return response.choices[0].text#to get the results from the open ai
    test = []
    # def generate_response():
    #     for chunk in response:
    #         chunk_message = chunk['choices'][0]['delta']
    #         test.append(chunk_message.get("content", ''))
    #         yield chunk_message.get({"content", ''})
    def generate_response():
        for chunk in response:
            if 'choices' in chunk and chunk['choices']:
                first_choice = chunk['choices'][0]
                if 'delta' in first_choice:
                    chunk_message = first_choice['delta']
                    test.append(chunk_message.get("content", ''))
                    yield chunk_message.get("content", '')


        # use Django's StreamingHttpResponse to send the response messages as a stream to the frontend
    return StreamingHttpResponse(generate_response(), headers={'X-Accel-Buffering': 'no'})


# def index(request):
#     ''' create session data if not exists '''
#     if not request.session.get('data'):
#         print('data not found')
#         request.session['data'] = []
#
#
#     if request.method=="POST":
#         if not request.session.get('data'):
#             print('data not found')
#             request.session['data'] = []
#         chats = request.session['data']
#         print("chats----",chats)
#         data = request.POST["raw"]
#         print("dataa======",data)
#
#         if "products" in data:
#             products = Products.objects.all()
#             product_info_list = []
#
#             for product in products:
#                 product_info = f"Product Name: {product.product_name}\n"
#                 product_info += f"Product Group: {product.product_group}\n"
#                 product_info += f"Product Features: {product.product_features}\n"
#                 product_info += f"Product Specifications: {product.product_specifications}\n"
#                 product_info += f"Product More Information: {product.product_more_information}\n"
#                 product_info += f"Product Image: {product.product_image.url}\n"
#                 product_info_list.append(product_info)
#                 result = "Available products:\n\n" + "\n".join(product_info_list)
#
#             chats.append('USER: %s' % data)
#             chats.append('Guide: %s' % result)
#
#         else:
#             result = "I'm sorry, I don't understand that."
#
#         chats.append('USER: %s' % data)
#         text_block = '\n'.join(chats)
#         print(">>>>>>.",text_block)
#         prompt = open_file('prompt.txt').replace('<<BLOCK>>', text_block)
#         prompt = prompt + '\nGuide:'
#
#
#         response=gpt3(prompt, request)
#         print(response)
#         chunk_str = ""
#         for chunk in response:
#             print("========",chunk)
#             chunk_str += chunk
#         print("-------",chunk_str)
#
#         result = json.dumps(chunk_str)
#         try:
#             print(result)
#
#         except openai.error.RateLimitError:
#             result = "[ INFO ] The server is currently overloaded with other requests. Sorry about that! You can retry your request."
#         except openai.error.ServiceUnavailableError:
#             result = "[ INFO ] The server is overloaded or not ready yet."
#
#         chats.append('Guide: %s' % result)
#         request.session['data'] = chats
#         print("type",type(result))
#         return JsonResponse({"fetch":result})
#
#
#     elif request.method == "GET":
#         response = Patient_Query.objects.all()
#         final = request.GET.get('raw')
#         if final:
#             request.session['data'] = []
#         return render(request,'templates/index.html',{"questions":response})


def index(request):
    return render(request,'templates/index2.html')

class StreamGeneratorView(View):
    def gpt3_5(self,request, long_text):
        try:
            print(long_text)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use the "gpt-3.5-turbo" model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": long_text},
                ],
                temperature=0.5,
                max_tokens=2000)
            yield response['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            result = str(e)
            return JsonResponse({"result": result})

    def get(self,request):
        name = self.gpt3_5(request, "Hello")
        #return Response({},status.HTTP_200_OK)
        response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
        response['Cache-Control']= 'no-cache',
        return response





        
