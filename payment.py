import request

# Установка параметров Portmone API
merchant_id = 'your_merchant_id'
password = 'your_password'
base_url = 'https://www.portmone.com.ua/gateway/'

# Создание платежа
payment_params = {
    'method': 'create',
    'payee_id': merchant_id,
    'shop_order_number': 'order_id_12345',
    'bill_amount': '100.00',
    'bill_currency': 'UAH',
    'description': 'Payment for goods',
    'success_url': 'https://example.com/payment_success',
    'failure_url': 'https://example.com/payment_failure',
}

response = request.post(base_url, data=payment_params, auth=(merchant_id, password))
print("Payment Status Code:", response.status_code)
