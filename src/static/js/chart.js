var visiblePage = undefined;

function getUrlParameters() {
  searchParams = new URLSearchParams(window.location.search);
  var initialDate = searchParams.get('initialDate');
  var endDate = searchParams.get('endDate');
  var manifestationType = searchParams.get('manifestationType');
  var urlParameters = {};

  if (initialDate) {
    initialDate = initialDate.split('-');
    initialDate = new Date(initialDate[0], initialDate[1], 1);
    urlParameters['initial_date'] = initialDate.toISOString().split('T')[0];
  }

  if (endDate) {
    endDate = endDate.split('-');
    endDate = new Date(endDate[0], endDate[1], 0);
    urlParameters['final_date'] = endDate.toISOString().split('T')[0];
  }

  if (manifestationType) {
    urlParameters['manifestation_type'] = manifestationType;
  }
  return $.param(urlParameters);
}

function loadData(url, callback) {
  var newArray = [];

  $.ajax({
    type: "GET",
    url: url + '?' + getUrlParameters(),
    beforeSend: function() {
      $('.hex-loading').addClass('-visible');
    },
    success: function(json){
      $('.hex-loading').removeClass('-visible');
      $('.hex-bg').addClass('-visible');
      callback(json);
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
  $('.js-page').removeClass('-active').addClass('_hidden');
  element.removeClass('_hidden').addClass('-active');
}

function zoomInAnimation(element) {
  var bbox = element.getBoundingClientRect();
  var hexPositionTop = bbox.top + bbox.height / 2;
  var hexPositionLeft = bbox.left + bbox.width / 2;
  $(element).parent().addClass('-active');
  var ball = $('.ball-animation');
  ball.addClass('-active')
    .css('top', hexPositionTop + 'px')
    .css('left', hexPositionLeft + 'px');
  ball.one('animationend', function(){
    $('.ball-animation').removeClass('-active');
    $('body').addClass('-invertedbg');
    $('.nav-bar').addClass('-negative');
  });
}

function drawCanvas(selector, chartName) {
  return d3.select(selector)
    .append("div")
    .classed('js-page', true)
    .classed('-active', true)
    .classed("page-content", true)
      .append("svg")
      .classed("js-svg-root", true)
      .attr("data-chart-name", chartName)
      .append('g')
        .classed("js-chart", true)
        .attr("transform-origin", "center top");
}

function createHexagonGroup(canvas, data) {
  return canvas.selectAll("rect")
    .data(data)
    .enter()
      .append('g')
        .classed("hexagon-group", true)
        .classed('js-hexagon-group', true)
        .attr('data-id', function(d, i) {
          return d.id;
        })
        .attr("transform-origin", "center")
        .append('g')
          .attr('id', function(d, i) {
            var chartName = $(this).closest('.js-svg-root').data('chartName');
            return `${chartName}-hexagon-${d.id}`;
          })
          .classed('_hidden', true)
          .classed('-small', true)
          .attr("transform-origin", "center top");
}

function hexagonOnClick(hexagonGroup, callback) {
  hexagonGroup.on('click', function(d, i) {
    zoomInAnimation(this);
    callback(d);
  })
}

function addHexagons(hexagonGroup, radius) {
  hexagonGroup.append("path")
  .classed('js-hexagon', true)
  .attr("fill", "white")
  .attr("d", function(d, i) {
    return drawHexagon(d.size, radius);
  })
}

function positionHexagon(hexagonGroup) {
  hexagonGroup.attr('transform', function(d, i) {
    d['element'] = this;
    bbox = this.getBoundingClientRect();

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
    .attr('x', function(d, i) { return d.element.getBBox().x; })
    .attr('y', function(d, i) { return d.element.getBBox().y; })
    .attr('width', function(d, i) { return d.element.getBBox().width; })
    .attr('height', function(d, i) { return d.element.getBBox().height; })
    .attr('transform', function(d, i) { return `scale(${d.size})`})
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
  svg.width(Math.floor(bbox.width));
  svg.height(Math.ceil(bbox.height));
}

function setTransformOrigin(canvas) {
  var chart = canvas[0][0];
  var svgRoot = $(chart).closest('.js-svg-root');
  var svgBBox = svgRoot[0].getBBox();
  var lastHexagon = $(chart).find('.js-hexagon-group').last()[0];
  var bbox = lastHexagon.getBBox();
  svgRoot.css('transform-origin', `${Math.ceil(bbox.x / svgBBox.width * 100)}% 99.95%`);
}


function tokensChart(tokenId) {
  loadData(`/visualizations/authors/${tokenId}`, function(data) {
    var canvas = drawCanvas('.wrapper','authors');
    var hexagonGroup = createHexagonGroup(canvas, data);
    addHexagons(hexagonGroup, 90);
    positionHexagon(hexagonGroup);
    addText(hexagonGroup);
    $('.ball-animation').on('animationend', function() {
      showHexagonGroup(hexagonGroup);
    })
    hexagonOnClick(hexagonGroup, function(data) {
      $('.ball-animation').addClass('-invertedbg');
      $('.ball-animation').one('animationend', function(){
        $('body').removeClass('-invertedbg');
        $('.nav-bar').removeClass('-negative');
        setNavigationName(data.token);
        authorsScroll = scrollPosition;
        authorsChart(tokenId, data.id);
        hammertime.destroy();
      });
    })
    updateCanvasSize(canvas);
    setTransformOrigin(canvas);
    enableScroll();
    visiblePage = 'authors';
  })
}

function authorsChart(tokenId, authorId) {
  loadData(`/visualizations/authors/${tokenId}/${authorId}/`, function(data) {
    var speechesPage = $(document.createElement('div'))
    speechesPage.addClass('speeches js-page');
    addPage(speechesPage);

    var hexGrid = $("<div class='hex-grid page-content'>");
    data.forEach(function(element, index) {
      var hexWrapper = $(`<div class="hex-wrapper">`);
      var hex = $(`<div class="hex js-manifestation" data-manifestation-id=${element.id}>`);

      var header = $('<div class="header">');
      header.append($('<div class="icon">'));

      var headerContent = $('<div class="content">');
      headerContent.append($(`<span class="date">${element.date}</span>`));
      headerContent.append($(`<span class="time">${element.time}</span>`));

      header.append(headerContent);

      hexWrapper.append(hex);
      hex.append(header);
      hex.append($(`<p>${element.preview}</p>`));
      hexGrid.append(hexWrapper);
    })

    speechesPage.append(hexGrid);
    $('.js-manifestation').on('click', function(e) {
      manifestationPage($(this).data('manifestationId'), tokenId);
    })

    var manifestationPageElement = $(document.createElement('div'))
    manifestationPageElement.addClass('manifestation-page js-page');
    $('main').append(manifestationPageElement);
    visiblePage = 'manifestations';
  })
}

function manifestationPage(manifestationId, tokenId) {
  loadData(`/visualizations/manifestation/${manifestationId}/${tokenId}/`, function(data) {
    var manifestationPage = $('.manifestation-page');

    manifestationPage.html(`
      <div class="header">
        <div class='close-manifestation'></div>
        <strong class='date'>${data.date}  às </strong>
        <strong class='time'>${data.time}</strong>
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

loadData("/visualizations/tokens/", function(data) {
  var canvas = drawCanvas('.wrapper', 'token');
  var hexagonGroup = createHexagonGroup(canvas, data);
  addHexagons(hexagonGroup, 90);
  hexagonOnClick(hexagonGroup, function(data) {
    var currentPage = $(data.element).closest('.js-page');
    currentPage.removeClass('-active');
    $('.ball-animation').one('animationend', function(){
      currentPage.addClass('_hidden');
      setNavigationTitle(data.token);
      $('.js-back').removeClass('_hidden');
    });
    tokensScroll = scrollPosition;
    hammertime.destroy();
    tokensChart(data.stem);
  });
  positionHexagon(hexagonGroup);
  addText(hexagonGroup);
  showHexagonGroup(hexagonGroup);
  updateCanvasSize(canvas);
  setTransformOrigin(canvas);
  enableScroll();
  visiblePage = 'tokens';
})
