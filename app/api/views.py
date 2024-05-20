# views.py

import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import User, Food, Order


# Utility function to parse JSON request body
def parse_json(request):
    return json.loads(request.body.decode('utf-8'))


# User Views
@csrf_exempt
def user_list_view(request):
    if request.method == 'GET':
        users = User.objects.all().values()
        return JsonResponse(list(users), safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        user = User.objects.create(email=data['email'])
        return JsonResponse({'id': user.id, 'email': user.email})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def user_detail_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': user.id, 'email': user.email})
    elif request.method == 'PATCH':
        data = parse_json(request)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({'id': user.id, 'email': user.email})
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])


# Food Views
@csrf_exempt
def food_list_view(request):
    if request.method == 'GET':
        foods = Food.objects.all().values()
        return JsonResponse(list(foods), safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        food = Food.objects.create(name=data['name'], price=float(data['price']))
        return JsonResponse({'id': food.id, 'name': food.name, 'price': food.price})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def food_detail_view(request, food_id):
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return JsonResponse({'error': 'Food not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': food.id, 'name': food.name, 'price': food.price})
    elif request.method == 'PATCH':
        data = parse_json(request)
        food.name = data.get('name', food.name)
        food.price = float(data.get('price', food.price))
        food.save()
        return JsonResponse({'id': food.id, 'name': food.name, 'price': food.price})
    elif request.method == 'DELETE':
        food.delete()
        return JsonResponse({'message': 'Food deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])


# Order Views
@csrf_exempt
def order_list_view(request):
    if request.method == 'GET':
        orders = Order.objects.all().values()
        return JsonResponse(list(orders), safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        try:
            user = User.objects.get(id=int(data['user_id']))
            food = Food.objects.get(id=int(data['food_id']))
        except (User.DoesNotExist, Food.DoesNotExist):
            return JsonResponse({'error': 'Invalid user or food id'}, status=400)
        order = Order.objects.create(user=user, food=food)
        return JsonResponse({'id': order.id, 'user': order.user.id, 'food': order.food.id})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def order_detail_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': order.id, 'user': order.user.id, 'food': order.food.id})
    elif request.method == 'PATCH':
        data = parse_json(request)
        try:
            user = User.objects.get(id=int(data['user_id']))
            food = Food.objects.get(id=int(data['food_id']))
        except (User.DoesNotExist, Food.DoesNotExist):
            return JsonResponse({'error': 'Invalid user or food id'}, status=400)
        order.user = user
        order.food = food
        order.save()
        return JsonResponse({'id': order.id, 'user': order.user.id, 'food': order.food.id})
    elif request.method == 'DELETE':
        order.delete()
        return JsonResponse({'message': 'Order deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])
