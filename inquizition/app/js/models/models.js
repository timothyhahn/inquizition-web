var app = app || {};
(function () {
  app.Question = Backbone.Model.extend({
    idAttribute: "id"
  });
  app.QuizInfo = Backbone.Model.extend({
    updateSeconds: function () {
      var secondsLeft = parseInt(this.get('secondsLeft'), 10);
      secondsLeft = secondsLeft - 1;
      this.set({'secondsLeft': secondsLeft});
    }
  });

  app.Result = Backbone.Model.extend({

  });

}());