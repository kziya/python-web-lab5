import json

from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models import User, Food, Order

users = []
foods = []
orders = []


# Utility function to parse JSON request body
def parse_json(request):
    return json.loads(request.body.decode('utf-8'))


# User Views
@csrf_exempt
def user_list_view(request):
    if request.method == 'GET':
        return JsonResponse([user.__dict__ for user in users], safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        user = User(len(users) + 1, data['email'])
        users.append(user)
        return JsonResponse(user.__dict__)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def user_detail_view(request, user_id):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(user.__dict__)
    elif request.method == 'PATCH':
        data = parse_json(request)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        return JsonResponse(user.__dict__)
    elif request.method == 'DELETE':
        users.remove(user)
        return JsonResponse({'message': 'User deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])


# Food Views
@csrf_exempt
def food_list_view(request):
    if request.method == 'GET':
        return JsonResponse([food.__dict__ for food in foods], safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        food = Food(len(foods) + 1, data['name'], float(data['price']))
        foods.append(food)
        return JsonResponse(food.__dict__)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def food_detail_view(request, food_id):
    food = next((f for f in foods if f.id == food_id), None)
    if not food:
        return JsonResponse({'error': 'Food not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(food.__dict__)
    elif request.method == 'PATCH':
        data = parse_json(request)
        food.name = data.get('name', food.name)
        food.price = float(data.get('price', food.price))
        return JsonResponse(food.__dict__)
    elif request.method == 'DELETE':
        foods.remove(food)
        return JsonResponse({'message': 'Food deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])


# Order Views
@csrf_exempt
def order_list_view(request):
    if request.method == 'GET':
        return JsonResponse([order.__dict__ for order in orders], safe=False)
    elif request.method == 'POST':
        data = parse_json(request)
        user = next((u for u in users if u.id == int(data['user_id'])), None)
        food = next((f for f in foods if f.id == int(data['food_id'])), None)
        if user and food:
            order = Order(len(orders) + 1, user, food, int(data['quantity']))
            orders.append(order)
            return JsonResponse(order.__dict__)
        return JsonResponse({'error': 'Invalid user or food id'}, status=400)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def order_detail_view(request, order_id):
    order = next((o for o in orders if o.id == order_id), None)
    if not order:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(order.__dict__)
    elif request.method == 'PATCH':
        data = parse_json(request)
        user = next((u for u in users if u.id == int(data['user_id'])), order.user)
        food = next((f for f in foods if f.id == int(data['food_id'])), order.food)
        order.user = user
        order.food = food
        order.quantity = int(data.get('quantity', order.quantity))
        return JsonResponse(order.__dict__)
    elif request.method == 'DELETE':
        orders.remove(order)
        return JsonResponse({'message': 'Order deleted'})
    else:
        return HttpResponseNotAllowed(['GET', 'PATCH', 'DELETE'])
