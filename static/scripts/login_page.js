document.querySelector('.style-2040').addEventListener('click', function(event) {
    const emailInput = document.querySelector('.style-2022');
    const passwordInput = document.querySelector('.style-2032');
    let valid = true;

    if (emailInput.value.trim() === '') {
        showMessage(emailInput, 'Please fill out this field');
        valid = false;
    }

    if (passwordInput.value.trim() === '') {
        showMessage(passwordInput, 'Please fill out this field');
        valid = false;
    }

    if (!valid) {
        event.preventDefault();
    }
});

function showMessage(input, message) {
    const msgElem = document.createElement('div');
    msgElem.textContent = message;
    msgElem.style.color = 'red';
    msgElem.style.marginTop = '5px';
    input.parentNode.appendChild(msgElem);
    setTimeout(() => msgElem.remove(), 3000);
}

document.querySelector('.style-2034').addEventListener('click', function() {
    const passwordInput = document.querySelector('.style-2032');
    const passwordType = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', passwordType);
});
