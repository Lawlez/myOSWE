$(document).ready(function() {

    var $clickMe = $('.click-icon'),
        $card = $('.card');
    
    $card.on('click', function() {
  
          $(this).toggleClass('is-opened');
      $clickMe.toggleClass('is-hidden');
  
      });
  
  });