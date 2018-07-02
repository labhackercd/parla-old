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

$('.js-back-word-chart').on('click', function() {
  $('body').removeClass('-invertedbg');
  $('.nav-bar').removeClass('-negative');
  $('.js-inactive-slider').addClass('-hide');
  $('.js-active-slider').removeClass('-hide');
  $('.js-page-token').removeClass('_hidden');
  $('.js-page-token').addClass('-active');
  $('.js-page:not(.js-page-token)').remove();
  $('.js-back').addClass('_hidden');
  if (visiblePage === 'manifestations' || visiblePage === 'manifestation') {
    $('.ball-animation').removeClass('-invertedbg');
  };
  setNavigationTitle('Parla');
  setNavigationName('');
  visiblePage = 'tokens';


  $('.ball-animation').addClass('-active -reverse').one('animationend', function() {
    enableScroll(tokensScroll);
    $(this).removeClass('-active -reverse');
  });
});

$('.js-back').on('click', function() {
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
      setNavigationName('');
    } else if (visiblePage === 'authors') {
      setNavigationTitle('Parla');
      $('.js-back').addClass('_hidden');
      $('body').removeClass('-invertedbg');
      $('.nav-bar').removeClass('-negative');
    }

    $('.ball-animation').addClass('-active -reverse').one('animationend', function() {
      $(this).removeClass('-active -reverse -invertedbg');
      if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
        enableScroll(authorsScroll);
      } else if (visiblePage === 'authors') {
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
