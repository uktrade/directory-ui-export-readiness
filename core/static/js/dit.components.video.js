// Video Component Functionality.
// Requires...
// dit.js
// dit.class.Modal.js
 
dit.components.video = (new function() {

  var VIDEO_COMPONENT = this;
  
  // Constants
  var CSS_CLASS_CONTAINER = "video-container";
  var SELECTOR_MODAL_ACTIVATOR = "[data-node='videoactivator']";
  var TYPE_VIDEO = "video";
  var TYPE_IFRAME = "iframe";
  
  // Private
  var _modal;
  
  function createModalContainer() {
    var $container = $(document.createElement("div"));
    $container.addClass(CSS_CLASS_CONTAINER);
    return $container;
  }

  function bindActivators($activators) {
    $activators.on("click", function(e) {
      e.preventDefault();
      VIDEO_COMPONENT.activate(this);
    });
  }
  
  function loadWithVideo(src) {
    var $video = $("<video controls></video>");
    var format = src.replace(/^.*\.([a-z0-9/]+)$/, "$1");
    var $source = $("<source src=\"" + src + "\" type=\"video/" + format  + "\">");
    $video.append($source);
    _modal.setContent($video);
  }
  
  function loadWithIframe(src) {
    var $iframe = $("<iframe src=\"" + src + "\"></iframe>");
    _modal.setContent($iframe);
  }

  function resize() {
    var width = $(window).width();
    var height = $(window).height();
    var $iframe = $("iframe", _modal.$container);
    var sizes = [
      [320, 240],
      [640, 360],
      [853, 480],
      [1280, 720],
      [1920, 1080]
    ];
    
    var i = 0;
    var size;
    
    do {
      size = sizes[i],
      i++;
    } while (i < sizes.length && sizes[i][0] <= width && sizes[i][1] <= height);
    
    $iframe.attr("width", size[0]);
    $iframe.attr("height", size[1]);
    //t = Math.floor((o - s.height()) / 4),
    //t > 0 && i.$content.css('margin-top', String(t > 0 ? t : 0) + 'px')
  }
  

  // Public  
  this.init = function() {
    var $activators = $(SELECTOR_MODAL_ACTIVATOR);
    var $container = createModalContainer();
    if($activators.length) {
      $(document.body).append($container);
      _modal = new dit.classes.Modal($container, {
        $activators: $activators
      });

      bindActivators($activators);
    }
    
    delete self.init; // Run once fuction.
  }

  this.activate = function(element) {
    var $activator = $(element);
    var type = $activator.data("element");
    var url = $activator.attr("href") || $activator.data("src");
    switch(type) {
      case TYPE_VIDEO:
        loadWithVideo(url);
        break;
      case TYPE_IFRAME:
        loadWithIframe(url);
        break;
      default:
        type = null;
    }

    if(type) {
      resize();
      _modal.open();
    }
  }

});
  

$(document).ready(function() {
  dit.components.video.init();
});
