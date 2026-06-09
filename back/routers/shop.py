from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
import database
from dependencies import get_current_user
import requests
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/shop", tags=["shop"])

# Тестовые ключи ЮKassa (замени на свои из личного кабинета)
YOOKASSA_SHOP_ID = "1380630"  # Получи в личном кабинете ЮKassa
YOOKASSA_SECRET_KEY = "test_TGLlgvcKnB2BrT2V-PDoxs4BGC_XrH-_cXlGZ4SnaeQ"  # Получи в личном кабинете ЮKassa
YOOKASSA_API_URL = "https://api.yookassa.ru/v3/payments"

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

class PaymentRequest(BaseModel):
    product_id: int
    return_url: str

# Случайные товары
PRODUCTS = [
    Product(id=1, name="Магический кристалл", description="Усиливает концентрацию на 200%", price=299.99),
    Product(id=2, name="Зелье продуктивности", description="Помогает выполнить все задачи за день", price=149.50),
    Product(id=3, name="Свиток бесконечной энергии", description="Никогда не устаёшь", price=499.00),
    Product(id=4, name="Артефакт удачи", description="+50 к шансу успешного исхода", price=799.99),
    Product(id=5, name="Портативный генератор времени", description="Добавляет 2 часа в сутки", price=1299.00),
    Product(id=6, name="Нейроинтерфейс для обучения", description="Загрузка знаний напрямую в мозг", price=2499.99),
]

@router.get("/products", response_model=list[Product])
def get_products():
    return PRODUCTS

@router.post("/create-payment")
def create_payment(payment_req: PaymentRequest, current_user: dict = Depends(get_current_user)):
    # Найди товар
    product = next((p for p in PRODUCTS if p.id == payment_req.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Создай уникальный idempotence key
    idempotence_key = str(uuid.uuid4())
    
    # Данные платежа
    payment_data = {
        "amount": {
            "value": str(product.price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": payment_req.return_url
        },
        "capture": True,
        "description": f"Покупка товара: {product.name}",
        "metadata": {
            "user_id": current_user['id'],
            "product_id": product.id,
            "product_name": product.name
        }
    }
    
    # Отправь запрос в ЮKassa
    response = requests.post(
        YOOKASSA_API_URL,
        auth=(YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY),
        headers={
            "Content-Type": "application/json",
            "Idempotence-Key": idempotence_key
        },
        json=payment_data
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания платежа: {response.text}"
        )
    
    payment_result = response.json()
    
    # Сохрани информацию о платеже в БД
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO payments (user_id, product_id, payment_id, amount, status, created_at)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (current_user['id'], product.id, payment_result['id'], product.price, 
         payment_result['status'], datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "confirmation_url": payment_result['confirmation']['confirmation_url'],
        "payment_id": payment_result['id']
    }

@router.post("/webhook")
async def payment_webhook(request: Request):
    # Обработка уведомлений от ЮKassa
    data = await request.json()
    
    payment_id = data['object']['id']
    status = data['object']['status']
    
    # Обнови статус платежа в БД
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE payments SET status = %s WHERE payment_id = %s",
        (status, payment_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"status": "ok"}