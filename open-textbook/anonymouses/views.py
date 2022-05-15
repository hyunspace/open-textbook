from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from pkg_resources import require
from .models import Anonymous, Comment
from .forms import AnonymousForm, CommentForm
from django.db.models import Count

@require_safe
def index(request):
    '''
    [GET] 익명 게시판의 글 목록을 보여준다
    '''
    keyword = request.GET.get('keyword')
    if keyword:
        anonymouses = Anonymous.objects.filter(title__contains=keyword).order_by('-created_at')
    else:
        anonymouses = Anonymous.objects.get_queryset().order_by('-created_at')

    hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]
    paginator = Paginator(anonymouses, 20)
    page_number = request.GET.get('page')
    
    hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]

    page_numbers_range = 10
    max_index = len(paginator.page_range)
    current_page = int(page_number) if page_number else 1
    
    previous_page = 0
    if current_page > 10:
        previous_page = ((current_page -1) // page_numbers_range) * page_numbers_range
    
    next_page = 0
    if max_index > 10 and ((current_page -1) // page_numbers_range) * page_numbers_range != ((max_index -1) - 1 // page_number_range):
        next_page = ((current_page -1) // page_numbers_range + 1) * page_numbers_range
    
    start_index = int((current_page - 1)// page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[0:20]
    anonymousList = paginator.get_page(current_page)

    hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]
    comment_articles = Anonymous.objects.annotate(comment_numbers = Count('comment')).order_by('-comment_numbers')[:5]
   

    context = {
        'page_range': page_range,
        'anonymouses': anonymousList,
        'hots': hot_articles,
        'previous_page': previous_page,
        'next_page': next_page,
        'current_page': current_page,
        'comments_articles': comment_articles,
    }    
    return render(request, 'anonymouses/index.html', context)


@require_http_methods(['GET', 'POST'])
def article_create(request):
    '''
    [GET] 새 글 작성 페이지
    [POST] 새 글 등록
    '''
    if request.user.is_authenticated:
        if request.method == 'GET':
            article_form = AnonymousForm
            hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]
            comment_articles = Anonymous.objects.annotate(comment_numbers = Count('comment')).order_by('-comment_numbers')[:5]
            context = {
                'article_form': article_form,
                'hots': hot_articles,
                'comments_articles': comment_articles,
            }
            return render(request, 'anonymouses/create.html', context)
        elif request.method == 'POST':
            article_form = AnonymousForm(request.POST)
            if article_form.is_valid():
                new_article = article_form.save(commit=False)
                new_article.user = request.user
                new_article.save()
            return redirect('anonymouses:article_detail', new_article.pk)
    return redirect('accounts:signin')


def article_detail(request, anonymous_pk):
    '''
    [GET] 특정 게시글 보여주기
    '''
    article = get_object_or_404(Anonymous, pk=anonymous_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(anonymous_id=anonymous_pk)
        comment_form = CommentForm
        hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]
        comment_articles = Anonymous.objects.annotate(comment_numbers = Count('comment')).order_by('-comment_numbers')[:5]
        context = {
            'anonymous': article,
            'comments': comments,
            'comment_form' : comment_form,
            'hots': hot_articles,
            'comments_articles': comment_articles,
        }
        return render(request, 'anonymouses/detail.html', context)



def article_update(request, anonymous_pk):
    '''
    [GET] 특정 게시글 수정 페이지
    [post] 특정 게시글 수정 (작성자==유저)
    '''
    user = request.user
    article = get_object_or_404(Anonymous, pk=anonymous_pk)
    if user.pk == article.user_id:
        if request.method == 'GET':
            # 수정 페이지로 이동
            hot_articles = Anonymous.objects.all().order_by('-like_users')[:5]
            comment_articles = Anonymous.objects.annotate(comment_numbers = Count('comment')).order_by('-comment_numbers')[:5]
            article_form = AnonymousForm(instance=article)
            context = {
                'article_form': article_form,
                'article': article,
                'hots': hot_articles,
                'comments_articles': comment_articles,
            }
            return render(request, 'anonymouses/update.html', context)
        elif request.method == 'PUT':
            # 수정 반영
            pass
    return redirect('anonymouses:index')


@require_POST
def article_delete(request, anonymous_pk):
    article = Anonymous.objects.get(pk=anonymous_pk)
    if request.user == article.user:
        article.delete()
        return redirect('anonymouses:index')

    return redirect('anonymouses:article_detail', anonymous_pk)


@require_POST
def comment_create(request, anonymous_pk):
    '''
    [POST] 댓글 작성
    '''
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        print(new_comment.content)
        new_comment.user = request.user
        new_comment.anonymous_id = anonymous_pk
        new_comment.save()
    return redirect('anonymouses:article_detail', anonymous_pk)


# @require_POST
# def comment_update(request, anonymous_pk, comment_id):
#     '''
#     [GET] 댓글 수정 버튼
#     '''
#     comment = get_object_or_404(Comment, pk=comment_id)
#     pass
#     # 비동기로 처리하면 페이지 이동 없이 수정 가능한데... 어떻게 하면 좋을지 생각할 것


@require_POST
def comment_delete(request, anonymous_pk, comment_id):
    '''
    [POST] 댓글 삭제
    '''
    comment = get_object_or_404(Comment, pk=comment_id)
    print(comment.user)
    if request.user == comment.user:
        comment.delete()
    print(1)
    return redirect('anonymouses:article_detail', anonymous_pk)


@require_POST
def article_like(request, anonymous_pk):
    if request.user.is_authenticated:
        # 특정 글 정보 불러오기
        article = get_object_or_404(Anonymous, pk=anonymous_pk)
        user = request.user

        # 이미 좋아요를 눌렀다면 좋아요 취소
        if article.like_users.filter(pk=user.pk).exists():
            article.like_users.remove(user)
            liked = False
        # 아직 좋아요 안 눌렀다면 좋아요!
        else:
            article.like_users.add(user)
            liked = True
        context = {
            # 좋아요 여부
            'liked': liked,
            'count': article.like_users.count()
        }
        return JsonResponse(context)
    # 로그인 X 유저는 로그인 페이지로 가세요
    return HttpResponse(status=401)