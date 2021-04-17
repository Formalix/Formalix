from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Document
from .forms import NewUserForm, DocumentForm
from django.contrib import messages
from django.contrib.auth import login
import re
import os
import openai
import json
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return (s[start:end], start-len(first), end+len(last))
    except ValueError:
        return ""

def index(request): 
    completion1 = ""
    completion2 = ""
    completion3 = ""
    if request.method == "POST":
        form = DocumentForm(request.POST or None)
        if form.is_valid():
            document = form.save()
            # print(form.cleaned_data['content'])

            html = form.cleaned_data['content']
            # s = BeautifulSoup(html)
            # found = [a for a in s.find_all(text=True) if 
            
            formcopy = DocumentForm(request.POST.copy())
            to_parse = find_between(html, "<p>---</p>", "<p>---</p>")
            if(to_parse[0] != ""):
                s = BeautifulSoup(to_parse[0], "html.parser")
                to_complete = ''.join(s.find_all(text=True))
                openai.api_key = os.getenv("OPENAI_API_KEY")
                # pre_prompt = ''.join(["mount everest 8000m above see level\n",
                #                 "lies in India and nepal\n",
                #                 "###\n", 
                #                 "Mount Everest is 8000m above sea level and spans across India and Nepal\n", 
                #                 "###\n", 
                #                 "network for large number devices\n", 
                #                 "tested with 10\n", 
                #                 "no errors\n", 
                #                 "50%% less power usage\n", 
                #                 "###\n", 
                #                 "The network architecture was designed to be used for a large number of devices. We tested it with 10 devices at our lab, no errors while encountered. This implementation also reduces power consumption by 50%% relative to the previous solution.\n", 
                #                 "###\n", 
                #                 "first switch trial\n", 
                #                 "distributions match error data\n", 
                #                 "compare frequencies of strategies used on trial 1\n", 
                #                 "distribution of stratigies in older children different than 1 year olds and apes", 
                #                 "1 year olds and apes similar", 
                #                 "###\n", 
                #                 "the first switch trial revealed that distributions match the error data. Comparison of frequencies of strategies adapted on trial 1 showed that distribution of first-choice strategy in older children differed significantly from those of 1-year-olds and apes, which were in turn very similar to each other.\n", 
                #                 "###\n"])
                pre_prompt = ''.join(["mount everest 8000m above see level\n",
                                "lies in India and nepal\n",
                                "###\n", 
                                "Mount Everest is 8000m above sea level and spans across India and Nepal\n", 
                                "###\n", 
                                "network for large number devices\n", 
                                "tested with 10\n", 
                                "no errors\n", 
                                "50%% less power usage\n", 
                                "###\n", 
                                "The network architecture was designed to be used for a large number of devices. We tested it with 10 devices at our lab, no errors while encountered. This implementation also reduces power consumption by 50%% relative to the previous solution.\n", 
                                "###\n", 
                                "first switch trial\n", 
                                "distributions match error data\n", 
                                "compare frequencies of strategies used on trial 1\n", 
                                "distribution of stratigies in older children different than 1 year olds and apes", 
                                "1 year olds and apes similar", 
                                "###\n", 
                                "the first switch trial revealed that distributions match the error data. Comparison of frequencies of strategies adapted on trial 1 showed that distribution of first-choice strategy in older children differed significantly from those of 1-year-olds and apes, which were in turn very similar to each other.\n", 
                                "###\n"])
                
                print(pre_prompt)                                
                test = openai.Completion.create(engine="davinci-instruct-beta", prompt= pre_prompt + to_complete + "\n###\n", max_tokens=400, temperature=0.3, stop="###", n=3)
                print(test)
                print('---------------')
                print(to_parse[1])
                print(to_parse[2])
                completion1 = test['choices'][0]['text']
                completion2 = test['choices'][1]['text']
                completion3 = test['choices'][2]['text']
                formcopy.data['content'] = form.data['content'].replace(form.data['content'][to_parse[1]:to_parse[2]], test['choices'][0]['text'])
                # formcopy.data['content'] 
                
            
            # result = re.search('<p>---</p>(.*)<p>---</p>', html)
            # print(result.group(1))
            # if(parsed_html.p.find(text=true))
            # print(parsed_html.body.find('div', attrs={'class':'container'}).text)
            # messages.success(request, "form saved.")
            # return redirect("homepage")
            return render(request=request, template_name='Portal/index.html', context={"document_form": formcopy, "completion1": completion1, "completion2": completion2, "completion3": completion3})    
        else: 
            messages.error(request, "could not save")

    form = DocumentForm()
    return render(request=request, template_name='Portal/index.html', context={"document_form": form})    

def get_completions(request):
    completion1 = ""
    completion2 = ""
    completion3 = ""
    if request.method == "POST":
        html = request.POST.get('content')
        to_parse = find_between(html, "<p>---</p>", "<p>---</p>")
        if(to_parse[0] != ""):
            s = BeautifulSoup(to_parse[0], "html.parser")
            to_complete = ''.join(s.find_all(text=True))
            openai.api_key = os.getenv("OPENAI_API_KEY")
            pre_prompt = ''.join(["mount everest 8000m above see level\n",
                            "lies in India and nepal\n",
                            "###\n", 
                            "Mount Everest is 8000m above sea level and spans across India and Nepal\n", 
                            "###\n", 
                            "network for large number devices\n", 
                            "tested with 10\n", 
                            "no errors\n", 
                            "50%% less power usage\n", 
                            "###\n", 
                            "The network architecture was designed to be used for a large number of devices. We tested it with 10 devices at our lab, no errors while encountered. This implementation also reduces power consumption by 50%% relative to the previous solution.\n", 
                            "###\n", 
                            "first switch trial\n", 
                            "distributions match error data\n", 
                            "compare frequencies of strategies used on trial 1\n", 
                            "distribution of stratigies in older children different than 1 year olds and apes", 
                            "1 year olds and apes similar", 
                            "###\n", 
                            "the first switch trial revealed that distributions match the error data. Comparison of frequencies of strategies adapted on trial 1 showed that distribution of first-choice strategy in older children differed significantly from those of 1-year-olds and apes, which were in turn very similar to each other.\n", 
                            "###\n"])
            print(pre_prompt)                                
            test = openai.Completion.create(engine="davinci-instruct-beta", prompt= pre_prompt + to_complete + "\n###\n", max_tokens=400, temperature=0.3, stop="###", n=3)
            print(test)
            print('---------------')
            print(to_parse[1])
            print(to_parse[2])
            completion1 = test['choices'][0]['text']
            completion2 = test['choices'][1]['text']
            completion3 = test['choices'][2]['text']
            return HttpResponse(json.dumps({"completion1": completion1, "completion2": completion2, "completion3": completion3}), content_type="application/json")



def register_request(request):
    messages.set_level(request, messages.DEBUG)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("homepage")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
        
    form = NewUserForm()
    return render(request=request, template_name="Portal/register.html", context={"register_form":form})

def homepage(request):
    return HttpResponse("Welcome to homepage")

