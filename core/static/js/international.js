// Geo Location Functionality.
// Uses third-party (AJAX request) data to report the users country, based on IP.
// Also allows redirect based on country code.
// 
// Requires...
// dit.js
// 
dit.geolocation = (new function () {
  var GEOLOCATION = this;
  var SUPPORTED_COUNTRIES = ['US', 'CN', 'DE', 'IN'];
  var LOCATIONS_REDIRECTED_AS_UK = ['GB', 'IE'];
  var GEO_LOCATION_UPDATE_EVENT = "geoLocationUpdated";
  
  this.GEO_LOCATION_UPDATE_EVENT = GEO_LOCATION_UPDATE_EVENT;
  this.countryCode = "int";

  /* Fetches the users country code (based on IP) and triggers a document event
   * to allow listeners to take action with updated value in place.
   * Default value is 'int' for international (ie. no country set).
   * Supported countries list is taken from existing code but does not have
   * the full range of countries shown in Language Selector component list.
   **/  
  this.fetchCountryCode = function() {
    var hasCallback = arguments.length && typeof(callback) == "function" ? true: false;
    $.ajax({
      url: "//freegeoip.net/json/",
      async: false,
      success: function(data) {
        var country = "int";
        if ($.inArray(data.country_code, LOCATIONS_REDIRECTED_AS_UK) != "-1") {
          country = "uk";
        }
        else {
          if ($.inArray(countryCode, SUPPORTED_COUNTRIES) != '-1') {
            country = country_code.toLowerCase();
          }
        }
        
        // update available value and trigger event for listeners
        GEOLOCATION.countryCode = country;
        $(document).trigger(GEO_LOCATION_UPDATE_EVENT);
      }
    });
  }
  
  /* Redirect to specified URL with a root prefix of countryCode.
   * (e.g. redirect to /<countryCode>/href/goes/here)
   * @href (String) Page location to put after root /<country>/ prefix.
   **/
  this.redirectToCountryUrl = function(href) {
    location.href = "/" + this.countryCode + href;
  }
  
});


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


/* Class: Modal
 * -------------------------
 * Create an area to use as popup/modal/lightbox effect. 
 * 
 * REQUIRES:
 * jquery
 * dit.js
 * dit.responsive.js
 *
 **/
(function($, utils, classes) {
  
  var ARIA_EXPANDED = "aria-expanded";
  var CSS_CLASS_CLOSE_BUTTON = "close";
  var CSS_CLASS_CONTAINER = "Modal-Container"
  var CSS_CLASS_CONTENT = "content";
  var CSS_CLASS_OPEN = "open";
  var CSS_CLASS_OVERLAY = "Modal-Overlay";

  /* Constructor
   * @options (Object) Allow some configurations
   **/
  classes.Modal = Modal;
  function Modal($container, options) {
    var modal = this;
    var config = $.extend({
      $activators: $(), // (optional) Element(s) to control the Modal
      closeOnBuild: true, // Whether intial Modal view is open or closed
      overlay: true  // Whether it has an overlay or not
    }, options || {});

    // If no arguments, likely just being inherited
    if (arguments.length) {
      // Create the required elements
      if(config.overlay) {
        this.$overlay = Modal.createOverlay();
        Modal.bindResponsiveOverlaySizeListener.call(this);
      }
    
      this.$closeButton = Modal.createCloseButton();
      this.$content = Modal.createContent();
      this.$container = Modal.enhanceModalContainer($container);
    
      // Add elements to DOM
      Modal.appendElements.call(this, config.overlay);
    
      // Add events
      Modal.bindCloseEvents.call(this);
      Modal.bindActivators.call(this, config.$activators);
    
      // Initial state
      if (config.closeOnBuild) {
        this.close();
      }
      else {
        this.open();
      }
    }
  }
  
  Modal.createOverlay = function() {
    var $overlay = $(document.createElement("div"));
    $overlay.addClass(CSS_CLASS_OVERLAY);
    return $overlay;
  }

  Modal.createCloseButton = function() {
    var $button = $(document.createElement("button"));
    $button.text("Close");
    $button.addClass(CSS_CLASS_CLOSE_BUTTON);
    return $button;
  }
  
  Modal.createContent = function() {
    var $content = $(document.createElement("div"));
    $content.addClass(CSS_CLASS_CONTENT);
    return $content;
  }

  Modal.enhanceModalContainer = function($container) {
    $container.addClass(CSS_CLASS_CONTAINER);
    return $container;
  }
  
  Modal.appendElements = function(overlay) {
    this.$container.append(this.$closeButton);
    this.$container.append(this.$content);
    
    if (overlay) {
      $(document.body).append(this.$overlay);
    }
    $(document.body).append(this.$container);
  }
  
  Modal.bindCloseEvents = function() {
    var self = this;
    self.$closeButton.on("click", function(e) {
      e.preventDefault();
      self.close();
    });
    
    if (self.$overlay && self.$overlay.length) {
      self.$overlay.on("click", function() {
        self.close();
      });
    }
  }
  
  Modal.bindActivators = function($activators) {
    // Prevent Defaults are after action to stop high-jacking tab too early.
    var self = this;
    $activators.on("click", function(e) {
      switch(e.which) {
        case 1: 
          self.open(false);
          e.preventDefault();
          break;
        case 13: 
          self.open(true);
          e.preventDefault();
          break;
      }
    });
  }

  Modal.bindResponsiveOverlaySizeListener = function() {
    var self = this;
    // Resets the overlay height (once) on scroll because document
    // height changes with responsive resizing and the browser
    // needs a delay to redraw elements. Alternative was to have
    // a rubbish setTimeout with arbitrary delay. 
    $(document.body).on(dit.responsive.reset, function(e, mode) {
      $(window).off("scroll.ModalOverlayResizer");
      $(window).one("scroll.ModalOverlayResizer", function() {
        Modal.setOverlayHeight(self.$overlay);
      });
    });
  }
  
  Modal.setOverlayHeight = function($overlay) {
    $overlay.get(0).style.height = ""; // Clear it first
    $overlay.height($(document).height());
  }
  
  Modal.prototype = {};
  Modal.prototype.close = function() {
    var self = this;
    self.$container.fadeOut(50, function () {
      self.$container.attr(ARIA_EXPANDED, false);
      self.$container.removeClass(CSS_CLASS_OPEN);
    });
    
    if (self.$overlay && self.$overlay.length) {
      self.$overlay.fadeOut(150);
    }
  }
  
  Modal.prototype.open = function(addFocus) {
    var self = this;
    self.$container.css("top", window.scrollY + "px");
    self.$container.addClass(CSS_CLASS_OPEN);
    self.$container.fadeIn(250, function () {
      self.$container.attr(ARIA_EXPANDED, true);
    });
    
    if(arguments.length > 0 && addFocus) {
      self.focus(); 
    }

    if (self.$overlay && self.$overlay.length) {
      Modal.setOverlayHeight(self.$overlay);
      self.$overlay.fadeIn(0);
    }
  }
  
  Modal.prototype.setContent = function(content) {
    var self = this;
    self.$content.empty();
    self.$content.append(content);
  }

  // Tries to add focus to the first found element allowed nwith atural focus ability.
  Modal.prototype.focus = function() {
    var self = this;
    self.$content.find("a, button, input, select").eq(0).focus();
  }
  
  
})(jQuery, dit.utils, dit.classes);


/* Class: Select Tracker
 * ---------------------
 * Adds a label element to mirror the matched selected option
 * text of a <select> input, for enhanced display purpose.
 *
 * REQUIRES:
 * jquery
 * dit.js
 * dit.classes.js
 *
 **/
(function($, classes) {
  
  /* Constructor
   * @$select (jQuery node) Target input element
   **/
  classes.SelectTracker = SelectTracker;
  function SelectTracker($select) {
    var SELECT_TRACKER = this;
    var button, code, lang;
    
    if(arguments.length && $select.length) {
      this.$node = $(document.createElement("p"));
      this.$node.attr("aria-hidden", "true");
      this.$node.addClass("SelectTracker");
      this.$select = $select;
      this.$select.addClass("SelectTracker-Select");
      this.$select.after(this.$node);
      this.$select.on("change.SelectTracker", function() {
        SELECT_TRACKER.update();
      });
      
      // Initial value
      this.update();
    }
  }
  SelectTracker.prototype = {};
  SelectTracker.prototype.update = function() {
    this.$node.text(this.$select.find(":selected").text());
  }
  
})(jQuery, dit.classes);


// Language Selector Component Functionality.
//
// Requires...
// dit.js
// dit.utils.js
// dit.class.modal.js

// Usage
// --------------------------------------------------------------------
// To find all Language Selector components and enhance using 
// the default settings.
//
// dit.components.languageSelector.init()  
//
// For greater control, use either of the individual enhance functions
// for Language Selector Control or Language Selector Dialog components.
// This also allow passing options to customise the output.
// 
// dit.components.languageSelector.enhanceControl()
// dit.components.languageSelector.enhanceDialog()
//
dit.components.languageSelector = (new function() {

  var SelectTracker = dit.classes.SelectTracker;

  /* Extends SelectTracker to meet additional display requirement
   * @$select (jQuery node) Target input element
   * @options (Object) Configurable options
   **/
  function LanguageSelectorControl($select, options) {
    SelectTracker.call(this, $select);
    if(this.$node) {
      this.$node.addClass("SelectTraker-Tracker");
      $select.parents("form").addClass("enhancedLanguageSelector");
      $select.on("change", function() {
        this.form.submit();
      })
    }
  }
  LanguageSelectorControl.prototype = new SelectTracker;
  LanguageSelectorControl.prototype.update = function() {
    var $code = $(document.createElement("span"));
    var $lang = $(document.createElement("span"));
    SelectTracker.prototype.update.call(this);
    $lang.addClass("lang");
    $code.addClass("code");
    $lang.text(this.$node.text());
    $code.text(this.$select.val());
    this.$node.empty();
    this.$node.append($code);
    this.$node.append($lang);
  }

  /* Contructor
   * Displays control and dialog enhancement for language-selector-dialog element.
   * @$dialog (jQuery node) Element displaying list of selective links
   * @options (Object) Configurable options
   **/
  function LanguageSelectorDialog($dialog, options) {
    var LANGUAGE_SELECTOR_DISPLAY = this;
    var id = dit.utils.generateUniqueStr("LanguageSelectorDialog_");
    dit.classes.Modal.call(LANGUAGE_SELECTOR_DISPLAY, $dialog);
    this.$container.attr("id", id);
    this.config = $.extend({
      $controlContainer: $dialog.parent() // Where to append the generated control
    }, options);


    if(arguments.length > 0 && $dialog.length) {
      this.$dialog = $dialog;
      this.$dialog.addClass("LanguageSelectorDialog-Modal");
      
      this.$control = LanguageSelectorDialog.createControl($dialog, id);
      this.config.$controlContainer.append(this.$control);
      this.setContent(this.$dialog.children());

      this.$control.on("click.LanguageSelectorDialog, keydown.LanguageSelectorDialog", function(e) {
        switch(e.which) {
          case 1: 
            LANGUAGE_SELECTOR_DISPLAY.open(false);
            e.preventDefault();
            break;
          case 13: 
            LANGUAGE_SELECTOR_DISPLAY.open(true);
            e.preventDefault();
            break;
        }
      });
    }
  }
  
  LanguageSelectorDialog.createControl = function($node, id) {
    var $control = $(document.createElement("a"));
    var $lang = $(document.createElement("span"));
    var $country = $(document.createElement("span"));
    $lang.addClass("lang");
    $lang.text($node.attr("data-lang"));
    $country.addClass("label");
    $country.text($node.attr("data-label"));
    $control.append($lang);
    $control.append($country);
    $control.addClass("LanguageSelectorDialog-Tracker");
    $control.attr("href", ("#" + id));
    $control.attr("aria-controls", id);
    return $control;
  }
  
  LanguageSelectorDialog.prototype = new dit.classes.Modal
  
  
  // Just finds all available Language Selector components
  // and enhances using the any default settings. 
  this.init = function() {
    $("[data-component='language-selector-control'] select").each(function() {
      new LanguageSelectorControl($(this));
    });

    $("[data-component='language-selector-dialog']").each(function() {
      new LanguageSelectorDialog($(this));
    });
  }
  
  // Selective enhancement for individual Language Selector Control views
  // Allows passing of custom options. 
  // @$control (jQuery object) Something like this: $("[data-component='language-selector-control'] select")
  // @options (Object) Configurable options for class used.
  this.enhanceControl = function($control, options) {
    if ($control.length) {
      new LanguageSelectorControl($control, options);
    }
    else {
      console.error("Language Selector Control missing or not passed")
    }
  }
  
  // Selective enhancement for individual Language Selector Dialog views
  // Allows passing of custom options. 
  // @$control (jQuery object) Something like this: $("[data-component='language-selector-dialog']")
  // @options (Object) Configurable options for class used.
  this.enhanceDialog = function($dialog , options) {
    if ($dialog.length) {
      new LanguageSelectorDialog($dialog, options);
    }
    else {
      console.error("Language Selector Dialog missing or not passed");
    }
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
      $controlContainer: $("#header-bar .container")
    });
  }

});

$(document).ready(function() {
  dit.pages.international.init();
});


/* DO NOT WAIT FOR $(document).ready()
 * THIS SHOULD FIRE BEFORE <body> tag creation
 * Attempts to redirect user based on detected country
 * only if the location is site root (www.great.gov.uk/)
 **/
var root = location.protocol + "//" + location.host + "/";
if (location.href == root) {
  $(document).on(dit.geolocation.GEO_LOCATION_UPDATE_EVENT, function() { 
    dit.geolocation.redirectToCountryUrl("/"); 
  });
  dit.geolocation.fetchCountryCode();
}
