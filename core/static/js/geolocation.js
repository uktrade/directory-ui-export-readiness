var dit = window.dit || {};

dit.geolocationRedirection = (new function() {
  this.init = function() {
    $.getJSON("//freegeoip.net/json/").done(function(data) {
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
    });
  }
});

dit.geolocationRedirection.init();
