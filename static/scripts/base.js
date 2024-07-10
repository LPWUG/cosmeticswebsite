        /* navbar script */

        document.addEventListener('DOMContentLoaded', function() {
            const searchIcon = document.querySelector('.search-icon');
            const searchBoxContainer = document.getElementById('search-box-container');

            searchIcon.addEventListener('click', function() {
                searchBoxContainer.style.display = searchBoxContainer.style.display === 'block' ? 'none' : 'block';
            });
        });

        /* navbar script */

        /* navbar2 script */

        document.addEventListener("DOMContentLoaded", function() {
            var navbar = document.querySelector('.style-103');
            var skincareLink = document.querySelector('a[href="/en-us/skincare"]');
            var skincareDropdown = skincareLink.nextElementSibling;
            var skincareIcon = skincareLink.querySelector('.dropdown-icon');

            var makeupLink = document.querySelector('a[href="/en-us/makeup"]');
            var makeupDropdown = makeupLink.nextElementSibling;
            var makeupIcon = makeupLink.querySelector('.dropdown-icon');

            skincareLink.addEventListener('mouseover', function() {
                if (window.innerWidth > 768) {
                    skincareDropdown.style.display = 'block';
                }
            });

            skincareLink.addEventListener('mouseout', function() {
                if (window.innerWidth > 768) {
                    skincareDropdown.style.display = 'none';
                }
            });

            skincareDropdown.addEventListener('mouseover', function() {
                if (window.innerWidth > 768) {
                    skincareDropdown.style.display = 'block';
                }
            });

            skincareDropdown.addEventListener('mouseout', function() {
                if (window.innerWidth > 768) {
                    skincareDropdown.style.display = 'none';
                }
            });

            makeupLink.addEventListener('mouseover', function() {
                if (window.innerWidth > 768) {
                    makeupDropdown.style.display = 'block';
                }
            });

            makeupLink.addEventListener('mouseout', function() {
                if (window.innerWidth > 768) {
                    makeupDropdown.style.display = 'none';
                }
            });

            makeupDropdown.addEventListener('mouseover', function() {
                if (window.innerWidth > 768) {
                    makeupDropdown.style.display = 'block';
                }
            });

            makeupDropdown.addEventListener('mouseout', function() {
                if (window.innerWidth > 768) {
                    makeupDropdown.style.display = 'none';
                }
            });

            skincareLink.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    var isOpen = skincareDropdown.style.display === 'block';
                    skincareDropdown.style.display = isOpen ? 'none' : 'block';
                }
            });

            makeupLink.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    var isOpen = makeupDropdown.style.display === 'block';
                    makeupDropdown.style.display = isOpen ? 'none' : 'block';
                }
            });
        });

        /* navbar2 script */

        document.addEventListener('DOMContentLoaded', function() {
            const styleNav = document.querySelector('.style-navigation');
            const navbar2 = document.querySelector('.style-101');

            styleNav.addEventListener('click', function(event) {
                event.preventDefault();
                navbar2.style.display = navbar2.style.display === 'flex' ? 'none' : 'flex';
                navbar2.style.position = 'fixed';
                navbar2.style.left = '0';
                navbar2.style.top = '0';
                navbar2.style.width = window.innerWidth > 768 ? '40%' : '80%';
                navbar2.style.height = '100%';
                navbar2.style.zIndex = '1000';
                navbar2.style.backgroundColor = 'white';
                navbar2.style.overflowY = 'auto';
                navbar2.style.transition = 'width 0.3s';
            });

            window.addEventListener('resize', function() {
                if (navbar2.style.display === 'flex') {
                    navbar2.style.width = window.innerWidth > 768 ? '40%' : '80%';
                }
            });

            document.addEventListener('click', function(event) {
                if (navbar2.style.display === 'flex' && !navbar2.contains(event.target) && !styleNav.contains(event.target)) {
                    navbar2.style.display = 'none';
                }
            });
        });