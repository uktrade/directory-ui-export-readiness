var GOVUK = {};

GOVUK.components = (new function() {
  this.Feedback = Feedback;

  function Feedback(
    positiveELement, negativeELement, containerQuestion, containerOutcome
  ) {
    function send_feedback(feedback) {
      if (window.ga) {
        window.ga('set', 'page', window.location.pathname + '/' + feedback);
        window.ga('send', 'pageview');
      }
      containerQuestion.style.display = 'none';
      containerOutcome.style.display = 'block';
    }
    positiveELement.addEventListener('click', function() {
      send_feedback('was-useful');
    });

    negativeELement.addEventListener('click', function() {
      send_feedback('was-not-useful');
    });
  }
});
