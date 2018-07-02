const monthShortNames = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
const today = new Date();

$('.js-slider').dateRangeSlider({
  arrows: false,
  bounds: {
    min: new Date(2015, 0),
    max: new Date(today.getFullYear(), today.getMonth())
  },

  defaultValues:{
    min: new Date(2015, 0),
    max: new Date(today.getFullYear(), today.getMonth())
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