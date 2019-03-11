const monthShortNames = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
const today = new Date();
var bound_min = {};
var bound_max = {};
var default_min = {};
var default_max = {};


$.ajax({
  url: "/visualizations/date-range/",
  async: false,
  dataType: 'json',
  success: function(data) {
    bound_min = [data['bound_min'].split('-')[0], '01']; // First month of the first year in the database
    bound_max = data['bound_max'].split('-');
    default_min = data['default_min'].split('-');
    default_max = data['default_max'].split('-');

    var parsedMinValue = `${default_min[0]}-${default_min[1]}`
    var parsedMaxValue = `${default_max[0]}-${default_max[1]}`
    getUrlParameters();

    if (searchParams.get('initialDate') === null || searchParams.get('endDate') === null) {
      const params = new URLSearchParams(window.location.search);
      params.set('initialDate', parsedMinValue);
      params.set('endDate', parsedMaxValue);
      window.history.replaceState({}, '', `${location.pathname}?${params}`);
    }

    $('.js-slider').dateRangeSlider({
      arrows: false,
      bounds: {
        min: new Date(bound_min[0], bound_min[1]-1),
        max: new Date(bound_max[0], bound_max[1]-1),
      },

      defaultValues:{
        min: new Date(default_min[0], default_min[1]-1),
        max: new Date(default_max[0], default_max[1])
      },

      range:{
        min: {months: 1}
      },

      step:{
        months: 1
      },

      formatter:function(val){
        var month = val.getMonth();
        return monthShortNames[month];
      },

      scales: [
      {
        first: function(value){ return value; },
        end: function(value) {return value; },
        next: function(value){
          var next = new Date(value);
          return new Date(next.setMonth(value.getMonth() + 1));
        },
        label: function(value){
          return null;
        },
        format: function(tickContainer, tickStart, tickEnd){
          tickContainer.addClass("month-label");
        }
      },
      {
        first: function(value){ return value; },
        end: function(value) {return value; },
        next: function(value){
          var next = new Date(value);
          return new Date(next.setFullYear(value.getFullYear() + 1));
        },
        label: function(value){
          return value.getFullYear();
        },
        format: function(tickContainer, tickStart, tickEnd){
          tickContainer.addClass("year-label");
        }
      }],

    });

    setTimeout(function(){
      currentMinValue = $('.js-slider').dateRangeSlider("values").min;
      currentMaxValue = $('.js-slider').dateRangeSlider("values").max;
    }, 1000)

    var timelineValues = getUrlParameters(false, true);

    var leftLabelText = $('.ui-rangeSlider-leftLabel .ui-rangeSlider-label-inner');
    var rightLabelText = $('.ui-rangeSlider-rightLabel .ui-rangeSlider-label-inner');

    var leftLabelDay = `<span>${timelineValues.initialDay}</span>`;  
    var leftLabelMonth = `<span>${timelineValues.initialMonth}</span>`;  
    var rightLabelDay = `<span>${timelineValues.endDay}</span>`;  
    var rightLabelMonth = `<span>${timelineValues.endMonth}</span>`;  

    leftLabelText.empty().append(leftLabelDay, leftLabelMonth);
    rightLabelText.empty().append(rightLabelDay, rightLabelMonth);

    if (getUrlParameters(false, true).parsedEndDate === parsedMaxValue) {
      rightLabelText.empty().append(`<span>${new Date().getUTCDate()}</span>`, rightLabelMonth);
    } else {
      rightLabelText.empty().append(rightLabelDay, rightLabelMonth);
    }
  }
});



