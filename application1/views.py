from django.shortcuts import render
import requests
from .models import *
from .forms import *
from django.shortcuts import  redirect
# Create your views here.


def function1(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&id=524901&appid=9f601a6811dac69ba37dc1db795053b6'
    message=''
    err_msg=''
    msg_ind=''
    if request.method=="POST":
        cities=City.objects.all()
        #print(cities)
        print(request.POST['name'])
        location=request.POST['name']
        try:
            filtering=City.objects.get(name=request.POST['name'])
            if filtering:
                err_msg="City already exists in the Database"
            else:
                pass
        except:
            print("Not Found")
            check=requests.get(url.format(location)).json()
            if 'message' not in check.keys():
                form=CityForm(request.POST)
                form.save()
            else:
                err_msg="City does not exist"
        if err_msg:
            message=err_msg
            msg_ind='is-danger'
        
        else:
            message="City added successfully"
            msg_ind='is-success'


                
    form=CityForm()
    cities=City.objects.all()
    weather_data=[]
    for city in cities:
        r=requests.get(url.format(city)).json()
        #print(111111111111111111111111111111111111111111111111111111111111111)
        #print(r)
        if 'message' not in r.keys():
            city_weather={'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
            'humidity':r['main']['humidity']}
            weather_data.append(city_weather)
    print(weather_data)
    return render (request , 'application1/weather.html', {'weather_data':weather_data, 'form':form, 'message': message, 'msg_ind': msg_ind})

# def function2(request):
#     if request.method=="POST":
#         city_name=request.POST
#         a=City(name=city_name)
#         a.save()
#     return redirect('function1')


def function2(request ,name):
    city=City.objects.filter(name=name)
    city.delete()
    return redirect('function1')