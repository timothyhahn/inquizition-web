var app = app || {};
(function () {
  app.Inquizition = Backbone.Router.extend({
    initialize: function () {
      app.createQuizView = new app.CreateQuizView();
    },
    routes: {
      '': 'home',
      'countdown?:quizID': 'countdown',
      'play?:quizID': 'play',
      'results?:quizID': 'results',
      'user': 'userResults'
    },
    clearAllIntervals: function () {
      window.clearInterval(app.resultsInterval);
      window.clearInterval(app.listCountInterval);
      window.clearInterval(app.listUpdateInterval);
      window.clearInterval(app.countDownUpdateInterval);
      window.clearInterval(app.countDownInterval);
      window.clearInterval(app.countDownJoinInterval);
    },
    home: function () {
      this.clearAllIntervals();
      app.loginView.validateUser();
      app.list.fetch();

      var $result = $('div#result');
      $result.css('visibility', 'hidden');
      // Count down every 1 second
      app.listCountInterval = window.setInterval(function () {
        app.list.each(function (quiz, index) {quiz.updateSeconds(); });
      }, 1000);

      // Update every 2.5 seconds
      app.listUpdateInterval = window.setInterval(function () {
        $('img#quizLoader').show();
        app.list.fetch({update: true}).complete(function () {
          $('img#quizLoader').hide();
        });
      }, 2500);


      var $container = $('#container');
      $container.empty();
      $container.append(app.listView.render().el);
    },
    countdown: function (quizID) {
      this.clearAllIntervals();
      var $container = $('#container');
      $container.empty();

      var $result = $('div#result');
      $result.hide();

      app.list.fetch();
      var quiz = app.list.get(quizID);
      if (quiz === undefined) {
        app.inquizition.navigate('', true);
      } else {
        app.countDownView = new app.CountDownView({
          secondsLeft: quiz.get('secondsLeft'),
          quiz_id: quizID,
          quizJoiners: []
        });
        $container.append(app.countDownView.render().el);
        $('div#countdown').slideDown();
      }
    },
    play: function (quizID) {
      this.clearAllIntervals();
      var $container = $('#container');
      $container.empty();

      var $result = $('div#result');
      $result.hide();
      this.questions = new app.Questions(quizID);
      app.questionsView = new app.QuestionsView({collection: this.questions});
      app.quiz_id = quizID;

      $container.append(app.questionsView.render().el);
      $('img#resultLoader').show();
      this.questions.fetch().complete(function () {
        $('img#resultLoader').hide();
        app.questionsView.showCurrent();
      });
    },
    results: function (quizID) {
      this.clearAllIntervals();
      var $container = $('#container');
      $container.empty();
      var $result = $('div#result');
      app.results = new app.Results(quizID);

      app.results.fetch().complete(function () {
        $result.hide();

        app.resultsView = new app.ResultsView({collection: app.results});
        app.quiz_id = quizID;
        $container.append(app.resultsView.render().el);
        app.resultsInterval = window.setInterval(function () {
          app.results.fetch();
        }, 5000);
      });

    },
    userResults: function () {
      this.clearAllIntervals();
      var $container = $('#container');
      $container.empty();
      var $result = $('div#result');
      app.userResults = new app.UserResults(app.loginView.user_id);
      app.userResults.fetch().complete(function () {
        $result.hide();
        app.userResultsView = new app.ResultsView({collection: app.userResults});
        $container.append(app.userResultsView.render().el);
      });
    }
  });

}());