$('.js-player').rangeslider({

    polyfill: false,

    rangeClass: 'controls',
    disabledClass: 'rangeslider--disabled',
    horizontalClass: 'rangeslider--horizontal',
    verticalClass: 'rangeslider--vertical',
    fillClass: 'fill',
    handleClass: 'handle',

    onInit: function() {
      $('.js-range-player .handle').prepend('<span class="currentdate js-current-date"></span>')
    }
});
selectedThroughPlayer = false;
interval = undefined;
currentMonthFromRange = 0;
datesRange = [];

function generateMonthRangeUrlParam() {
  var urlMinMonthValue = ("0" + ((monthShortNames.indexOf(datesRange[currentMonthFromRange].split(' ')[0]))+1)).slice(-2);
  var urlMinYearValue = datesRange[currentMonthFromRange].split(' ')[1]
  var urlMaxMonthValue = ("0" + ((monthShortNames.indexOf(datesRange[currentMonthFromRange].split(' ')[0]))+2)).slice(-2);


  var urlMinValue = urlMinYearValue+"-"+urlMinMonthValue;

  if (urlMinMonthValue == "12") {
    var urlMaxValue = parseInt(urlMinYearValue) + 1 +"-"+"01";

  } else {
    var urlMaxValue = urlMinYearValue +"-"+urlMaxMonthValue
  }

  const params = new URLSearchParams(window.location.search);
  params.set('initialDate', urlMinValue);
  params.set('endDate', urlMaxValue);
  var manualParams = `?${params}`;

  return manualParams;
}

$('.js-player-play').click(function(){
  selectedThroughPlayer = true;

  $(this).addClass('-hide');
  $('.js-player-pause').removeClass('-hide');
  $('.js-player-stop').removeClass('-hide');

  datesRange = [];

  var initialDate = $(".js-slider").dateRangeSlider("values").min;
  var lastDate = $(".js-slider").dateRangeSlider("values").max;

  var subtractedLastDate = new Date($(".js-slider").dateRangeSlider("values").max.getTime());
  subtractedLastDate.setDate(subtractedLastDate.getDate() - 1);

  var currentYear = initialDate.getFullYear();
  var currentMonth = initialDate.getMonth();

  var nextTick = null;
  var currentTick = null;

  function loadInterval() {
    currentTick = parseInt(playerInput.val());

    currentMonthFromRange = Math.floor(currentTick / monthRatio);

    if (currentMonthFromRange !== showingMonth) {

      onlyLoadWordChart(function() {
        interval = setInterval(loadInterval, speed);
      }, generateMonthRangeUrlParam());

      if (interval) {
        clearInterval(interval)
      };

      showingMonth = currentMonthFromRange;
    }

    nextTick = currentTick + 1;
    if (nextTick <= max) {
      playerInput.val(nextTick).change();
    } else {
      clearInterval(interval);
    }
  }

  $('.js-player-slider-min').text('01/' + (monthShortNames[initialDate.getMonth()]+"/"+initialDate.getFullYear()))
  $('.js-player-slider-max').text(subtractedLastDate.getUTCDate() + '/' + (monthShortNames[subtractedLastDate.getMonth()]+"/"+subtractedLastDate.getFullYear()))

  var dateDiff = (lastDate.getFullYear() - initialDate.getFullYear())*12 + (lastDate.getMonth() - initialDate.getMonth());

  $('.js-active-slider').addClass('-hide');
  $('.js-range-player').removeClass('-hide');

  for (i = 0; i < dateDiff; i++) {
    datesRange.push(monthShortNames[currentMonth]+" "+currentYear);

    if (currentMonth == 11) {
      currentMonth = 0;
      currentYear++;
    } else {
      currentMonth++;
    };
  };

  onlyLoadWordChart(function(){}, generateMonthRangeUrlParam());


  var playerInput = $('.js-player');

  var max = 500;
  var months = datesRange.length;

  var monthSecs = 2;
  var monthRatio = max / months;

  var speed = max / monthRatio * monthSecs * 2;

  var showingMonth = 0;
  playerInput.attr('max', max);

  previousCurrentMonthFromRange = 0

  playerInput.on('input', function(){

    currentTick = parseInt(playerInput.val());

    if (currentTick < max) {
      if (currentMonthFromRange != previousCurrentMonthFromRange || currentTick == 1) {
        $('.js-current-date').html(`<span>${datesRange[currentMonthFromRange]}</span>`);
      }
    }

    previousCurrentMonthFromRange = currentMonthFromRange
    currentMonthFromRange = Math.floor(currentTick / monthRatio);


    if (currentTick == max) {
      if (interval) {
        clearInterval(interval)
        $('.js-player-pause').addClass('-hide');
        $('.js-player-play').removeClass('-hide');
      };
    }

  });

  if (interval) {
    clearInterval(interval);
  };

  interval = setInterval(loadInterval, speed);
});

$('.js-player-pause').click(function(){
  $(this).addClass('-hide');
  $('.js-player-play').removeClass('-hide');

  if (interval) {
    clearInterval(interval);
  };
});

$('.js-player-stop').click(function(){
  selectedThroughPlayer = false;
  if (interval) {
    clearInterval(interval);
  };
  currentMonthFromRange = 0;
  $(this).addClass('-hide');
  $('.js-player-pause').addClass('-hide');
  $('.js-player-play').removeClass('-hide');
  clearInterval(interval);
  $('.js-player').val(0);
  $('.js-player').off('input');
  $('.js-active-slider').removeClass('-hide');
  $('.js-range-player').addClass('-hide');
  onlyLoadWordChart(function(){});
});

