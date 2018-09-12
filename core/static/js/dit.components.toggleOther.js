var GOVUK = GOVUK || {}
GOVUK.utils = GOVUK.utils || {};


GOVUK.utils.toggleOtherOnSelect = (function() {
  return function toggleOtherOnClick(inputBox, options) {
    function hide(element) {
      element.style.display = 'none';
    }

    function show(element) {
      element.style.display = 'block';
    }

    function hideInputBox() {
      hide(inputBox.parentElement);
    }

    function showInputBox() {
      show(inputBox.parentElement);
      inputBox.focus();
    }

    function handleSelectboxChange(event) {
      if (event.target.value.toUpperCase() === 'OTHER') {
        showInputBox();
      } else {
        hideInputBox();
        inputBox.value = '';
      }
    }

    if (inputBox.value === '') {
      hideInputBox();
    }
    
    options.addEventListener('change', handleSelectboxChange);
  };
})();
