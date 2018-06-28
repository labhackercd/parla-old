$('.filter').click(function() {
  $('.filter-modal').addClass('-active');
});

$('.close').click(function() {
  $('.filter-modal').removeClass('-active');
});

var previousPageRelation = {
  'tokens': null,
  'authors': 'tokens',
  'manifestations': 'authors',
  'manifestation': 'authors',
}

$('.back').on('click', function() {
  if (previousPageRelation[visiblePage]) {
    if (visiblePage === 'manifestation') {
      var manifestationPage = $('.manifestation-page');
      manifestationPage.removeClass('-open');
    };
    if (visiblePage === 'authors') {
      $('.js-inactive-slider').addClass('-hide');
      $('.js-active-slider').removeClass('-hide');
    };
    var current = $('.js-page.-active');
    var prev = current.prev('.js-page');

    current.removeClass('-active');
    $('body').removeClass('-invertedbg');
    current.remove();
    prev.removeClass('_hidden').addClass('-active');

    if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
      $('body').addClass('-invertedbg');
      $('.nav-bar').addClass('-negative');
      $('.js-inactive-slider').addClass('-negative');
    } else if (visiblePage === 'authors') {
      $('body').removeClass('-invertedbg');
      $('.nav-bar').removeClass('-negative');
    }

    $('.ball-animation').addClass('-active -reverse').one('animationend', function() {
      $(this).removeClass('-active -reverse -invertedbg');
      if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
        setNavigationName('');
        enableScroll(authorsScroll);
      } else if (visiblePage === 'authors') {
        setNavigationTitle('Parla');
        $('.js-back').addClass('_hidden');
        enableScroll(tokensScroll);
      }
      visiblePage = previousPageRelation[visiblePage];
      current.addClass('_hidden');
    });
  }
})

function setNavigationTitle(title){
  $('.js-title').text(title);
}

function setNavigationName(name){
  $('.js-name').text(name);
}

document.addEventListener('touchmove', function(e) {
  return false;
});
