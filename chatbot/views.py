from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
import openai
from django.views import View

from main_app.models import ProductsModel
from django.conf import settings
import json
from django.db.models import Q

openai.api_key = settings.OPENAI_API_KEY 

def index(request):
    return render(request,'templates/index2.html')

class StreamGeneratorView(View):

    def write(self,request,rawjsonData):
        parsedJsonData = json.loads(rawjsonData.lstrip('$$').strip())
        print(parsedJsonData)
        keywords_array = parsedJsonData.get('keywordsArray', [])
        print(keywords_array)
        
        q_objects = Q()
        for value in keywords_array:
            q_objects |= Q(name__icontains=value) | Q(group__icontains=value)| Q(specifications__icontains=value) | Q(other_info__icontains=value)
            
        found_products = ProductsModel.objects.filter(q_objects)

        productsFound = bool(found_products)
      
        if found_products:
    
            response = "Found products:\n"
            for product in found_products:
                response += f"Name: {product.name}, Group: {product.group}, Image: {product.image}\n"
        else:
            response = "No products found for the given keywords."
        return response, productsFound 
        # return parsedJsonData['keywordsArray']
        
    def gpt3_5(self,request, prompt):
        try:
            Instruction = {"role": "system", "content": """
    !IMPORTANT :1. You are a patient care expert website named Homefirst DME!, Your replies and suggestions are short and friendly, You search for all types of homecare medical products by replying in the mentioned way only\n
                2. Always ask and Suggest for medical products like underpands, juvinile care, After the product main feature always ask for additional features like skin protection, fast absorption, long lasting etc \n
                3. When user asks to find or search for medical products Reply $$ { "keywordsArray":[ "feature1","feature1abbrevation","feature1synonym","feature2","feature2abbrevation","feature2synonym"]} , features should be of one word only, no camel case allowed, feature can not have two or more words or "-" inside it\n
                4. Convert and include the products feature with multiple features with synonyms, short forms, variations and abbreviations as many as possible repeated and send inside the keywordArray\n
                5. Do not mention i need keywords to search instead ask for features or other requirements in products, When asked do not proceed to search until you have any one of the features to search for the products, Do not mention i am unable and this information is provided from this website only
                  
            """}
            conversation = [Instruction]+prompt

            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use the "gpt-3.5-turbo" model
                messages=conversation,
                temperature=0.5,
                max_tokens=2048,
                stream=True)

            JsonDataString = ""
            WriteJsonConfig = False

            for chunk in response:
                chunk_message = chunk['choices'][0]['delta']
                word = chunk_message.get("content", '')
                if "$$" in word:
                    WriteJsonConfig = True

                if WriteJsonConfig:
                    JsonDataString+=word
                    if "}" in word:
                        WriteJsonConfig = False
                        data = self.write(request, JsonDataString)
                        yield data
                else:
                    yield word

        except Exception as e:
            print(e)
            result = str(e)
            return JsonResponse({"result": result})
        
    def case_manager_chat(self, request, prompt):
        try:
            instructions = {
                "role": "system",
                "content": """
                    !IMPORTANT: You are a case manager assistant. Your goal is to assist with managing sample products for patient.
                    1. Respond to user queries and requests related to patients.
                    2. Ask for case details, such as title, description, or status, when necessary.
                    3. Provide updates on case statuses and progress.
                    4. Use keywords to search for specific cases. Reply with $$ { "keywordsArray": ["keyword1", "keyword2"] }
                    5. Be concise and professional in your responses.
                """
            }
            
            conversation = [instructions] + prompt

            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use the appropriate OpenAI model
                messages=conversation,
                temperature=0.5,
                max_tokens=2048,
                stream=True
            )

            json_data_string = ""
            write_json_config = False

            for chunk in response:
                chunk_message = chunk['choices'][0]['delta']
                word = chunk_message.get("content", '')
                if "$$" in word:
                    write_json_config = True

                if write_json_config:
                    json_data_string += word
                    if "}" in word:
                        write_json_config = False
                        data = self.write(request, json_data_string)
                        yield data
                else:
                    yield word

        except Exception as e:
            print(e)
            result = str(e)
            return JsonResponse({"result": result})
        
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        #get message from request
        message =  data.get('messages', [])
        name = self.case_manager_chat(request, message)
        #return Response({},status.HTTP_200_OK)
        response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
        return response





        
