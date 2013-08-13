(function($) {
    window.QuizInfo = Backbone.Model.extend({
        updateSeconds: function() {
            var secondsLeft = parseInt(this.get('secondsLeft'));
            secondsLeft = secondsLeft - 1;
            this.set({'secondsLeft': secondsLeft});
        },
    });

    window.Result = Backbone.Model.extend({

    });

    window.Results = Backbone.Collection.extend({
        model: Result,
        parse: function(response){
            return response.results;
        },
        initialize: function(id){
            this.url = '/quiz/results/'+id;
            this.id = id;
        },
    });

    window.UserResults = Backbone.Collection.extend({
        model: Result,
        parse: function(response){
            return response.results;
        },
        initialize: function(id){
            this.url = '/user/'+id;
        }
    });

    window.ResultView = Backbone.View.extend({
        tagName: 'tr',
        className: 'result',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#result-template').html());
        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        },
    });


    window.ResultsView = Backbone.View.extend({
        tagName: 'section',
        className: 'results',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#results-template').html());
            this.collection.bind('reset', this.render);
        },
        render: function() {
            var $results,
                collection = this.collection;
            $(this.el).html(this.template({}));
            $results = this.$('.results');
            collection.each(function(result) {
                var view = new ResultView({
                    model: result
                });
                $results.append(view.render().el);
            });

            return this;
        },
    });


    window.Question = Backbone.Model.extend({
        idAttribute:"id",
    });

    window.Questions = Backbone.Collection.extend({
        model: Question,
        parse: function(response){
            return response.questions;
        },
        initialize: function(id){
            this.url = '/quiz/' + id;
            this.id = id;
            this.currentIndex = 0;
        },
        getCurrent: function() {
            window.question_id = this.models[this.currentIndex].get('id');
            return this.models[this.currentIndex];
        },
        next: function() {
            this.currentIndex++;
            percentage = (this.currentIndex * 10) + '%';
            $('span.meter#questionProgress').css('width', percentage);
            if(this.currentIndex < this.models.length){
                window.question_id = this.models[this.currentIndex].get('id');
            } else {
                App.navigate('results?' + this.id, true);
            }
            return this;
        },
    });

    window.QuestionView = Backbone.View.extend({
        tagName: 'div',
        className: 'question',
        events: {
            'click .answer': 'answer'
        },
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#question-template').html());
            this.model.bind('change',this.render);

        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).addClass('row wrap together');
            $(this.el).attr('id', 'question_' + this.model.get('id'));
            $(this.el).attr('style', 'display: none');
            $(this.el).html(renderedContent);
            return this;
        },
        answer: function(ev) {
            var answer = $(ev.target).data('id');
            $.post('/quiz/answer/' + window.quiz_id, { user_id: window.user_id, question_id: window.question_id, answer: answer},function(data){

                $result = $('div#result');

                $result.hide();
                console.log(data);
                if(data['correct'] == "True"){
                    $result.addClass('success');
                    $result.removeClass('alert');
                    $result.html('Correct!');
                } else {
                    $result.addClass('alert');
                    $result.removeClass('success');
                    $result.html('Incorrect! The answer was: ' + data['text']);
                }
                $result.slideDown();
                $('h5#points').html(data['score']);
            });

            questionsView.proceedNext();
            questionsView.showCurrent();
        }
    });


    window.QuestionsView = Backbone.View.extend({
        tagName: 'section',
        className: 'questions',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#questions-template').html());
            this.collection.bind('reset', this.render);
        },
        render: function() {
            var $quiz,
                collection = this.collection;
                        $(this.el).html(this.template({}));
            $quiz = this.$('.questions');
            collection.each(function(quiz) {
                if(quiz.get('text') != undefined){
                    var view = new QuestionView({
                        model: quiz
                    });
                    $quiz.append(view.render().el);
                }
            });

            return this;
        },
        showCurrent:function() {
            var collection = this.collection;
            var id = collection.getCurrent().get('id');
            select = '.question#question_' + id
            $(select).slideDown();
        },
        proceedNext:function() {
            var collection = this.collection;
            select = '.question#question_' + window.question_id
            $(select).slideUp();
            collection.next();
        },

    });

    window.QuizInfos = Backbone.Collection.extend({
        model: QuizInfo,
        url: '/quiz',
        parse: function(response) {
            return response.quizzes;
        }
    });

    window.QuizInfoView = Backbone.View.extend({
        tagName: 'section',
        className: 'quizInfo',
        events: {
            'click .join': 'join'
        },

        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('change',this.render);
            this.template = _.template($('#quiz-template').html());
        },

        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        },

        join: function(ev) {
            var quizID = $(ev.target).data('id');
            $.post('/quiz/join/' + quizID, {user_id: window.user_id});
            App.navigate('countdown?' + quizID,  true);

        },
    });

    window.list = new QuizInfos();

    window.ListQuizInfoView = QuizInfoView.extend({
        
    });

    window.ListView = Backbone.View.extend({
        tagName: 'section',
        className: 'list',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#list-template').html());
            this.collection.bind('reset', this.render);
        },

        render: function() {
            var $quizInfo,
                collection = this.collection;
            
            $(this.el).html(this.template({}));
            $quizInfo = this.$('.quizInfo');
            collection.each(function(quizInfo) {
                var view = new ListQuizInfoView({
                    model: quizInfo,
                    collection: collection
                });
                $quizInfo.append(view.render().el);
            });

            return this;
        }
    });

    window.CountDownView = Backbone.View.extend({
        tagName: 'section',
        className: 'countdown',
        initialize: function(options) {
            _.bindAll(this, 'render');
            this.template = _.template($('#countdown-template').html());

            window.secondsLeft = options.secondsLeft;

            window.decisecondsLeft = window.secondsLeft * 10;
            window.countDownInterval = window.setInterval(function() {
                if(decisecondsLeft > 11) { 
                        decisecondsLeft--;
                        deciTotal = window.seconds * 10;
                        decisecondsTaken = deciTotal - decisecondsLeft;
                        factor = window.seconds / 10;
                        percentage = decisecondsTaken / factor + '%';
                        $('span.meter#waitProgress').css('width', percentage);
                } else {
                    App.navigate('play?' + options.quiz_id,  true);
                }
            }, 100);

            window.countDownUpdateInterval = window.setInterval(function() {
                $.get('/quiz/seconds/' + options.quiz_id, function(data) {
                    this.secondsLeft = data;
                    }).done(function() {
                        if(this.secondsLeft < window.seconds)
                            window.decisecondsLeft = this.secondsLeft * 10;
                });
            }, 5000);
            this.updateJoiners();
            window.countDownJoinInterval = window.setInterval(function(){
                window.countDownView.updateJoiners();
            }, 2500);

        },
        updateJoiners: function(){
            var options = this.options;
             $.get('/quiz/joiners/' + options.quiz_id, function(data){
                    for (var i = 0; i < data.joiners.length; i++){
                        if($.inArray(data.joiners[i].id,options.quizJoiners) == -1){
                            options.quizJoiners.push(data.joiners[i].id);
                            var box = '<div data-alert class="alert-box secondary" style="display: none" id="joiner">' + data.joiners[i].name +' Joined</div>'
                            $('div#join').append(box);
                            $('div#joiner').slideDown();
                        } 
                    }
                });
        },

        render: function() {
            $(this.el).html(this.template({}));
            $countdown = this.$('.countdown');

            return this;
        }
    });

    window.Inquizition = Backbone.Router.extend({
        initialize: function() {
            window.seconds = 30;
            this.listView = new ListView({
                collection: window.list
            });
        },
        routes: {
            '': 'home',
            'countdown?:quizID': 'countdown',
            'play?:quizID': 'play',
            'results?:quizID': 'results',
            'user': 'userResults',
        },
        home: function() {

            validateUser();
            window.list.fetch();


            var $result = $('div#result');
            $result.hide();
            // Count down every 1 second
            window.listCountInterval = window.setInterval(function() {
              window.list.each(function(quiz, index) {quiz.updateSeconds()});
            }, 1000);

            // Update every 5 seconds
            window.listUpdateInterval = window.setInterval(function() {
              window.list.fetch({update: true});
              },5000);

            window.clearInterval(window.resultsInterval);

            var $container = $('#container');
            $container.empty();
            $container.append(this.listView.render().el);
        },
        countdown: function(quizID) {
            var $container = $('#container');
            $container.empty();

            var $result = $('div#result');
            $result.hide();
            window.clearInterval(window.listCountInterval);
            window.clearInterval(window.listUpdateInterval);

            window.list.fetch();
            var quiz = window.list.get(quizID);
            if(quiz == undefined) {
                App.navigate('', true)
            } else {

                window.countDownView = new CountDownView({
                    secondsLeft: quiz.get('secondsLeft'),
                    quiz_id: quizID,
                    quizJoiners: new Array(),
                 });

                $container.append(window.countDownView.render().el);
                $('div#countdown').slideDown();
            }
        },
        play: function(quizID) {
            var $container = $('#container');
            $container.empty();


            var $result = $('div#result');
            $result.hide();
            window.clearInterval(window.countDownUpdateInterval);
            window.clearInterval(window.countDownInterval);
            this.questions = new Questions(quizID);
            window.questionsView = new QuestionsView({collection:this.questions});
            window.quiz_id = quizID;

            $container.append(questionsView.render().el);

            this.questions.fetch().complete(function() {
                questionsView.showCurrent();
            });

        },
        results: function(quizID) {
            var $container = $('#container');
            $container.empty();
            
            $result = $('div#result');
            window.results = new Results(quizID);

            window.results.fetch().complete(function() {

            $result.hide();

            window.resultsView = new ResultsView({collection: window.results});
            window.quiz_id = quizID;
            $container.append(resultsView.render().el);
            window.resultsInterval = window.setInterval(function() {
                window.results.fetch();
            }, 5000);

            });

        },
        userResults: function(){
            var $container = $('#container');
            $container.empty();
             $result = $('div#result');
                 window.clearInterval(window.listCountInterval);
            window.clearInterval(window.listUpdateInterval);
            window.userResults = new UserResults(window.user_id);


            window.userResults.fetch().complete(function() {
                $result.hide();
                window.userResultsView = new ResultsView({collection: window.userResults});
                $container.append(userResultsView.render().el);
         });
        },
    });

    $(function() {
        window.App = new Inquizition();
        Backbone.history.start();
    });

})(jQuery)
