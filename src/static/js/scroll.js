var hammertime;
var tokensScroll = 0;
var authorsScroll = 0;
var scrollPosition = 0;
function enableScroll(initialPosition = 0) {
  scrollPosition = initialPosition;
  var idealHexagonNumber = 20;
  var hexagonsNumber = $('.js-page.-active .js-hexagon-group').length;

  var maxScroll = 30000 * (hexagonsNumber / idealHexagonNumber);
  var maxScale = 600 ** (hexagonsNumber / idealHexagonNumber);

  hammertime = new Hammer($(".wrapper")[0]);

  hammertime.get('pan').set({ direction: Hammer.DIRECTION_ALL });

  hammertime.on('panup pandown', function(e) {
    scrollPosition = scrollPosition - e.deltaY;
    if (scrollPosition < 0) {
      scrollPosition = 0;
    } else if (scrollPosition > maxScroll) {
      scrollPosition = maxScroll;
    }

    var scrollRatio = scrollPosition / maxScroll;

    var svg = $('.js-page.-active > .js-svg-root')[0];
    var scale = svg.style.getPropertyValue('transform').indexOf('scale');
    if (scale === -1) {
      scale = 1;
    } else {
      scale = maxScale ** scrollRatio;
    }

    $(svg).css('transform', `scale(${scale})`);
  });
}
