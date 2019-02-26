var visiblePage = undefined;
window.circleAnimating = undefined;

function getUrlParameters(manualParams = false) {
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

  return $.param(urlParameters);
}

function loadData(url, callback, loadOnly = false, manualParams = false) {
  var newArray = [];
  if (manualParams === false) {
    url = url + '?' + getUrlParameters();
  } else {
    url = url + '?' + getUrlParameters(manualParams);
  }


  $.ajax({
    type: "GET",
    url: url,
    beforeSend: function() {
      $('body').addClass('-processing');

      if (window.circleAnimating === true) {
        $('.js-circle').one('transitionend', function(){
          if ($('body').hasClass('-processing')) {
            $('.js-loading').addClass('-visible');
            $('.js-loading-svg').show();
          }
        });
      } else {
        if ($('body').hasClass('-processing')) {
          $('.js-loading').addClass('-visible');
          $('.js-loading-svg').show();
        }
      }

    },
    success: function(data){
      $('body').removeClass('-processing');

      $('.hex-bg').addClass('-visible');
      $('.js-loading').removeClass('-visible').one('transitionend', function(){
        $('.js-loading-svg').hide();
      });
      if ((window.circleAnimating === true) ) {
        $('.js-circle').one('transitionend', function(){
          $('.js-loading').removeClass('-visible').one('transitionend', function(){
            $('.js-loading-svg').hide();
          });

          if (data.length === 0) {
            $('.js-error-data').removeClass('-hide');
            if (loadOnly === false) {
              $('.js-active-slider').removeClass('-hide');
            } else {
              callback(null);
            }
          } else {
            $('.js-error-data').addClass('-hide');
            callback(data);
          }
        })

      } else {
        if (data.length === 0) {
          $('.js-error-data').removeClass('-hide');
          if (loadOnly === false) {
            $('.js-active-slider').removeClass('-hide');
          } else {
            callback(null);
          }
        } else {
          $('.js-error-data').addClass('-hide');
          callback(data);
        }

      }

    },
    error: function(data) {
      $('body').removeClass('-processing');
      $('.js-error-server').removeClass('-hide');
      $('.js-loading').removeClass('-visible');
    }
  });

  return newArray;

}

function drawHexagon(scale, radius = 90) {
  var h = (Math.sqrt(3)/2),
  scaledRadius = radius * scale,
  hexagonData = [
    { "x": scaledRadius,   "y": 0},
    { "x": scaledRadius / 2,  "y": scaledRadius * h},
    { "x": - scaledRadius / 2,  "y": scaledRadius * h},
    { "x": - scaledRadius,  "y": 0},
    { "x": - scaledRadius / 2,  "y": - scaledRadius * h},
    { "x": scaledRadius / 2, "y": - scaledRadius * h}
  ];

  var draw = d3.svg.line()
    .x(function(d) { return d.x; })
    .y(function(d) { return d.y; })
    .interpolate("cardinal-closed")
    .tension("0.25");

  return draw(hexagonData)
}

function addPage(element) {
  $('.wrapper').append(element);
  element.removeClass('_hidden').addClass('-active');
}

function zoomInAnimation(element) {
  var bbox = $(element).find('.js-hexagon')[0].getBoundingClientRect();
  var hexPositionTop = bbox.top -1 + bbox.height / 2;
  var hexPositionLeft = bbox.left -1 + bbox.width  / 2;
  var offsetX = Math.abs( ($(window).width() / 2) - hexPositionLeft );
  var offsetY = Math.abs( ($(window).height() / 2) - hexPositionTop );
  var deltaX = ($(window).width() / 2) + offsetX
  var deltaY = ($(window).height() / 2) + offsetY;
  window.scaleRatio = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));
  $(element).parent().addClass('-active');
  var circleWrapper = $('.js-circle-wrapper');
  var circle = $('.js-circle');

  circleWrapper.css('transform', `translate(${hexPositionLeft}px, ${hexPositionTop}px)`);
  circle.removeClass('-animating').css('transform', `scale(0) translateZ(0)`).hide();
  $('body').removeClass('-animating');
  window.circleAnimating = true;


  setTimeout(function(){
    $('body').addClass('-animating');
    circle.addClass('-animating').css('transform', `scale(0) translateZ(0)`);
    circle.show().css('transform', `scale(${window.scaleRatio}) translateZ(0)`);

    circle.one('transitionend', function(){
      if ($('body').hasClass('-invertedbg')) {
        $('body').removeClass('-invertedbg');
        $('.nav-bar').removeClass('-negative');

      } else {
        $('body').addClass('-invertedbg');
        $('.nav-bar').addClass('-negative');
      }

      circle.addClass('-fadeout').one('transitionend', function(){

        circle.hide().removeClass('-fadeout');
        $('body').removeClass('-animating');

        if (circle.hasClass('-invertedbg')) {
          circle.removeClass('-invertedbg');
        } else {
          circle.addClass('-invertedbg');
        }
      });

      window.circleAnimating = false;
    });
  }, 1);
}

function drawCanvas(selector, chartName) {
  return d3.select(selector)
    .append("div")
    .classed('js-page', true)
    .classed('js-page-'+chartName, true)
    .classed('-active', true)
    .classed("page-content", true)
      .append("svg")
      .classed("js-svg-root", true)
      .attr("data-chart-name", chartName)
      .append('g')
        .classed("js-chart-wrapper", true)
        .append('g')
          .classed("js-chart", true)
}

function createHexagonGroup(canvas, data, loadOnly = false) {
  return canvas.selectAll("rect")
    .data(data)
    .enter()
      .append('g')
        .classed("hexagon-group", true)
        .classed('js-hexagon-group', true)
        .attr('data-id', function(d, i) {
          return d.id;
        })
        .append('g')
          .attr('id', function(d, i) {
            var chartName = $(this).closest('.js-svg-root').data('chartName');
            return `${chartName}-hexagon-${d.id}`;
          })
          .classed('-small', true)
          // .classed('_hidden', true)
          .classed('_hidden', function(d, i) {
            if (loadOnly === true) {
              return false;
            } else {
              return true;
            }
          });
}

function hexagonOnClick(hexagonGroup, callback) {
  hexagonGroup.on('click', function(d, i) {
    zoomInAnimation(this);
    callback(d);
  })
}

function addHexagons(hexagonGroup, radius) {
  var path = hexagonGroup.append("path")
  .classed('js-hexagon', true)
  .attr("fill", "white")
  .attr("d", function(d, i) {
    return drawHexagon(d.size, radius);
  });

  hexagonGroup.attr("width", function(d, i) {
    return $(this).find('.js-hexagon')[0].getBBox().width;
  });

  hexagonGroup.attr("height", function(d, i) {
    return $(this).find('.js-hexagon')[0].getBBox().height;
  });

  hexagonGroup.insert("image", ".js-hexagon")
  .attr('x', function(d, i) {
    return $(this).siblings('.js-hexagon')[0].getBBox().width / -2;
  })
  .attr('y', function(d, i) {
    return $(this).siblings('.js-hexagon')[0].getBBox().height / -2;
  })
  .attr('width', function(d, i) {
    return $(this).siblings('.js-hexagon')[0].getBBox().width * 1.065;
  })
  .attr('height', function(d, i) {
    return $(this).siblings('.js-hexagon')[0].getBBox().height * 1.065;
  })
  .attr('xlink:href', '/static/img/shadow.png');
}

function positionHexagon(hexagonGroup) {
  hexagonGroup.attr('transform', function(d, i) {
    d['element'] = this;
    bbox = $(this).find('.js-hexagon')[0].getBoundingClientRect();

    var translateX = bbox.width / 2;
    var translateY = bbox.height / 2;

    var previous = hexagonGroup.data()[i - 1];
    if (previous) {
      var chartName = $(this).closest('.js-svg-root').data('chartName');
      var previousBBox = previous.element.getBoundingClientRect();
      previous = d3.select(`#${chartName}-hexagon-${previous.id}`);
      previousTransform = d3.transform(previous.attr("transform"));
      translateX = previousTransform.translate[0];
      translateY = previousTransform.translate[1] + bbox.height;
      if (i % 2 !== 0) {
        translateX = translateX + bbox.width;
      } else {
        translateX = translateX - bbox.width;
      }
    }
    return `translate(${translateX}, ${translateY})`;
  })
}

function addText(hexagonGroup) {
  hexagonGroup.append("foreignObject")
    .attr('x', 0)
    .attr('y', 0)
    .attr('width', 1)
    .attr('height', 1)
    .attr('transform', function(d, i) { return `scale(${d.size})`})
    .attr('overflow', 'visible')
    .append('xhtml:div')
      .attr("class", 'text-box')
      .append('xhtml:p')
        .attr('class', 'text')
        .text((d) => {return d.token;})
}

function showHexagonGroup(hexagonGroup) {
  hexagonGroup.each(function(d, i) {
    setTimeout(function() {
      $(d.element).removeClass('_hidden');
    }, i * 150)
  })
}

function updateCanvasSize(canvas) {
  var chart = canvas[0][0];
  var bbox = chart.getBBox();

  var svg = $(chart).closest('.js-svg-root');
  svg.attr('width', '100%');
  svg.attr('viewBox', `0 0 ${bbox.width} 565`)
}

function setTransformOrigin(canvas) {
  var chart = canvas[0][0];
  var chartChildren = $(chart).children();
  var svgRoot = $(chart).closest('.js-svg-root');
  var svgBBox = svgRoot[0].getBBox();
  var lastHexagon = $(chart).find('.js-hexagon-group').last()[0];
  var bbox = lastHexagon.getBBox();
  var bboxYPos = bbox.y + bbox.height * 2;

  if (chartChildren.length % 2 == 0) {
    $(chart).css('transform-origin', `${bbox.x}px ${bboxYPos}px `);
  } else {
    $(chart).css('transform-origin', `${(bbox.x + bbox.width)}px ${bboxYPos}px `);
  }
}

function onlyLoadWordChart(callback, manualParams = false) {
  $('.js-page').remove();
  loadData("/visualizations/tokens/", function(data) {
    if (data) {
      var canvas = drawCanvas('.wrapper', 'token');
      var hexagonGroup = createHexagonGroup(canvas, data, loadOnly = true);
      addHexagons(hexagonGroup, 90);
      hexagonOnClick(hexagonGroup, function(data) {
        var currentPage = $(data.element).closest('.js-page');
        currentPage.removeClass('-active');
        $('.js-active-slider').addClass('-hide');
        $('.js-player-controls').addClass('-hide');
        $('.js-range-player').addClass('-hide');
        if (interval) {
          clearInterval(interval)
          $('.js-player-pause').addClass('-hide');
          $('.js-player-play').removeClass('-hide');
        };
        $('.js-circle').one('transitionend', function(){
          currentPage.addClass('_hidden');
          setNavigationTitle(data.token);
          $('.js-back').removeClass('_hidden');

        });
        tokensChart(data.stem);
        tokensScroll = scrollPosition;
        hammertime.destroy();
      });
      positionHexagon(hexagonGroup);
      addText(hexagonGroup);
      showHexagonGroup(hexagonGroup);
      updateCanvasSize(canvas);
      setTransformOrigin(canvas);
      enableScroll();
      visiblePage = 'tokens';
    }
    callback();
  }, loadOnly = true, manualParams);
}

function wordChart() {
  $('.js-page').remove();
  const params = new URLSearchParams(window.location.search);
  if (params.get('initialDate') !== null) {
    initialDate = params.get('initialDate').split('-');
    initialDate = new Date(initialDate[0], initialDate[1]-1);
    endDate = params.get('endDate').split('-');
    endDate = new Date(endDate[0], endDate[1]-1);
    $(".js-slider").dateRangeSlider("values", new Date(initialDate), new Date(endDate));
  };

  loadData("/visualizations/tokens/", function(data) {
    var canvas = drawCanvas('.wrapper', 'token');
    var hexagonGroup = createHexagonGroup(canvas, data);
    addHexagons(hexagonGroup, 90);
    hexagonOnClick(hexagonGroup, function(data) {
      var currentPage = $(data.element).closest('.js-page');
      currentPage.removeClass('-active');
      $('.js-active-slider').addClass('-hide');
      $('.js-player-controls').addClass('-hide');  
      $('.js-range-player').addClass('-hide');
      if (interval) {
        clearInterval(interval)
        $('.js-player-pause').addClass('-hide');
        $('.js-player-play').removeClass('-hide');
      };
      $('.js-circle').one('transitionend', function(){
        currentPage.addClass('_hidden');
        setNavigationTitle(data.token);
        $('.js-back').removeClass('_hidden');

      });
      tokensChart(data.stem);
      tokensScroll = scrollPosition;
      hammertime.destroy();
    });
    positionHexagon(hexagonGroup);
    addText(hexagonGroup);
    showHexagonGroup(hexagonGroup);
    updateCanvasSize(canvas);
    setTransformOrigin(canvas);
    enableScroll();
    $('.js-active-slider').removeClass('-hide');
    visiblePage = 'tokens';
  });
};

wordChart();

function tokensChart(tokenId) {
  loadData(`/visualizations/authors/${tokenId}`, function(data) {
    var canvas = drawCanvas('.wrapper','authors');
    var hexagonGroup = createHexagonGroup(canvas, data);
    addHexagons(hexagonGroup, 90);
    showHexagonGroup(hexagonGroup);
    hexagonOnClick(hexagonGroup, function(data) {
      var currentPage = $(data.element).closest('.js-page');
      $('.js-circle').one('transitionend', function(){
        currentPage.addClass('_hidden');
        currentPage.removeClass('-active');
        setNavigationName(data.token);
      });
      authorsChart(tokenId, data.id);
      authorsScroll = scrollPosition;
      hammertime.destroy();

    })

    positionHexagon(hexagonGroup);
    addText(hexagonGroup);
    var minValue = $(".js-slider").dateRangeSlider("values").min;
    var maxValue = $(".js-slider").dateRangeSlider("values").max;
    var parsedMinValue = monthShortNames[minValue.getMonth()]+"/"+minValue.getFullYear()
    var parsedMaxValue = monthShortNames[maxValue.getMonth()]+"/"+maxValue.getFullYear()
    $('.js-slider-min').text(parsedMinValue);
    $('.js-slider-max').text(parsedMaxValue);
    $('.js-inactive-slider').removeClass('-hide');
    updateCanvasSize(canvas);
    setTransformOrigin(canvas);
    enableScroll();
    visiblePage = 'authors';
  })
}

function calculateSpeechHexagonSize(ratio) {
  if (ratio <= 1 && ratio > 0.8333) {
    return 1;
  } else if (ratio <= 0.8333 && ratio > 0.6666) {
    return 0.8333;
  } else if (ratio <= 0.6666 && ratio > 0.5) {
    return 0.6666;
  } else if (ratio <= 0.5 && ratio > 0.3334) {
    return 0.5;
  } else if (ratio <= 0.3334 && ratio > 0.1666) {
    return 0.3334;
  } else {
    return 0.1666;
  }
}

function authorsChart(tokenId, authorId) {
  loadData(`/visualizations/authors/${tokenId}/${authorId}/`, function(data) {
    var speechesPage = $(document.createElement('div'))
    speechesPage.addClass('speeches js-page js-page-speeches');

    var hexGrid = $("<div class='speeches-list page-content'>");

    data.forEach(function(element, index) {
      var content = $('<div class="content">');

      var timestamp = $('<div class="timestamp">');

      timestamp.append($(`<span class="date">${element.date}</span>`));
      timestamp.append($(`<span> às </span>`));
      timestamp.append($(`<span class="time">${element.time}</span>`));

      content.append(timestamp);
      content.append($(`<p>${element.preview}</p>`));

      var hex = $(`<div class="hex" style="transform: scale(${calculateSpeechHexagonSize(element.ratio)})">`);

      var item = $(`<div class="item js-manifestation" data-manifestation-id=${element.id}>"`);
      hexGrid.append(item);
      item.append(hex);
      item.append(content);


      addPage(speechesPage);
      speechesPage.append(hexGrid);
      visiblePage = 'manifestations';
    });

    $('.manifestation-page').remove();
    $('.js-manifestation').on('click', function(e) {
      manifestationPage($(this).data('manifestationId'), tokenId);
    })
    var manifestationPageElement = $(document.createElement('div'))
    manifestationPageElement.addClass('manifestation-page js-page js-page-manifestation');
    $('main').append(manifestationPageElement);
  })
}

function manifestationPage(manifestationId, tokenId) {
  loadData(`/visualizations/manifestation/${manifestationId}/${tokenId}/`, function(data) {
    var manifestationPage = $('.manifestation-page');
    if (data.indexes) {
      var indexes = data.indexes;
    } else {
      var indexes = "-";
    }

    manifestationPage.html(`
      <div class="header">
        <div class='close-manifestation'></div>
        <strong class='date'>${data.date}  às </strong>
        <strong class='time'>${data.time}</strong>
      </div>
      <div class="indexes">
        <span>Indexação</span>
        <p>${indexes}</p>
      </div>
      <div class="content">
        <p>${data.content}</p>
      </div>
    `);
    manifestationPage.addClass('-open');

    $('.close-manifestation').on('click', function() {
      manifestationPage.removeClass('-open');
    });
    visiblePage = 'manifestation';
  })
}

$(".js-slider").bind("valuesChanged", function(e, data){
  var minValue = $(".js-slider").dateRangeSlider("values").min;
  var maxValue = $(".js-slider").dateRangeSlider("values").max;
  var parsedMinValue = minValue.getFullYear()+"-"+("0" + (minValue.getMonth() + 1)).slice(-2);
  var parsedMaxValue = maxValue.getFullYear()+"-"+("0" + (maxValue.getMonth() + 1)).slice(-2);

  const params = new URLSearchParams(window.location.search);
  params.set('initialDate', parsedMinValue);
  params.set('endDate', parsedMaxValue);
  window.history.replaceState({}, '', `${location.pathname}?${params}`);

  if (!hammertime === undefined){
    hammertime.destroy();
  };

  wordChart();
});
