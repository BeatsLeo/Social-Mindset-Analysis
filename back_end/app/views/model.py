from django.http import JsonResponse

#文本摘要接口
def text_summary(request):
    return JsonResponse(safe=False)

#情感分类借口
def attitude_classification(request):
    return JsonResponse(safe=False)

#命名体识别接口
def named_body_recognition(request):
    return JsonResponse(safe=False)

#引导建议生成接口
def guide_recommendation_generation(request):
    return JsonResponse(safe=False)