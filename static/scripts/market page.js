/* main scripts */

        document.querySelector('.style-585').addEventListener('click', function() {
            const dropdown = document.getElementById('dropdown-options');
            const img = document.querySelector('.style-591');
    
            if (dropdown.style.display === 'none' || dropdown.style.display === '') {
                dropdown.style.display = 'block';
                img.src = 'https://i.postimg.cc/VLPZP0dq/Caret-Symbol-PNG-Image-2.png'; 
            } else {
                dropdown.style.display = 'none';
                img.src = 'https://i.postimg.cc/WbYwvdPW/Caret-Symbol-PNG-Image.png'; 
            }
        });
    
        document.getElementById('brand-button').addEventListener('click', function() {
            const img = document.getElementById('brand-image');
            const buttonsContainer = document.getElementById('buttons-container');
            const currentSrc = img.src;
            const originalSrc = 'https://i.postimg.cc/BvX9MLBx/pngegg-1.png';
            const newSrc = 'https://i.postimg.cc/ZnGQWGyB/plus-104-32.png';
    
            if (currentSrc === originalSrc) {
                img.src = newSrc;
                buttonsContainer.style.display = 'none';
            } else {
                img.src = originalSrc;
                buttonsContainer.style.display = 'block';
            }
        });
        document.getElementById('price-button').addEventListener('click', function() {
            const img = document.getElementById('price-image');
            const formContainer = document.getElementById('price-form-container');
            const currentSrc = img.src;
            const originalSrc = 'https://i.postimg.cc/BvX9MLBx/pngegg-1.png'; 
            const newSrc = 'https://i.postimg.cc/ZnGQWGyB/plus-104-32.png'; 
    

            if (currentSrc === originalSrc) {
                img.src = newSrc;
                formContainer.style.display = 'none';
            } else {
                img.src = originalSrc;
                formContainer.style.display = 'block';
            }
        });
        document.querySelectorAll('[id^="favorites-button"]').forEach((button, index) => {
            button.addEventListener('click', () => {
                const heartImage = document.getElementById(`heart-image-${index + 1}`);
                const currentSrc = heartImage.src;
                const defaultSrc = "https://i.postimg.cc/Sx0HWSZK/heart-3510-1.png";
                const activeSrc = "https://i.postimg.cc/Vs33jWM6/heart-3510-1-copy.png";
                
                const currentFilename = currentSrc.substring(currentSrc.lastIndexOf('/') + 1);
                const defaultFilename = defaultSrc.substring(defaultSrc.lastIndexOf('/') + 1);
                const activeFilename = activeSrc.substring(activeSrc.lastIndexOf('/') + 1);

                heartImage.src = currentFilename === defaultFilename ? activeSrc : defaultSrc;
            });
        });

        const browseByButton = document.getElementById('browseByButton');
        const filterSortButton = document.getElementById('filterSortButton');
        const sidebarPopup = document.getElementById('sidebarPopup');
        const filterPopup = document.getElementById('filterPopup');

        browseByButton.addEventListener('click', () => {
            sidebarPopup.classList.toggle('popup-visible');
        });

        filterSortButton.addEventListener('click', () => {
            filterPopup.classList.toggle('popup-visible');
        });

        document.addEventListener('click', (event) => {
            if (!sidebarPopup.contains(event.target) && !browseByButton.contains(event.target)) {
                sidebarPopup.classList.remove('popup-visible');
            }
            if (!filterPopup.contains(event.target) && !filterSortButton.contains(event.target)) {
                filterPopup.classList.remove('popup-visible');
            }
        });
      
    

/* main scripts */