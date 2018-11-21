// Header code
//
// Requires
// jQuery
// dit.js
// dit.components.js
//
dit.prototypePage = (new function () {
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
      $controlContainer: $("#great-header-account-links")
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
  dit.prototypePage.init();
});
