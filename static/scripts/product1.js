/* main scripts */

    function toggleImage() {
        const image = document.getElementById('heart-image');
        const currentSrc = image.src;
        const newSrc = currentSrc === 'https://i.postimg.cc/Sx0HWSZK/heart-3510-1.png' ? 
            'https://i.postimg.cc/Vs33jWM6/heart-3510-1-copy.png' : 
            'https://i.postimg.cc/Sx0HWSZK/heart-3510-1.png';
        image.src = newSrc;
    }
    function toggleContent() {
        const content = document.getElementById('shippingContent');
        const image = document.getElementById('toggleImage');

        if (content.style.display === 'none') {
            content.style.display = 'block';
            image.src = 'https://i.postimg.cc/VLPZP0dq/Caret-Symbol-PNG-Image-2.png';
        } else {
            content.style.display = 'none';
            image.src = 'https://i.postimg.cc/WbYwvdPW/Caret-Symbol-PNG-Image.png';
        }
    }
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

/* main scripts */