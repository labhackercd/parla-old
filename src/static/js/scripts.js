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
  var parsedEndDate = endDate;
  var parsedInitialDate = initialDate;
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

    return {initialDay: initialDay, initialMonth: initialMonth, endDay: endDay, endMonth: endMonth, parsedInitialDate: parsedInitialDate, parsedEndDate: parsedEndDate}
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

$('.js-filter-form').submit(function() {
  var parameters = getUrlParameters(false, true);
  $('.js-initialDate').val(parameters.parsedInitialDate);
  $('.js-endDate').val(parameters.parsedEndDate);
})

$('.js-toggle-dropdown').click(function(){
  $(this).closest('.js-filter-dropdown').toggleClass('-closed');
});

/*$('.js-filter-options').each(function(){
  $(this).find('.js-filter-option').each(function(){
    $(this).closest('.js-filter-select').find('.js-filter-indicators').append('<span class="indicator js-filter-indicator"></span>')
  });
});

$('.js-filter-indicators').each(function(){
  selectedOptionIndex = $(this).closest('.js-filter-options').find('.js-filter-option.-active').index()

  $(this).find('.js-filter-indicator').eq(selectedOptionIndex).addClass('-active');
});*/

$(this).closest('.js-filter-select').find('.js-filter-option.-active');

$('.js-filter-options').each(function(){
  var currentLabel = $(this).find('.js-filter-option.-active .js-filter-label').text();
  $(this).closest('.js-filter-dropdown').find('.js-selected-label').text(currentLabel);
});

$('.js-change-filter').click(function(){
  changeFilter = $(this);
  direction = null;
  fadeClass = null;
  label = null;
  algorithmID = null;
  updatedFilter = null;
  selectedOptionVal = null;
  selectedOptionLabel = null;
  currentFilter = changeFilter.closest('.js-filter-select').find('.js-filter-option.-active');

  if(changeFilter.is('.-left')) {
    direction = 'left';
    fadeClass = '-faderight'
  } else {
    direction = 'right'
    fadeClass = '-fadeleft'
  }

  currentFilter.addClass(fadeClass).one('animationend', function(){
    if (direction === 'right') {
      if (currentFilter.next().length === 1) {
        updatedFilter = currentFilter.next();
        label = updatedFilter.find('.js-filter-label').text();

      } else {
        updatedFilter = currentFilter.siblings().first();
        label = updatedFilter.find('.js-filter-label').text();
      }

    } else {

      if (currentFilter.prev().length === 1) {
        updatedFilter = currentFilter.prev();
        label = updatedFilter.find('.js-filter-label').text();

      } else {
        updatedFilter = currentFilter.siblings().last();
        label = updatedFilter.find('.js-filter-label').text();
      }
    }

    updatedFilter.addClass('-active');
    algorithmID = updatedFilter.data('formValue');

    currentFilter.removeClass('-active');
    currentFilter.removeClass(fadeClass);

    if (changeFilter.is('.js-update-algorithm')) {
      updateLabel('algorithm', label);
      $('.js-algorithm-input').val(algorithmID);
    }

    if ((updatedFilter).is('.-none')) {
      updateLabel('filter', 'Nenhum');
    }

    if ((updatedFilter).is('.-select')) {

      updatedVal = $(this).find('.js-form-select option:selected').val();
      currentSelect = $(this).find('.js-form-select');

      if ($('.js-selected-label.-filter').text() !== "Nenhum") {
        if (updatedVal === "") {
          updateLabel('filter', 'Nenhum');
        } else {
          updateSelectLabel(currentSelect);
        }
      }
    }

  });
});

function updateSelectLabel(select) {
  if (select.val() !== null) {
    selectedOptionLabelPart = select.data('labelPart');
    selectedOptionLabel = select.find(':selected').text();
    label = selectedOptionLabelPart + selectedOptionLabel
  }

  updateLabel('filter', label);
}

$('.js-form-select').change(function(){
  updateSelectLabel($(this));
});

function updateLabel(labelID, newLabel) {
  $(`.js-selected-label.-${labelID}`).addClass('-fadeout').one('animationend', function(){
    $(this).text(newLabel);
    $(this).removeClass('-fadeout');
    $(this).addClass('-fadein').one('animationend', function(){
      $(this).removeClass('-fadein');
    });
  });
}

$('.js-update-label').click(function(){
  $(this).closest('.js-filter-select').find('.js-filter-option.-active')
});