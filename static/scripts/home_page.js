
    (function() {
        const products = document.querySelector('.products');
        const productElements = document.querySelectorAll('.product');
        const buttonLeft = document.querySelector('.button-left');
        const buttonRight = document.querySelector('.button-right');
        let currentIndex = 0;

        function updateVisibility() {
            productElements.forEach((product, index) => {
                if (index >= currentIndex && index < currentIndex + 6) {
                    product.style.display = 'flex';
                } else {
                    product.style.display = 'none';
                }
            });
        }

        buttonRight.addEventListener('click', () => {
            if (currentIndex < productElements.length - 6) {
                currentIndex++;
                updateVisibility();
            }
        });

        buttonLeft.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateVisibility();
            }
        });

        updateVisibility();
    })();

    (function() {
        document.querySelectorAll('.heart-icon').forEach(heart => {
            heart.addEventListener('click', function(e) {
                e.preventDefault(); 
                const currentSrc = this.src;
                const newSrc = currentSrc.includes('heart-3510-1.png') 
                    ? 'https://i.postimg.cc/Vs33jWM6/heart-3510-1-copy.png'
                    : 'https://i.postimg.cc/Sx0HWSZK/heart-3510-1.png';
                this.src = newSrc;
            });
        });
    })();

    (function() {
        let currentIndex = 0;
        const images = document.querySelectorAll('#imageContainer img');
        const totalImages = images.length;
        const images993 = document.querySelectorAll('#imageContainer993 img');
        const totalImages993 = images993.length;

        function showImage(index) {
            const imageContainer = document.getElementById('imageContainer');
            const offset = -index * 100;
            imageContainer.style.transform = `translateX(${offset}vw)`;
        }

        function showImage993(index) {
            const imageContainer993 = document.getElementById('imageContainer993');
            const offset = -index * 100;
            imageContainer993.style.transform = `translateX(${offset}vw)`;
        }

        window.prevImage = function() {
            if (window.innerWidth > 993) {
                if (currentIndex > 0) {
                    currentIndex--;
                    showImage(currentIndex);
                }
            } else {
                if (currentIndex > 0) {
                    currentIndex--;
                    showImage993(currentIndex);
                }
            }
        };

        window.nextImage = function() {
            if (window.innerWidth > 993) {
                if (currentIndex < totalImages - 1) {
                    currentIndex++;
                } else {
                    currentIndex = 0;
                }
                showImage(currentIndex);
            } else {
                if (currentIndex < totalImages993 - 1) {
                    currentIndex++;
                } else {
                    currentIndex = 0;
                }
                showImage993(currentIndex);
            }
        };

        if (window.innerWidth > 993) {
            showImage(currentIndex);
            document.getElementById('imageContainer').style.display = 'flex';
            document.getElementById('imageContainer993').style.display = 'none';
        } else {
            showImage993(currentIndex);
            document.getElementById('imageContainer').style.display = 'none';
            document.getElementById('imageContainer993').style.display = 'flex';
        }

        window.addEventListener('resize', () => {
            if (window.innerWidth > 993) {
                showImage(currentIndex);
                document.getElementById('imageContainer').style.display = 'flex';
                document.getElementById('imageContainer993').style.display = 'none';
            } else {
                showImage993(currentIndex);
                document.getElementById('imageContainer').style.display = 'none';
                document.getElementById('imageContainer993').style.display = 'flex';
            }
        });


        setInterval(nextImage, 10000);
    })();