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
var interval = undefined;
var datesRange = [];
var currentMonthFromRange = undefined;

$('.js-player-play').click(function(){
  var initialDate = $(".js-slider").dateRangeSlider("values").min;
  var lastDate = $(".js-slider").dateRangeSlider("values").max;

  var currentYear = initialDate.getFullYear();
  var currentMonth = initialDate.getMonth();

  $('.js-slider-min').text((monthShortNames[initialDate.getMonth()]+"/"+initialDate.getFullYear()))
  $('.js-slider-max').text((monthShortNames[lastDate.getMonth()]+"/"+lastDate.getFullYear()))

  var dateDiff = (lastDate.getFullYear() - initialDate.getFullYear())*12 + (lastDate.getMonth() - initialDate.getMonth());

  $('.js-active-slider').addClass('-hide');
  $('.js-range-player').removeClass('-hide');

  for (i = 0; i < dateDiff + 1; i++) {
    datesRange.push(monthShortNames[currentMonth]+"/"+currentYear);

    if (currentMonth == 11) {
      currentMonth = 0;
      currentYear++;
    } else {
      currentMonth++;
    };
  };

  var playerInput = $('.js-player');

  var max = 500;
  var months = datesRange.length;

  var monthSecs = 2;
  var monthRatio = max / months;

  var speed = max / monthRatio * monthSecs * 2;

  var showingMonth = 0;
  playerInput.attr('max', max);

  playerInput.on('input', function(){
    var currentTick = parseInt(playerInput.val());
    var currentMonthFromRange = Math.floor(currentTick / monthRatio);

    $('.js-current-date').html(datesRange[currentMonthFromRange]);

  });

  if (interval) {
    clearInterval(interval)
  };

  function loadInterval() {
      var currentTick = parseInt(playerInput.val());

      currentMonthFromRange = Math.floor(currentTick / monthRatio);
      console.log(currentMonthFromRange)
      if (currentMonthFromRange !== showingMonth) {
        var urlMinMonthValue = ("0" + ((monthShortNames.indexOf(datesRange[currentMonthFromRange].split('/')[0]))+1)).slice(-2);
        var urlMinYearValue = datesRange[currentMonthFromRange].split('/')[1]
        var urlMaxMonthValue = ("0" + ((monthShortNames.indexOf(datesRange[currentMonthFromRange].split('/')[0]))+2)).slice(-2);

        var urlMinValue = urlMinYearValue+"-"+urlMinMonthValue;

        if (urlMinMonthValue == "12") {
          var urlMaxValue = parseInt(urlMinYearValue) + 1 +"-"+"01";

        } else {
          var urlMaxValue = urlMinYearValue +"-"+urlMaxMonthValue
        }
        console.log(urlMaxValue);

        const params = new URLSearchParams(window.location.search);
        params.set('initialDate', urlMinValue);
        params.set('endDate', urlMaxValue);
        window.history.replaceState({}, '', `${location.pathname}?${params}`);

        onlyLoadWordChart(function() {
          interval = setInterval(loadInterval, speed);
        });
        if (interval) {
          clearInterval(interval)
        };
        showingMonth = currentMonthFromRange;
      }

      var nextTick = currentTick + 1;
      if (nextTick <= max) {
        playerInput.val(nextTick).change();
      } else {
        clearInterval(interval);
      }
    }

  interval = setInterval(loadInterval, speed);


});

$('.js-player-pause').click(function(){
  if (interval) {
    clearInterval(interval)
  };
});

$('.js-player-stop').click(function(){
  clearInterval(interval);
  $('.js-player').val(0);
  $('.js-player').off('input');
  $('.js-active-slider').removeClass('-hide');
  $('.js-range-player').addClass('-hide');
});

