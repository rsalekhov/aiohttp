from aiohttp import web
import uuid
from datetime import datetime

# Хранилище для объявлений
ads = {}


# Функция для создания нового объявления
async def create_ad(title, description, owner):
    ad_id = str(uuid.uuid4())
    ad = {
        "id": ad_id,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "owner": owner
    }
    ads[ad_id] = ad
    return ad


# Маршрут для создания нового объявления
async def create_ad_route(request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid request, JSON is required"}, status=400)

    if not all(k in data for k in ("title", "description", "owner")):
        return web.json_response({"error": "Invalid request, fields missing"}, status=400)

    ad = await create_ad(data['title'], data['description'], data['owner'])
    return web.json_response(ad, status=201)


# Маршрут для получения объявления по ID
async def get_ad_route(request):
    ad_id = request.match_info['ad_id']
    ad = ads.get(ad_id)
    if not ad:
        return web.json_response({"error": "Ad not found"}, status=404)

    return web.json_response(ad, status=200)


# Маршрут для удаления объявления по ID
async def delete_ad_route(request):
    ad_id = request.match_info['ad_id']
    ad = ads.pop(ad_id, None)
    if not ad:
        return web.json_response({"error": "Ad not found"}, status=404)

    return web.json_response({"message": "Ad deleted"}, status=200)


# Создание приложения и маршрутов
app = web.Application()

app.add_routes([
    web.post('/ads', create_ad_route),
    web.get('/ads/{ad_id}', get_ad_route),
    web.delete('/ads/{ad_id}', delete_ad_route),
])


# Запуск сервера
if __name__ == '__main__':
    web.run_app(app, port=8080)
