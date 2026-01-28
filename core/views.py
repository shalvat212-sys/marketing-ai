from django.shortcuts import render
from .models import MarketingPlan
from google import genai
from django.views.decorators.csrf import csrf_exempt
import markdown

# API კონფიგურაცია - ჩასვი შენი გასაღები
client = genai.Client(api_key="AIzaSyD2Qx4zzEgXEasj9Ic-gM3gcKrdTi77Xew")


@csrf_exempt
def create_plan(request):
    context = {}
    if request.method == 'POST':
        d = request.POST
        # მონაცემების შენარჩუნება შეცდომის შემთხვევისთვის
        context = {
            'business_name': d.get('business_name', ''),
            'strengths': d.get('strengths', ''),
            'weaknesses': d.get('weaknesses', ''),
            'opportunities': d.get('opportunities', ''),
            'threats': d.get('threats', ''),
            'pestel_data': d.get('pestel_data', ''),
            'target_audience': d.get('target_audience', ''),
            'marketing_mix_4p': d.get('marketing_mix_4p', ''),
            'marketing_mix_4c': d.get('marketing_mix_4c', ''),
        }

        try:
            # 1. ვპოულობთ ხელმისაწვდომ მოდელს
            models = list(client.models.list())
            usable_model = next((m.name for m in models if "generateContent" in m.supported_actions),
                                "gemini-1.5-flash")

            prompt = f"""
            შენ ხარ პროფესიონალი მარკეტოლოგი. შეადგინე სრული გეგმა ქართულად. გამოიყენე სათაურები და სიები.
            ბიზნესი: {context['business_name']}
            SWOT: {context['strengths']}, {context['weaknesses']}, {context['opportunities']}, {context['threats']}
            PESTEL: {context['pestel_data']}
            STP: {context['target_audience']}
            4P/4C: {context['marketing_mix_4p']}, {context['marketing_mix_4c']}
            """

            # 2. AI გენერაცია
            response = client.models.generate_content(
                model=usable_model,
                contents=prompt
            )

            # 3. Markdown-ის გარდაქმნა HTML-ად (ვარსკვლავების მოსაშორებლად)
            formatted_text = markdown.markdown(response.text)

            # 4. ბაზაში შენახვა
            plan = MarketingPlan.objects.create(
                business_name=context['business_name'],
                strengths=context['strengths'],
                weaknesses=context['weaknesses'],
                opportunities=context['opportunities'],
                threats=context['threats'],
                pestel_data=context['pestel_data'],
                marketing_mix_4p=context['marketing_mix_4p'],
                marketing_mix_4c=context['marketing_mix_4c'],
                target_audience=context['target_audience'],
                generated_strategy=formatted_text
            )

            return render(request, 'core/plan_result.html', {'plan': plan})

        except Exception as e:
            error_msg = str(e)
            context['error'] = f"შეცდომა: {error_msg}"
            return render(request, 'core/plan_form.html', context)

    return render(request, 'core/plan_form.html', context)