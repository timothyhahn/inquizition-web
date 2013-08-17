var app = app || {};
(function () {

  // Collection of all the questions
  app.Questions = Backbone.Collection.extend({
    model: app.Question,
    parse: function (response) {
      return response.questions;
    },
    initialize: function (id) {
      this.url = '/quiz/' + id;
      this.id = id;
      this.currentIndex = 0; // Starts at the first question
    },
    // Gets the question id of the model at the current index
    getCurrent: function () {
      app.question_id = this.models[this.currentIndex].get('id');
      return this.models[this.currentIndex];
    },
    // Moves to the next question and progresses the progress bar
    next: function () {
      this.currentIndex++;
      var percentage = (this.currentIndex * 10) + '%';
      $('span.meter#questionProgress').css('width', percentage);
      if (this.currentIndex < this.models.length) { // More questions left
        app.question_id = this.models[this.currentIndex].get('id');
      } else { // Finished
        app.inquizition.navigate('results?' + this.id, true);
      }
      return this;
    }
  });

}());