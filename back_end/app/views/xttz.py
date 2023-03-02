from django.shortcuts import render

#返回心态调整建议库页面
def xttz(request):
    return render(request,"xttz.html")