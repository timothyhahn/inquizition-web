var app = app || {};
(function () {
  // Collection of all the results at the end of a quiz
  app.Results = Backbone.Collection.extend({
    model: app.Result,
    parse: function (response) {
      return response.results;
    },
    initialize: function (id) {
      this.url = '/quiz/results/' + id;
      this.id = id;
    }
  });
  // Collection of all the results for a user
  app.UserResults = Backbone.Collection.extend({
    model: app.Result,
    parse: function (response) {
      return response.results;
    },
    initialize: function (id) {
      this.url = '/user/' + id;
    }
  });
}());