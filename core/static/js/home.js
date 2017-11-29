// Header code
//
// Requires
// jQuery
// dit.js
// dit.components.js
//
dit.header = (new function () {
  // Page init
  this.init = function() {
    dit.responsive.init({
      "desktop": "min-width: 768px",
      "tablet" : "max-width: 767px",
      "mobile" : "max-width: 480px"
    });

    enhanceLanguageSelector();
    delete this.init; // Run once
    dit.components.menu.init();
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
  dit.header.init();
});
