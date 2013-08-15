var app = app || {};
(function () {
  app.Questions = Backbone.Collection.extend({
    model: app.Question,
    parse: function (response) {
      return response.questions;
    },
    initialize: function (id) {
      this.url = '/quiz/' + id;
      this.id = id;
      this.currentIndex = 0;
    },
    getCurrent: function () {
      app.question_id = this.models[this.currentIndex].get('id');
      return this.models[this.currentIndex];
    },
    next: function () {
      this.currentIndex++;
      var percentage = (this.currentIndex * 10) + '%';
      $('span.meter#questionProgress').css('width', percentage);
      if (this.currentIndex < this.models.length) {
        app.question_id = this.models[this.currentIndex].get('id');
      } else {
        app.inquizition.navigate('results?' + this.id, true);
      }
      return this;
    }
  });

}());