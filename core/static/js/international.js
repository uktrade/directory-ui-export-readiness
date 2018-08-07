// Responsive Functionality.
// Adds functionality to help control JS responsive code.
// Needs corresponding CSS (using media queries) to control
// the values. See getResponsiveValue();
// E.g.
//
// Requires...
// dit.js
//
dit.responsive = (new function () {

  // Constants
  var RESET_EVENT = "dit:responsive:reset";
  var RESPONSIVE_ELEMENT_ID = "dit-responsive-size";

  // Sizing difference must be greater than this to trigger the events.
  // This is and attempt to restrict the number of changes when, for
  // example, resizing the screen by dragging.
  var ARBITRARY_DIFFERENCE_MEASUREMENT = 50;

  // Private
  var _self = this;
  var _rotating = false;
  var _responsiveValues = [];
  var _height = 0;
  var _width = 0;


  /* Detect responsive size in play.
   * Use CSS media queries to control z-index values of the
   * #RESPONSIVE_ELEMENT_ID hidden element. Detected value
   * should match up with index number of _responsiveValues
   * array. dit.responsive.mode() will return a string that
   * should give the current responsive mode.
   * E.g. For _responsiveValues array ["desktop", "table", "mobile"],
   * the expected z-index values would be:
   * desktop = 0
   * tablet = 1
   * mobile = 2
   **/
  function getResponsiveValue() {
    return Number($("#" + RESPONSIVE_ELEMENT_ID).css("z-index"));
  };

  /* Create and append a hidden element to track the responsive
   * size. Note: You need to add CSS to set the z-index property
   * of the element. Do this using media queries so that it fits
   * in with other media query controlled responsive sizing.
   * See _responsiveValues variable for expected values (the
   * array index should match the set z-index value).
   **/
  function addResponsiveTrackingElement() {
    var $responsiveElement = $("<span></span>");
    $responsiveElement.attr("id", RESPONSIVE_ELEMENT_ID);
    $responsiveElement.css({
      "height": "1px",
      "position": "absolute",
      "top": "-1px",
      "visibility": "hidden",
      "width": "1px"
    })

    $(document.body).append($responsiveElement);
  }

  /* Create in-page <style> tag containing set media query
   * breakpoints passed to dit.responsive.init()
   * @queries (Object) Media queries and label - e.g. { desktop: "min-width: 1200px" }
   **/
  function addResponsiveSizes(queries) {
    var $style = $("<style id=\"dit-responsive-css\" type=\"text/css\"></style>");
    var css = "";
    var index = 0;
    for(var query in queries) {
      if(queries.hasOwnProperty(query)) {
        _responsiveValues.push(query);
        css += "@media (" + queries[query] + ") {\n";
        css += " #"  + RESPONSIVE_ELEMENT_ID + "{\n";
        css += "   z-index: " + index + ";\n";
        css += "  }\n";
        css += "}\n\n";
        index++;
      }
    }

    $style.text(css);
    $(document.head).append($style);
  }

  /* Triggers jQuery custom event on body for JS elements
   * listening to resize changes (e.g. screen rotate).
   **/
  function bindResizeEvent() {
    $(window).on("resize", function () {
      if (!_rotating) {
        _rotating = true;
        setTimeout(function () {
          if (_rotating) {
            _rotating = false;
            if(dimensionChangeWasBigEnough()) {
              $(document.body).trigger(RESET_EVENT, [_self.mode()]);
            }
          }
        }, "1000");
      }
    });
  }

  /* Calculate if window dimensions have changed enough
   * to trigger a reset event. Note: This was added
   * because some mobile browsers hide the address bar
   * on scroll, which otherwise gives false positive
   * when trying to detect a resize.
   **/
  function dimensionChangeWasBigEnough() {
    var height = $(window).height();
    var width = $(window).width();
    var result = false;

    if (Math.abs(height - _height) >= ARBITRARY_DIFFERENCE_MEASUREMENT) {
      result = true;
    }

    if (Math.abs(width - _width) >= ARBITRARY_DIFFERENCE_MEASUREMENT) {
      result = true;
    }

    // Update internals with latest values
    _height = height;
    _width = width;

    return result;
  }

  /* Return the detected current responsive mode */
  this.mode = function() {
    return _responsiveValues[getResponsiveValue()];
  };

  this.reset = RESET_EVENT;

  this.init = function(breakpoints) {
    addResponsiveSizes(breakpoints);
    addResponsiveTrackingElement();
    bindResizeEvent();
  }
});


// Default (static) page-specific code
//
// Requires
// jQuery
// dit.js
// dit.geolocation.js
// dit.components.js
//
dit.pages.international = (new function () {
  var _great = this;
  var _cache = {
    teasers_site: $(),
    teasers_site_h3: $(),
    teasers_site_p: $()
  }

  // Overwrite stuff in dit.exred because it shouldn't be here.
  // This is due to not developing the required JavaScript loader
  // mechanism due to halted ExRed development.
  dit.components.menu = {
    init: function() {}
  };

  // Page init
  this.init = function() {
    dit.responsive.init({
      "desktop": "min-width: 768px",
      "tablet" : "max-width: 767px",
      "mobile" : "max-width: 480px"
    });

    enhanceLanguageSelector();
    setComponents();
    viewAdjustments(dit.responsive.mode());
    bindResponsiveListener();

    delete this.init; // Run once
  }

  function setComponents() {
    _cache.teasers_site = $("[data-component='teaser-site']");
    _cache.teasers_site_h3 = $("[data-component='teaser-site'] .title");
    _cache.teasers_site_p = $("[data-component='teaser-site'] .text");
  }

  function viewAdjustments(view) {
    switch(view) {
    case "desktop": // Fall through
      case "tablet":
        clearTeaserSiteComponentsAdjustments();
        alignTeaserSiteComponents();
        break;
      case "mobile":
        clearTeaserSiteComponentsAdjustments();
        break;
    }
  }

  function clearTeaserSiteComponentsAdjustments() {
    var clearHeights = dit.utils.clearHeights;
    clearHeights(_cache.teasers_site_h3);
    clearHeights(_cache.teasers_site_p);
    clearHeights(_cache.teasers_site);
  }

  function alignTeaserSiteComponents() {
    var alignHeights = dit.utils.alignHeights;
    alignHeights(_cache.teasers_site_h3);
    alignHeights(_cache.teasers_site_p);
    alignHeights(_cache.teasers_site);
  }

  /* Bind listener for the dit.responsive.reset event
   * to reset the view when triggered.
   **/
  function bindResponsiveListener() {
    $(document.body).on(dit.responsive.reset, function(e, mode) {
      viewAdjustments(mode);
    });
  }

  /* Find and enhance any Language Selector Dialog view
   **/
  function enhanceLanguageSelector() {
    var $dialog = $("[data-component='language-selector-dialog']");
    dit.components.languageSelector.enhanceDialog($dialog, {
      $controlContainer: $("#international-header-bar .container")
    });

    languageSelectorViewInhibitor(false);
  }

  /* Because non-JS view is to show all, we might see a brief glimpse of
   * the open language selector before JS has kicked in to add functionality.
   * We are preventing this by immediately calling a view inhibitor function,
   * and then the enhanceLanguageSelector() function will switch of the
   * inhibitor by calling when component has been enhanced and is ready.
   **/
  languageSelectorViewInhibitor(true);
  function languageSelectorViewInhibitor(activate) {
    var rule = "[data-component='language-selector-dialog'] { display: none; }";
    var style;
    if (arguments.length && activate) {
      // Hide it.
      style = document.createElement("style");
      style.setAttribute("type", "text/css");
      style.setAttribute("id", "language-dialog-view-inhibitor");
      style.appendChild(document.createTextNode(rule));
      document.head.appendChild(style);
    }
    else {
      // Reveal it.
      document.head.removeChild(document.getElementById("language-dialog-view-inhibitor"));
    }
  }

});


$(document).ready(function() {
  dit.pages.international.init();
});
