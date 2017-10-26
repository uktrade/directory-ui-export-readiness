var GOVUK = {};

GOVUK.components = (new function() {
  this.ArticlePaginator = ArticlePaginator;
  this.hiddenClass = 'hidden'; // expect css file to define this class
  this.pageSize = 5
  function ArticlePaginator(listElement, loadMoreButton) {
    var liElements = listElement.getElementsByTagName("li");
    for (var i=GOVUK.components.pageSize; i < liElements.length; i++ ) {
      liElements[i].className = GOVUK.components.hiddenClass;
    }
    loadMoreButton.addEventListener('click', function() {
      var hiddenLiElements = listElement.getElementsByClassName(GOVUK.components.hiddenClass);
      var length = Math.min(hiddenLiElements.length, GOVUK.components.pageSize)
      for (var i=0; i < length; i++ ) {
        hiddenLiElements[0].className = '';
      }
      if (hiddenLiElements.length === 0) {
        loadMoreButton.className = GOVUK.components.hiddenClass;
      }
    })
  }
});
