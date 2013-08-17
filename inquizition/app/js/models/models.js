var app = app || {};
(function () {
  // Question Model
  app.Question = Backbone.Model.extend({
    idAttribute: "id"
  });
  // Quiz Info Model
  app.QuizInfo = Backbone.Model.extend({
    updateSeconds: function () {
      var secondsLeft = parseInt(this.get('secondsLeft'), 10);
      secondsLeft = secondsLeft - 1;
      this.set({'secondsLeft': secondsLeft});
    }
  });
  // Results Model
  app.Result = Backbone.Model.extend({

  });

}());