from django.http.response import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Document
from .forms import NewUserForm, DocumentForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from htmldocx import HtmlToDocx

import re
import os
import openai
import json
import numpy as np
from django.views import generic

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


# class IndexView(generic.ListView):
#     template_name = 'Portal/index.html'
#     context_object_name = 'document_list'
#     # model = Document
#     def get_queryset(self):
#         return Document.objects.values_list('content', 'title')

def index(request):
    print(Document._meta.fields)
    document_list = Document.objects.all()
    # document_list = Document.objects.all()
    return render(request=request, template_name='Portal/index.html', context={"document_list": document_list}) 

    
def genDoc(request):
    # print(request.POST.get('ids')[0])
    final = ""
    parser = HtmlToDocx()

    for doc in Document.objects.all():
        final += doc.content + "<br/>\n"

    
    # final += "<br/>\n<hr/>\n<h2>References:</h2>"
    
    final += "<br/><h2>References</h2><br/>\n"

    for doc in Document.objects.all():
        final += doc.reference + "<br/>"


    result = parser.parse_html_string(final)
    print(parser.parse_html_string(final))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    result.save(response)
    return response



def genTex(request):
    print("unimplemented")


def edit(request): 
    # completion1 = ""
    # completion2 = ""
    # completion3 = ""
    form = DocumentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            document = form.save(commit=False)
            document.user_id = request.user
            document.save()
            return redirect("index")
    
    return render(request=request, template_name='Portal/edit.html', context={"document_form": form})


def deleteDocument(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect("index")

def editDetail(request, document_id):
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=get_object_or_404(Document, pk=document_id))
        if form.is_valid():
            document = form.save(commit=False)
            document.user_id = request.user
            document.save()
            return redirect("index")
    form = DocumentForm(instance=get_object_or_404(Document, pk=document_id))
    return render(request=request, template_name='Portal/editDetail.html', context={"document_form": form})

def get_completions(request):
    completion1 = ""
    completion2 = ""
    completion3 = ""
    if request.method == "POST":
        html = request.POST.get('content')
        to_parse = find_between(html, "<p>---</p>", "<p>---</p>")
        if(to_parse[0] != ""):
            s = BeautifulSoup(to_parse[0], "html.parser")
            to_complete = ''.join(s.find_all(text=True)).replace("\n", ", ")
            openai.api_key = os.getenv("OPENAI_API_KEY")
            """pre_prompt = ''.join(["mount everest 8000m above see level\n",
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
                            "###\n"])"""
            pre_prompt = "Write a paragraph in academic style that includes the terms "
            print(pre_prompt)                                
            #test = openai.Completion.create(engine="davinci-instruct-beta", prompt= pre_prompt + to_complete + "\n###\n", max_tokens=400, temperature=0.3, stop="###", n=3)
            test = openai.Completion.create(engine="davinci-instruct-beta", prompt=pre_prompt + to_complete + ":\n",
                                            max_tokens=150, temperature=0.3, top_p=1, frequency_penalty=.8, stop="\n", n=3)
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

latex_trials = 3
latex_primer = """
Write \"4 times (x to the n) minus 2 times (2 to the x)\" as a latex formula:
$4 \\times x^{n} - 2 \\times 2^{x}$

Write \"log of x base 4\" as a latex formula:
$log_{4}({x})$

Write \"partial derivative of the nth root of x wrt x\" as a latex formula:
$\\frac{\\partial}{\\partial x} (\\sqrt[n]{x})$

Write \"derivative of the nth root of x wrt x\" as a latex formula:
$\\frac{d}{dx} (\\sqrt[n]{x})$

"""
#user_input = "3 minus the nth root of x"
#user_input = "partial derivative of f wrt x"
#user_input = "n choose 2"
#user_input = "partial derivative of the nth root of x wrt x"
#user_input = "partial derivative of 4 times x cubed minus y to the 6 wrt x"
#user_input = "3 times (y to the z) plus 7 times (3 to the 4)"
#user_input = "3x over y"
#user_input = "natural logarithm of x"
#user_input = "ln x"
#user_input = "log 4117 base 3"
#user_input = "derivative of f wrt x"
#user_input = "integral of f wrt x"
#user_input = "integral from 0 to infinity of f wrt x"

def logprob_to_prob(logits):
    odds = np.exp(logits)
    return odds / (1 + odds)

def latex_formula_request(user_input):
    req_input = latex_primer + "Write \"" + user_input + "\" as a latex formula:\n$"
    result = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=req_input,
        max_tokens=len(user_input),
        temperature=0.2,
        top_p=1,
        stop="$",
        logprobs=4,
        n=3)
    confidence_per_result = compute_confidence_per_result(result)
    return result['choices'][np.argmax(confidence_per_result)]['text']

# Calculates how confident GPT-3 is about each response,
# i.e. the average probability of the tokens in each response.
# high value = high probability = high confidence
def compute_confidence_per_result(response, trials=3, max_tokens):
    token_logprobs = []
    for i in range(trials):
        logprobs_i = np.asarray(response['choices'][i]['logprobs']['token_logprobs'])
        # some results stop before consuming all tokens.
        # fill that up with zeros, so we don't confuse numpy
        logprobs_i.resize(max_tokens)
        token_logprobs.append(logprobs_i)
    logprobs = np.asarray(token_logprobs).reshape(trials, -1)
    # Shouldn't use np.mean(1) here, because that'd include the padding zeros from above
    log_confidence = np.true_divide(logprobs.sum(axis=1), (logprobs != 0).sum(axis=1))
    return logprob_to_prob(log_confidence)


