var app = app || {};
(function () {
  app.CountDownView = Backbone.View.extend({
    tagName: 'section',
    className: 'countdown',
    initialize: function (options) {
      _.bindAll(this, 'render');
      this.template = _.template($('#countdown-template').html());
      
      app.seconds = options.secondsLeft;
      app.decisecondsLeft = options.secondsLeft * 10;
      app.countDownInterval = window.setInterval(function () {
        if(app.decisecondsLeft > 5 || app.decisecondsLeft > 1000) {
          app.decisecondsLeft--;
          deciTotal = app.seconds * 10;
          decisecondsTaken = deciTotal - app.decisecondsLeft;
          factor = app.seconds / 10;
          percentage = decisecondsTaken / factor + '%';
          $('span.meter#waitProgress').css('width', percentage);
        } else {
          app.inquizition.navigate('play?' + options.quiz_id,  true);
        }
      }, 100);

      app.countDownUpdateInterval = window.setInterval(function () {
        $.get('/quiz/seconds/' + options.quiz_id, function (data) {
          this.secondsLeft = data;
        }).done(function () {
          if(this.secondsLeft < app.seconds)
            app.decisecondsLeft = this.secondsLeft * 10;
          });
      }, 5000);
 
      this.updateJoiners();
      app.countDownJoinInterval = window.setInterval(function () {
          app.countDownView.updateJoiners();
      }, 2500);
    },
    
    updateJoiners: function () {
        var options = this.options;
        $.get('/quiz/joiners/' + options.quiz_id, function (data) {
          for (var i = 0; i < data.joiners.length; i++){
            if($.inArray(data.joiners[i].id,options.quizJoiners) == -1){
              options.quizJoiners.push(data.joiners[i].id);
              var box = '<div data-alert class="alert-box secondary" style="display: none" id="joiner">' + data.joiners[i].name +' Joined</div>';
              $('div#join').append(box);
              $('div#joiner').slideDown();
            }
          }
        });
    },
    render: function () {
      $(this.el).html(this.template({}));
      var $countdown = this.$('.countdown');
      return this;
    }
  });

}());