from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Max, Min
from .models import User, GuangDongHouse, UserFavorite
import bcrypt
import json
from pyecharts.charts import Bar, Pie, Line, Scatter, Radar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import plotly.graph_objects as go
import plotly.offline as pyo


def register_view(request):
    """用户注册视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': '用户名已存在'})
        
        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': '邮箱已被注册'})
        
        # 密码加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # 创建用户
        user = User.objects.create(
            username=username,
            password=hashed_password.decode('utf-8'),
            email=email,
            phone=phone
        )
        
        return JsonResponse({'success': True, 'message': '注册成功'})
    
    return render(request, 'register.html')


def login_view(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            # 验证密码
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                # 登录成功，设置session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return JsonResponse({'success': True, 'message': '登录成功'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})
    
    return render(request, 'login.html')


def logout_view(request):
    """用户登出视图"""
    request.session.flush()
    return redirect('login')


def index_view(request):
    """首页视图"""
    # 获取筛选参数
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    orientation = request.GET.get('orientation', '')
    pattern = request.GET.get('pattern', '')
    elevator = request.GET.get('elevator', '')
    sort_by = request.GET.get('sort', 'id')
    page = request.GET.get('page', 1)
    
    # 构建查询条件
    houses = GuangDongHouse.objects.all()
    
    # 城市筛选
    if city:
        houses = houses.filter(city__icontains=city)
    
    # 价格筛选
    if min_price:
        try:
            houses = houses.filter(total_price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            houses = houses.filter(total_price__lte=float(max_price))
        except ValueError:
            pass
    
    # 朝向筛选
    if orientation:
        houses = houses.filter(orientation__icontains=orientation)
    
    # 房型筛选
    if pattern:
        houses = houses.filter(pattern__icontains=pattern)
    
    # 电梯筛选
    if elevator:
        if elevator == '有':
            houses = houses.filter(elevator=True)
        elif elevator == '无':
            houses = houses.filter(elevator=False)
    
    # 排序
    if sort_by == 'price_asc':
        houses = houses.order_by('total_price')
    elif sort_by == 'price_desc':
        houses = houses.order_by('-total_price')
    elif sort_by == 'area_asc':
        houses = houses.order_by('area')
    elif sort_by == 'area_desc':
        houses = houses.order_by('-area')
    elif sort_by == 'unit_price_asc':
        houses = houses.order_by('unit_price')
    elif sort_by == 'unit_price_desc':
        houses = houses.order_by('-unit_price')
    else:
        houses = houses.order_by('-id')
    
    # 分页
    paginator = Paginator(houses, 12)  # 每页显示12个房源
    houses_page = paginator.get_page(page)
    
    # 获取筛选选项数据
    cities = GuangDongHouse.objects.values_list('city', flat=True).distinct()
    orientations = GuangDongHouse.objects.values_list('orientation', flat=True).distinct()
    patterns = GuangDongHouse.objects.values_list('pattern', flat=True).distinct()
    
    # 获取用户收藏的房源ID列表
    user_favorites = []
    if request.session.get('user_id'):
        user_favorites = UserFavorite.objects.filter(
            user_id=request.session['user_id']
        ).values_list('house_id', flat=True)
    
    context = {
        'houses': houses_page,
        'cities': cities,
        'orientations': orientations,
        'patterns': patterns,
        'current_filters': {
            'city': city,
            'min_price': min_price,
            'max_price': max_price,
            'orientation': orientation,
            'pattern': pattern,
            'elevator': elevator,
            'sort': sort_by,
        },
        'user_favorites': list(user_favorites),
    }
    
    return render(request, 'index.html', context)


@csrf_exempt
def add_favorite(request):
    """添加收藏"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'})
    
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        user_id = request.session['user_id']
        
        # 检查是否已收藏
        if UserFavorite.objects.filter(user_id=user_id, house_id=house_id).exists():
            return JsonResponse({'success': False, 'message': '已经收藏过了'})
        
        # 添加收藏
        UserFavorite.objects.create(user_id=user_id, house_id=house_id)
        return JsonResponse({'success': True, 'message': '收藏成功'})
    
    return JsonResponse({'success': False, 'message': '请求方法错误'})


@csrf_exempt
def remove_favorite(request):
    """取消收藏"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'})
    
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        user_id = request.session['user_id']
        
        # 删除收藏
        UserFavorite.objects.filter(user_id=user_id, house_id=house_id).delete()
        return JsonResponse({'success': True, 'message': '取消收藏成功'})
    
    return JsonResponse({'success': False, 'message': '请求方法错误'})


def house_detail(request, house_id):
    """房源详情页面"""
    house = get_object_or_404(GuangDongHouse, id=house_id)
    
    # 检查是否已收藏
    is_favorited = False
    if request.session.get('user_id'):
        is_favorited = UserFavorite.objects.filter(
            user_id=request.session['user_id'],
            house_id=house_id
        ).exists()
    
    # 获取相似房源（同城市、相似价格范围）
    similar_houses = GuangDongHouse.objects.filter(
        city=house.city,
        total_price__gte=house.total_price * 0.8,
        total_price__lte=house.total_price * 1.2
    ).exclude(id=house_id)[:6]
    
    context = {
        'house': house,
        'is_favorited': is_favorited,
        'similar_houses': similar_houses,
    }
    
    return render(request, 'house_detail.html', context)


def dashboard_view(request):
    """数据可视化大屏"""
    # 获取基础统计数据
    total_houses = GuangDongHouse.objects.count()
    avg_price = GuangDongHouse.objects.aggregate(Avg('total_price'))['total_price__avg'] or 0
    avg_unit_price = GuangDongHouse.objects.aggregate(Avg('unit_price'))['unit_price__avg'] or 0
    
    # 城市分布数据
    city_data = GuangDongHouse.objects.values('city').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    city_names = [item['city'] for item in city_data]
    city_counts = [item['count'] for item in city_data]
    
    # 生成图表
    city_bar_chart = create_city_bar_chart(city_names, city_counts)
    
    context = {
        'total_houses': total_houses,
        'avg_price': round(avg_price, 2),
        'avg_unit_price': round(avg_unit_price, 2),
        'city_bar_chart': city_bar_chart,
    }
    
    return render(request, 'dashboard.html', context)


def create_city_bar_chart(city_names, city_counts):
    """创建城市分布柱状图"""
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="100%", height="400px"))
        .add_xaxis(city_names)
        .add_yaxis("房源数量", city_counts)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="热门城市房源分布"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            yaxis_opts=opts.AxisOpts(name="数量")
        )
    )
    return bar.render_embed()
