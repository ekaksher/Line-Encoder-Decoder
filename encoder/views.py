from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import EncoderForm
from Utils import generator
def index(request):
    return render(request,'encoder/home.html')
def encode(request):
    form = EncoderForm()
    if request.method == "POST":
        form = EncoderForm(request.POST)
        custom = form['custom'].data
        if custom:
            seq = list(map(int,list(form['custom_bits'].value())))
        else:
            if form['fixed_sequence'].data:
                fixed_size = int(form['fixed_size'].data)
                fixed_freq = int(form['fixed_freq'].data)
            bit_size = int(form['bit_size'].data)
            seq = generator.generate(bit_size,form['fixed_sequence'].data,fixed_size,fixed_freq)
        print(seq)
        scheme = form['scheme_choice'].data
        if scheme=='AMI':
            scrambling = form['scrambling_choice'].data            
        
        if form.is_valid():
            
            return redirect('results',scheme=scheme)
        else:
            print(form)
    return render(request,'encoder/encode.html',{'title':"Encode",'form':form})
def decode(request):
    return render(request,'encoder/decode.html',{'title':"Decode"})
def about(request):
    return render(request,'encoder/about.html',{'title':"About"})
def results(request,scheme):
    return render(request,'encoder/result.html')
