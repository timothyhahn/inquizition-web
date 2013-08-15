var app = app || {};
(function () {
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