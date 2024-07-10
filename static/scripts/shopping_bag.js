document.addEventListener('DOMContentLoaded', (event) => {
    const decrementButton = document.querySelector('[data-testid="decrement-btn"]');
    const incrementButton = document.querySelector('[data-testid="increment-btn"]');
    const quantityInput = document.querySelector('[data-testid="quantity-input"]');

    const updateButtons = () => {
        const quantityValue = parseInt(quantityInput.value);
        decrementButton.disabled = quantityValue <= 1;
        decrementButton.style.cursor = quantityValue <= 1 ? 'default' : 'pointer';
    };

    decrementButton.addEventListener('click', () => {
        if (quantityInput.value > 1) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
        }
        updateButtons();
    });

    incrementButton.addEventListener('click', () => {
        quantityInput.value = parseInt(quantityInput.value) + 1;
        updateButtons();
    });

    updateButtons();
});