from django.shortcuts import render,redirect
from django.db.models import F, Sum
from .models import Quote, PageView, Comment
from django.http import Http404, JsonResponse
import random

 #  Выбор цитаты с весом
def choose_quote():
    quotes = Quote.objects.all()
    if not quotes:
        return None
    return random.choices(quotes, weights=[q.weight for q in quotes])[0]

 # Основное представление со случайной цитатой, комментами, счётчиком
def random_quote_view(request):
    quote = choose_quote()
    if not quote:
        return render(request, 'quotes/no_quotes.html')

    page_views = PageView.increment('random_quote_page') # если счётчика нет, он создастся
    
    comments = quote.comments.order_by('-created_at')

    return render(request, 'quotes/chosen_quote.html', {
        'quote': quote,
        'page_views': page_views,
        'comments': comments,
    })

# Для лайков
def like_quote(request,quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
    except Quote.DoesNotExist:
        raise Http404("Цитата не найдена")

    # Получаем или создаем списки лайкнутых и дизлайкнутых цитат 
    liked = request.session.get('liked_quotes', [])
    disliked = request.session.get('disliked_quotes', [])

    if quote_id in liked:
        pass  # Уже лайкнуто, ничего не делаем
    else:
        quote.update_likes()
        liked.append(quote_id)

        if quote_id in disliked:
            disliked.remove(quote_id)
            quote.update_dislikes(-1)

    # Сохраняем обновленные списки в сессии
    request.session['liked_quotes'] = liked
    request.session['disliked_quotes'] = disliked

    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

 # Для дизлайков
def dislike_quote(request,quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
    except Quote.DoesNotExist:
        raise Http404("Цитата не найдена")

    # Получаем или создаем списки лайкнутых и дизлайкнутых цитат 
    liked = request.session.get('liked_quotes', [])
    disliked = request.session.get('disliked_quotes', [])

    if quote_id in disliked:
        pass  # Уже дизлайкнуто, ничего не делаем
    else:
        quote.update_dislikes()
        disliked.append(quote_id)

        if quote_id in liked:
            liked.remove(quote_id)
            quote.update_likes(-1)

    # Сохраняем обновленные списки в сессии
    request.session['liked_quotes'] = liked
    request.session['disliked_quotes'] = disliked

    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})
    
# Представление для добавления цитат
def add_quote_view(request):
    PageView.increment('add_quote_page') 
    if request.method == 'POST': # если отправили новую цитату
        text = request.POST.get('text', '').strip()
        source = request.POST.get('source', '').strip()
        weight = int(request.POST.get('weight', 1))
        if Quote.objects.filter(text=text).exists(): # Фильтруем дубли
            return render(request, 'quotes/add_quote.html', {'error': 'Цитата уже существует.'})

        if Quote.objects.filter(source=source).count() >= 3: # Фильтруем источники, у которых больше 3 цитат
            return render(request, 'quotes/add_quote.html', {'error': 'У этого источника уже есть 3 цитаты.'})

        Quote.objects.create(text=text, source=source, weight=weight)
        return redirect('quotes:random_quote') # Перенаправляем обратно к цитатам

    return render(request, 'quotes/add_quote.html')

# Представление для топа цитат
def top_quotes_view(request):
    top_quotes = Quote.objects.order_by('-likes')[:10]
    PageView.increment('top_quotes_page')
    return render(request, 'quotes/top_quotes.html', {'top_quotes': top_quotes,})

# Представление для топа источников. Суммируем лайки по источникам и сортируем
def top_sources_view(request):
    top_sources = Quote.objects.values('source').annotate(total_likes=Sum('likes')).order_by('-total_likes')[:5]
    PageView.increment('top_sources_page')
    return render(request, 'quotes/top_sources.html', {'top_sources': top_sources})

# Представление для добавления комментариев к цитате
def add_comment(request, quote_id):
    if request.method == 'POST':
        try:
            quote = Quote.objects.get(id=quote_id)
        except Quote.DoesNotExist:
            raise Http404("Цитата не найдена")
        
        text = request.POST.get('text', '').strip()
        author = request.POST.get('author', '').strip()

        if text and author:
            Comment.objects.create(quote=quote, text=text, author=author)

    return redirect(request.META.get('HTTP_REFERER', 'quotes:random_quote'))