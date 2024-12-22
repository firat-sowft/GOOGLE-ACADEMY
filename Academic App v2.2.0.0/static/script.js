document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([38.9637, 35.2433], 6); // Türkiye'nin merkezine yakın bir konum

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var cities = [
        { name: "Elazığ", coords: [38.6743, 39.2220] },
        { name: "İzmir", coords: [38.4237, 27.1428] }
    ];

    cities.forEach(function(city) {
        var marker = L.marker(city.coords).addTo(map)
            .bindPopup(city.name);

        if (city.name === "Elazığ") {
            marker.on('click', function() {
                document.getElementById('elazigModal').style.display = 'block';
            });
        } else if (city.name === "İzmir") {
            marker.on('click', function() {
                document.getElementById('izmirModal').style.display = 'block';
            });
        }
    });

    var elazigModal = document.getElementById('elazigModal');
    var firatModal = document.getElementById('firatModal');
    var izmirModal = document.getElementById('izmirModal');
    var izmirEconomyModal = document.getElementById('izmirEconomyModal');
    var closeBtns = document.querySelectorAll('.modal .close');

    closeBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            elazigModal.style.display = 'none';
            firatModal.style.display = 'none';
            izmirModal.style.display = 'none';
            izmirEconomyModal.style.display = 'none';
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target === elazigModal) {
            elazigModal.style.display = 'none';
        } else if (event.target === firatModal) {
            firatModal.style.display = 'none';
        } else if (event.target === izmirModal) {
            izmirModal.style.display = 'none';
        } else if (event.target === izmirEconomyModal) {
            izmirEconomyModal.style.display = 'none';
        }
    });

    var firatLink = document.getElementById('firatLink');
    firatLink.addEventListener('click', function(event) {
        event.preventDefault();
        elazigModal.style.display = 'none';
        firatModal.style.display = 'block';
    });

    var izmirEconomyLink = document.getElementById('izmirEconomyLink');
    izmirEconomyLink.addEventListener('click', function(event) {
        event.preventDefault();
        izmirModal.style.display = 'none';
        izmirEconomyModal.style.display = 'block';
    });
});