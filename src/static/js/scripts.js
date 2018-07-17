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
  zoomOutAnimation();
  $('body').removeClass('-invertedbg');
  $('.nav-bar').removeClass('-negative');
  $('.js-inactive-slider').addClass('-hide');
  $('.js-active-slider').removeClass('-hide');
  $('.js-page-token').removeClass('_hidden');
  $('.js-page-token').addClass('-active');
  $('.js-page:not(.js-page-token)').remove();
  $('.js-back').addClass('_hidden');
  if (visiblePage === 'manifestations' || visiblePage === 'manifestation') {
    $('.js-circle').removeClass('-invertedbg');
  };
  setNavigationTitle('Parla');
  setNavigationName('');
  visiblePage = 'tokens';
  hammertime.destroy();


  $('.js-circle').addClass('-active -reverse').one('transitionend', function() {
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
    current.remove();
    prev.removeClass('_hidden').addClass('-active');
    hammertime.destroy();

    if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
      $('.js-inactive-slider').addClass('-negative');
      setNavigationName('');
    } else if (visiblePage === 'authors') {
      setNavigationTitle('Parla');
      $('.js-back').addClass('_hidden');
    }

    zoomOutAnimation();

    $('.js-circle').one('transitionend', function() {

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

function zoomOutAnimation() {
  var circleWrapper = $('.js-circle-wrapper');
  var circle = $('.js-circle');

  circle.removeClass('-animating').css('transform', `scale(${window.scaleRatio}) translateZ(0)`);
  $('body').removeClass('-animating');
  window.circleAnimating = true;

  if ($('body').hasClass('-invertedbg')) {
    circle.removeClass('-invertedbg');
    $('body').removeClass('-invertedbg');
    $('.nav-bar').removeClass('-negative');

  } else {
    circle.addClass('-invertedbg');
    $('body').addClass('-invertedbg');
    $('.nav-bar').addClass('-negative');
  }
  setTimeout(function(){
    circle.addClass('-animating').css('transform', `scale(0) translateZ(0)`);
    circle.css('transform', `scale(0) translateZ(0)`);
    $('body').addClass('-animating');

    circle.one('transitionend', function(){
      circle.removeClass('-animating');
      $('body').removeClass('-animating');
    });

    window.circleAnimating = false;
  }, 1);
}

document.addEventListener('touchmove', function(e) {
  return false;
});
