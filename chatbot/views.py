from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
import openai
from django.views import View
import requests
import os
from main_app.models import ProductsModel,Categories,SampleProductsModel, OrderSample
from django.conf import settings
import json
from django.db.models import Q

openai.api_key = settings.OPENAI_API_KEY 

def index(request):
    
    return render(request,'templates/index3.html')

class StreamGeneratorView(View):
    
    def write(self,request,rawjsonData):    
        parsedJsonData = json.loads(rawjsonData.lstrip('$$').strip())
        keywords_array = parsedJsonData.get('keywordsArray', [])
  
        q_objects = Q()
        for value in keywords_array:
            q_objects |= Q(name__icontains=value) | Q(group__icontains=value)| Q(specifications__icontains=value) | Q(other_info__icontains=value)
            
        found_products = ProductsModel.objects.filter(q_objects)
      
        if found_products:
            products_data = []
            for product in found_products:
                product_info = {
                    "id":product.id,
                    "name": product.name,
                    "image":str(product.image.url) if product.image else '',
                    "group": product.group,
                }
                products_data.append(product_info)
                
    
            response_data = {
                "productsFound": True,
                "products": products_data,
            }
        else:
            response_data = {
                "productsFound": False,
                "message": "No products found",
            }
   
        return response_data
    
    
        
    def order(self,request,rawjsonData):   
        product_details = request.session.get('product_details', {})
        sample_item = product_details.get('name', None)
        category = product_details.get('category', None)
 
        parsedJsonData = json.loads(rawjsonData.lstrip('##').strip())
        keywords = parsedJsonData.get('keywordsArray', [])
        first_name = keywords[0]
        last_name = keywords[1]
        gender = keywords[2]
        mobile_phone = keywords[3]
        delivery_method = keywords[4]
        shipping_address = keywords[5]
        
        if delivery_method.lower() == "office":
            delivery_method = "Pick Up in Office"
        else:
            delivery_method = "Home Delivery"
            
        if gender.lower() == "male":
            gender = "Male"
        elif gender.lower() == "female":
            gender = "Female"
        else:
            gender = "Other"
            
        try:
            category = Categories.objects.get(name=category)
        except Categories.DoesNotExist:
            category = None

        try:
            sample_item = SampleProductsModel.objects.get(name=sample_item)
            print(sample_item)
        except SampleProductsModel.DoesNotExist:
            sample_item = None

        order = OrderSample(
            category=category,
            sample_item=sample_item,
            delivery_method=delivery_method,
            shipping_address=shipping_address,
            last_name=last_name,
            first_name=first_name,
            gender=gender,
            mobile_phone=mobile_phone,
        )

        # Save the OrderSample instance to the database
        order.save()
        task = f"Order: {category} - {sample_item}, " \
           f"Delivery Method: {delivery_method}, " \
           f"Shipping Address: {shipping_address}, " \
           f"First Name: {first_name}, " \
           f"Last Name: {last_name}, " \
           f"Gender: {gender}, " \
           f"Mobile Phone: {mobile_phone}"
        
        url = "https://app.asana.com/api/1.0/tasks?opt_fields=&opt_pretty=true"
        payload = { "data": {
                          
                                "projects": ["1205600469702396"],
                                "name": str(task),
                            
                            } }
        headers = {
                        "accept": "application/json",
                        "content-type": "application/json",
                        "authorization": os.environ.get('ASANA_TOKEN')
                    }
        
        response = requests.post(url, json=payload, headers=headers)
        
        return "Thanks for placing your order!"
     
    def gpt3_5(self,request, prompt):
        try:
            Instruction = {"role": "system", "content": """
    !IMPORTANT :1. You are a patient care expert website named Homefirst DME!, Your replies and suggestions are short and friendly, You search for all types of homecare medical products by replying in the mentioned way only\n
                2. Always ask and Suggest for medical products like underpands,liner/pad,brief,personal care.After the product main feature always ask for additional features like skin protection, fast absorption, long lasting etc \n
                3. When user asks to find or search for medical products Reply $$ { "keywordsArray":[ "feature1","feature1abbrevation","feature1synonym","feature2","feature2abbrevation","feature2synonym"]} , features should be of one word only, no camel case allowed, feature can not have two or more words or "-" inside it\n
                4. Convert and include the products feature with multiple features with synonyms, short forms, variations and abbreviations as many as possible repeated and send inside the keywordArray\n
                5. Do not mention i need keywords to search instead ask for features or other requirements in products, When asked do not proceed to search until you have any one of the features to search for the products, Do not mention i am unable and this information is provided from this website only
                6. When user say i have selected a product then ask about Patient First Name, Last Name, Gender , Mobile Number, delivery method: Home Delivery or Pick Up in Office,shipping address.
                7. When user asks to order products Reply ## { "keywordsArray":[ "firstname","lastname","gender","mobileno","delivery method","shipping address"]} \n
                8. When order is placed reply thanks message.
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
            WriteJsonOrder = False 

            for chunk in response:
                chunk_message = chunk['choices'][0]['delta']
                word = chunk_message.get("content", '')
                print("word",word)
    
                if "$$" in word:
                    WriteJsonConfig = True
                
                if "##" in word:
                    WriteJsonOrder = True
                    
                if WriteJsonConfig:
                    JsonDataString+=word
                    if "}" in word:
                        WriteJsonConfig = False
                        data = self.write(request, JsonDataString)
                        yield json.dumps({"data":data,"type":"products"})
                        
                elif WriteJsonOrder:
                    JsonDataString+=word
                    if "}" in word:
                        WriteJsonOrder = False
                        data = self.order(request, JsonDataString)
                        print("data",data)
                        yield json.dumps({"data":data,"type":"order"})
                else:
                    if(word!=''):
                        yield word

        except Exception as e:
            print(e)
            result = str(e)
            return JsonResponse({"result": result})
        
    def post(self,request):
            selectedProducts = request.POST.get('product_id')
            print("_______",selectedProducts)
            
    
            if selectedProducts:
                try:
                    product = ProductsModel.objects.get(id=selectedProducts)
                except ProductsModel.DoesNotExist:
                    return JsonResponse({'error': 'Product not found'}, status=404)
                
                product_details = {
                    'name': product.name,
                    'category': product.category.name
                }
                print("Product Details:", product_details)
                request.session['product_details'] = product_details
                request.session.save()
                
                
                name = self.gpt3_5(request, [])
                print("=====",name)
                response = StreamingHttpResponse(name, status=200, content_type='text/event-stream')
                return response

            else:

                data = json.loads(request.body.decode('utf-8'))

                #get message from request
                message =  data.get('messages', [])
        
                name = self.gpt3_5(request, message)
            
                response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
                return response




def Load_Categories_SampleProducts(request):
    categories = Categories.objects.values('id', 'name')
    products = SampleProductsModel.objects.values('id', 'name')

    categories_list = list(categories)
    products_list = list(products)

    data = {
        "categories": categories_list,
        "products": products_list,
    }

    return JsonResponse(data)






        
