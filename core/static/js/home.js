// Header code
//
// Requires
// jQuery
// dit.js
// dit.components.js
//
dit.home = (new function () {
  // Page init
  this.init = function() {
    dit.responsive.init({
      "desktop": "min-width: 768px",
      "tablet" : "max-width: 767px",
      "mobile" : "max-width: 480px"
    });

    enhanceLanguageSelector();
    delete this.init; // Run once
  }

  /* Find and enhance any Language Selector Dialog view
   **/
  function enhanceLanguageSelector() {
    var $dialog = $("[data-component='language-selector-dialog']");
    dit.components.languageSelector.enhanceDialog($dialog, {
      $controlContainer: $("#header-bar .account-locale-links")
    });
  }
});

$(document).ready(function() {
  dit.home.init();
  dit.components.video.init();
});
