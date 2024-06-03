$(document).ready(function () {
    // Check API status
    $.get("http://0.0.0.0:5001/api/v1/status/", function (data) {
        if (data.status === "OK") {
            $("#api_status").addClass("available");
        } else {
            $("#api_status").removeClass("available");
        }
    });

    function fetchPlaces(filters = {}) {
        $.ajax({
            url: "http://0.0.0.0:5001/api/v1/places_search/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(filters),
            success: function (data) {
                $('.places').empty();
                for (let place of data) {
                    $('.places').append(
                        `<article>
                            <div class="title_box">
                                <h2>${place.name}</h2>
                                <div class="price_by_night">$${place.price_by_night}</div>
                            </div>
                            <div class="information">
                                <div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>
                                <div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>
                                <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>
                            </div>
                            <div class="description">
                                ${place.description}
                            </div>
                            <div class="reviews">
                                <h2>Reviews <span data-place-id="${place.id}" class="toggle-reviews">show</span></h2>
                                <div class="review-list"></div>
                            </div>
                        </article>`
                    );
                }
            }
        });
    }

    // Fetch initial places
    fetchPlaces();

    // Handle amenities, states, and cities checkbox changes
    const amenities = {};
    const states = {};
    const cities = {};

    $('input[type="checkbox"]').change(function () {
        const isChecked = this.checked;
        const id = $(this).data('id');
        const name = $(this).data('name');

        if ($(this).closest('.locations').length) {
            // Handle states and cities
            if (isChecked) {
                if ($(this).parent().has('ul').length) {
                    states[id] = name;
                } else {
                    cities[id] = name;
                }
            } else {
                if ($(this).parent().has('ul').length) {
                    delete states[id];
                } else {
                    delete cities[id];
                }
            }
            $('.locations h4').text([...Object.values(states), ...Object.values(cities)].join(', '));
        } else {
            // Handle amenities
            if (isChecked) {
                amenities[id] = name;
            } else {
                delete amenities[id];
            }
            $('.amenities h4').text(Object.values(amenities).join(', '));
        }
    });

    // Handle search button click
    $('button').click(function () {
        fetchPlaces({
            amenities: Object.keys(amenities),
            states: Object.keys(states),
            cities: Object.keys(cities)
        });
    });

    // Handle review toggle
    $(document).on('click', '.toggle-reviews', function () {
        const placeId = $(this).data('place-id');
        const reviewList = $(this).closest('.reviews').find('.review-list');
        if ($(this).text() === 'show') {
            $.get(`http://0.0.0.0:5001/api/v1/places/${placeId}/reviews`, function (data) {
                reviewList.empty();
                for (let review of data) {
                    reviewList.append(`<div class="review">
                        <h3>From ${review.user.first_name} ${review.user.last_name} the ${new Date(review.created_at).toLocaleDateString()}</h3>
                        <p>${review.text}</p>
                    </div>`);
                }
                $(this).text('hide');
            }.bind(this));
        } else {
            reviewList.empty();
            $(this).text('show');
        }
    });
});

