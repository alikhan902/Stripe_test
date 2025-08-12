function initStripePayment(buyUrl, publishableKey) {
    // Передача ключа и создание форм
    const stripe = Stripe(publishableKey);
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');

    const buyButton = document.getElementById('buy-button');
    const paymentMessage = document.getElementById('payment-message');
    // Отправка и проверка данных
    buyButton.addEventListener('click', async () => {
        try {
            const resp = await fetch(buyUrl);
            const data = await resp.json();

            if (data.error) {
                paymentMessage.textContent = data.error;
                return;
            }

            const { error, paymentIntent } = await stripe.confirmCardPayment(data.client_secret, {
                payment_method: { card: cardElement }
            });

            if (error) {
                paymentMessage.textContent = error.message;
            } else if (paymentIntent.status === 'succeeded') {
                paymentMessage.textContent = '✅ Payment succeeded!';
            }
        } catch (err) {
            paymentMessage.textContent = '❌ Error: ' + err.message;
        }
    });
}
