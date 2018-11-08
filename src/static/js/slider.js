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
    bound_min = data['bound_min'].split('-');
    bound_max = data['bound_max'].split('-');
    default_min = data['default_min'].split('-');
    default_max = data['default_max'].split('-');
  }
});

$('.js-slider').dateRangeSlider({
  arrows: false,
  bounds: {
    min: new Date(bound_min[0], bound_min[1]-1),
    max: new Date(bound_max[0], bound_max[1]-1)
  },

  defaultValues:{
    min: new Date(default_min[0], default_min[1]-1),
    max: new Date(default_max[0], default_max[1]-1)
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
