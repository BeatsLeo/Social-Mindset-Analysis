from django.http import JsonResponse
from transformers import logging, BertTokenizer, AutoTokenizer
from app import models
from app.views.model_setting import *
from app.views.networks import *


def generate(model, event, attitude,device):
    tokenizer = BertTokenizer.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    base_prompt = '对于"{}"这件事，大家都表现出"{}"的心态。对于此心态的出现，引导建议为：\n'
    message = base_prompt.format(event, attitude)

    inputs = tokenizer.encode_plus(message, return_tensors='pt', add_special_tokens=True).to(device)
    output = tokenizer.decode(model.generate(inputs['input_ids'], max_length=350, do_sample=True, num_beams=5)[0])
    output = output.replace(' ', '').replace('1', '\n1').replace('2', '\n2').replace('3', '\n3').replace('4','\n4').replace('5', '\n5').strip()
    pure = output[:output.find('[PAD]')].replace('[CLS]', '').replace('[SEP]', '').replace('[UNK]', '')

    return pure

def classify(model, text,tokenizer):
    model = model.eval()
    inputs = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')
    out = model(inputs)['cls']
    res = out.argmax(dim=1).item()
    return list(ATTITUDE2ID.keys())[res]

#文本摘要接口（模型接口）
def text_summary(request):
    tokenizer = AutoTokenizer.from_pretrained('IDEA-CCNL/Randeng-BART-139M-SUMMARY')
    # 导入模型
    model = torch.load('back_end/text_summary.model')
    model.eval()

    text= request.GET.get('text')# '网页Google 免费提供的这项服务可在简体中文和其他 100 多种语言之间即时翻译字词、短语和网页。某些句子可能包含区分性别的替代译文。点击句子即可查看替代译文。'
    if(text==None):
        return JsonResponse('',safe=False)

    inputs = tokenizer.encode_plus(text, return_tensors='pt')
    result = model.generate(inputs['input_ids'], max_length=128, do_sample=True)[0]

    # print("文本摘要：",tokenizer.decode(result).replace('</s>', '').strip())
    return JsonResponse(tokenizer.decode(result).replace('</s>', '').strip(),safe=False)

#情感分类接口（模型接口）
def attitude_classification(request):

    logging.set_verbosity_error()  # 消除未使用权重的warning
    tokenizer = BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')

    # 导入模型
    model = torch.load('back_end/attitude_classify.model')
    attitude_clf = request.GET.get('attitude_clf')# '我可真高兴呵呵'
    if (attitude_clf==None):
        return JsonResponse('', safe=False)


    # print("情感分类：",classify(model,attitude_clf,tokenizer))
    return JsonResponse(classify(model,attitude_clf,tokenizer),safe=False)

#命名体识别接口（模型接口）
def named_body_recognition(request):
    tokenizer = AutoTokenizer.from_pretrained('IDEA-CCNL/Randeng-BART-139M-SUMMARY')
    # 导入模型
    model = torch.load('back_end/text_summary.model')
    model.eval()

    identity=request.GET.get('identity')# '网页Google 免费提供的这项服务可在简体中文和其他 100 多种语言之间即时翻译字词、短语和网页。某些句子可能包含区分性别的替代译文。点击句子即可查看替代译文。'
    if (identity==None):
        return JsonResponse('', safe=False)

    inputs = tokenizer.encode_plus(identity, return_tensors='pt')
    result = model.generate(inputs['input_ids'], max_length=128, do_sample=True)[0]

    # print("命名体识别：",tokenizer.decode(result).replace('</s>', '').strip())
    return JsonResponse(tokenizer.decode(result).replace('</s>', '').strip(),safe=False)

#引导建议生成接口（心态详情引导建议&心态调整建议库心态列表&建议生成）
def guide_recommendation_generation(request):
    device = 'cuda' if (torch.cuda.is_available()) else 'cpu'

    event=request.GET.get('event')# '很喜欢宫崎骏的一段话'
    attitude = request.GET.get('attitude')# '高兴'
    if (event==None and attitude==None):
        return JsonResponse('', safe=False)
    # 导入模型
    model = torch.load('back_end/lead_opinions.model')
    model.eval().to(device)

    print("心态&事件引导建议：", generate(model, event, attitude,device))
    return JsonResponse(generate(model, event, attitude,device),safe=False)

#心态引导建议生成接口（心态调整建议库心态列表）
def attitude_recommendation_generation(request):
    attitude = request.GET.get('attitude')

    queryset=models.attitude_recommend.objects.filter(attitude=attitude).first()

    # print("心态引导建议：",queryset.suggestion)
    return JsonResponse(queryset.suggestion, safe=False)

#模型打分-type = ((0, '命名体识别'),(1, '情感分类'),(2, '文本摘要'),(3, '引导建议生成'))
def feedback(request):
    try:
        input= request.GET.get('input')
        output=request.GET.get('output')
        type=request.GET.get('type')
        score = request.GET.get('score')

        models.feedback.objects.create(input=input,output=output,type=type,score=score)
        return JsonResponse({'feedback_flag':True},safe=False)
    except Exception as e:
        return JsonResponse({'feedback_flag':False},safe=False)