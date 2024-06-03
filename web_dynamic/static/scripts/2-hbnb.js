$(document).ready(function() {
  const selectedAmenities = {};

  $('input[type="checkbox"]').change(function() {
    if ($(this).is(':checked')) {
      selectedAmenities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete selectedAmenities[$(this).attr('data-id')];
    }

    const amenitiesList = Object.values(selectedAmenities).join(', ');
    if (amenitiesList.length > 0) {
      $('.amenities h4').text(amenitiesList);
    } else {
      $('.amenities h4').html('&nbsp;');
    }
  });

  $.get('http://0.0.0.0:5001/api/v1/status/', function(data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
});

