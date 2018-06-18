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

$('.back').on('click', function() {
  if (previousPageRelation[visiblePage]) {
    if (visiblePage === 'manifestation') {
      var manifestationPage = $('.manifestation-page');
      manifestationPage.removeClass('-open');
    }
    var current = $('.js-page.-active');
    var prev = current.prev('.js-page');
    current.addClass('_hidden');
    current.one('transitionend', function(){
      current.removeClass('-active');
      $('body').removeClass('-invertedbg');
      current.remove();
      prev.removeClass('_hidden').addClass('-active');
      $('.nav-bar').removeClass('-negative');
      $('.ball-animation').addClass('-active -reverse').one('animationend', function(){
        $(this).removeClass('-active -reverse');
        if (visiblePage === 'manifestation' || visiblePage === 'manifestations') {
          setNavigationName('');
          enableScroll(authorsScroll);
        } else if (visiblePage === 'authors') {
          setNavigationTitle('Babel');
          $('.js-back').addClass('_hidden');
          enableScroll(tokensScroll);
        }
        visiblePage = previousPageRelation[visiblePage];
      });
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
