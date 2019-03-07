var visiblePage = undefined;
window.circleAnimating = undefined;

function getUrlParameters(manualParams = false, returnTimelineValues = false) {
  searchParams = null;
  if (manualParams === false) {
    searchParams = new URLSearchParams(window.location.search);
  } else {
    searchParams = new URLSearchParams(manualParams);
  }
  var initialDate = searchParams.get('initialDate');
  var endDate = searchParams.get('endDate');
  var algorithm = searchParams.get('algorithm');
  var urlParameters = {};

  if (initialDate) {
    initialDate = initialDate.split('-');
    initialDate = new Date(initialDate[0], initialDate[1]-1, 1);
    urlParameters['initial_date'] = initialDate.toISOString().split('T')[0];
  }

  if (endDate) {
    endDate = endDate.split('-');
    endDate = new Date(endDate[0], endDate[1]-1, 0);
    urlParameters['final_date'] = endDate.toISOString().split('T')[0];
  }

  if (algorithm) {
    urlParameters['algorithm'] = algorithm;
  }

  if (returnTimelineValues) {
    var initialDay = initialDate.getUTCDate()
    var initialMonth = monthShortNames[initialDate.getMonth()]
    var endDay = endDate.getUTCDate()
    var endMonth = monthShortNames[endDate.getMonth()]

    return {initialDay: initialDay, initialMonth: initialMonth, endDay: endDay, endMonth: endMonth}
  }

  return $.param(urlParameters);
}

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
  backToWordChart = true;
  $('.js-circle').removeClass('-invertedbg');
  zoomOutAnimation();
  setTimeout(function(){
    $('body').removeClass('-invertedbg');
    $('.nav-bar').removeClass('-negative');
    $('.js-inactive-slider').addClass('-hide');
    $('.js-page-token').removeClass('_hidden');
    $('.js-page-token').addClass('-active');
    $('.js-page:not(.js-page-token)').remove();
    $('.js-back').addClass('_hidden');
    $('.js-player-controls').removeClass('-hide');
    if (selectedThroughPlayer === true) {
      $('.js-range-player').removeClass('-hide');  
    } else {
      $('.js-active-slider').removeClass('-hide');
    }
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
  }, 410);
});

$('.js-back').on('click', function() {
  backToWordChart = false;
  zoomOutAnimation();
  setTimeout(function(){
    if (previousPageRelation[visiblePage]) {
      if (visiblePage === 'manifestation') {
        var manifestationPage = $('.manifestation-page');
        manifestationPage.removeClass('-open');
      };
      if (visiblePage === 'authors') {
        $('.js-player-controls').removeClass('-hide');
        $('.js-inactive-slider').addClass('-hide');

        if (selectedThroughPlayer === true) {
          $('.js-range-player').removeClass('-hide');  

        } else {
          $('.js-active-slider').removeClass('-hide');
        }
      };
      var current = $('.js-page.-active');
      var prev = current.prev('.js-page');

      current.removeClass('-active');
      current.remove();
      prev.removeClass('_hidden').addClass('-active');
      hammertime.destroy();

      if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
        setNavigationName('');
      } else if (visiblePage === 'authors') {
        setNavigationTitle('Parla');
        $('.js-back').addClass('_hidden');
      }


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
  }, 410);
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

  circle.removeClass('-animating').addClass('-reverse').show().css('transform', `scale(${window.scaleRatio}) translateZ(0)`);
  $('body').removeClass('-animating');
  window.circleAnimating = true;

  if (backToWordChart === false) {
    if (circle.hasClass('-invertedbg')) {
      circle.removeClass('-invertedbg');
    } else {
      circle.addClass('-invertedbg');
    }
  }

  setTimeout(function(){
    $('body').addClass('-animating');
    circle.addClass('-animating -fadein').one('transitionend', function(){

      if (backToWordChart === false) {
        if ($('body').hasClass('-invertedbg')) {
          $('body').removeClass('-invertedbg');
          $('.nav-bar').removeClass('-negative');

        } else {
          $('body').addClass('-invertedbg');
          $('.nav-bar').addClass('-negative');
        }
      }

      circle.css('transform', `scale(0) translateZ(0)`).one('transitionend', function(){
        circle.removeClass('-animating -fadein -reverse');
        $('body').removeClass('-animating');
      });
    });


    window.circleAnimating = false;
  }, 1);
}

document.addEventListener('touchmove', function(e) {
  return false;
});
