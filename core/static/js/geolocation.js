dit.geolocationRedirection = (new function() {

  var cookieName = 'disable_geoloaction';

  this.init = function() {
    if (this.shouldPreventRedirect()) {
      dit.utils.setCookie(cookieName, true, 365);
    } else {
      $.getJSON("//freegeoip.net/json/").done(this.handleGeolocationRedirection);
    }
  }

  this.handleGeolocationRedirection = function(data) {
    if (data.country_code !== 'GB' && data.country_code !== 'IE') {
      var countryToLanguageMap = {
        CN: 'zh-hans',
        DE: 'de',
        ES: 'es',
        JP: 'ja',
      };
      var language = countryToLanguageMap[data.country_code] || 'en-gb';
      location.assign('/international/?lang=' + language);
    }
  }

  this.shouldPreventRedirect = function() {
    return (
      dit.utils.getCookie(cookieName) === "true" ||
      dit.utils.getQuerystringParameter('lang') === 'en-gb'
    );
  }

});

dit.geolocationRedirection.init();
