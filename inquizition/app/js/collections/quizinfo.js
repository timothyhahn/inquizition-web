var app = app || {};
(function () {
  // Collection of all the quiz information
  var QuizInfos = Backbone.Collection.extend({
    model: app.QuizInfo,
    url: '/quiz',
    parse: function (response) {
      return response.quizzes;
    }
  });
  app.list = new QuizInfos();
}());