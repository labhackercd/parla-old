$('.js-player').rangeslider({

    polyfill: false,

    // Default CSS classes
    rangeClass: 'controls',
    disabledClass: 'rangeslider--disabled',
    horizontalClass: 'rangeslider--horizontal',
    verticalClass: 'rangeslider--vertical',
    fillClass: 'fill',
    handleClass: 'handle',

    onInit: function() {
      $('.js-range-player .handle').prepend('<span class="currentdate js-current-date">JAN/2016</span>')
    }
});

var input = $('.js-player');
var currentDate = $('.js-current-date');
var monthList = ['jan/17', 'fev/17', 'mar/17', 'abr/17']

var max = 500;
var months = monthList.length;

var monthSecs = 2;
var monthRatio = max / months;

var speed = max / monthRatio * monthSecs * 2;

input.attr('max', max);

var interval = undefined;


$('.js-player-play').click(function(){
  $('.js-active-slider').addClass('-hide');
  $('.js-range-player').removeClass('-hide');
  interval = setInterval(function() {
    var currentTick = parseInt(input.val());
    var currentMonth = Math.floor(currentTick / monthRatio);
    currentDate.html(monthList[currentMonth]);

    var nextTick = currentTick + 1;
    if (nextTick <= max) {
      input.val(nextTick).change();
    } else {
      clearInterval(interval);
    }
  }, speed)
});

$('.js-player-pause').click(function(){
  if (interval) {
    clearInterval(interval);
  }
});

$('.js-player-stop').click(function(){
  clearInterval(interval);
  input.val(0);
  $('.js-active-slider').removeClass('-hide');
  $('.js-range-player').addClass('-hide');
});

var initialDate = $(".js-slider").dateRangeSlider("values").min;
var lastDate = $(".js-slider").dateRangeSlider("values").max;

// Returns an array of dates between the two dates
var getDates = function(startDate, endDate) {
  var dates = [],
      currentDate = startDate,
      addDays = function(days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
      };
  while (currentDate <= endDate) {
    dates.push(currentDate);
    currentDate = addDays.call(currentDate, 1);
  }
  return dates;
};

// Usage
var dates = getDates(initialDate, lastDate);
console.log(dates);

var initialDate = $(".js-slider").dateRangeSlider("values").min;
var lastDate = $(".js-slider").dateRangeSlider("values").max;

var dateDiff = (lastDate.getFullYear() - initialDate.getFullYear())*12 + (lastDate.getMonth() - initialDate.getMonth())