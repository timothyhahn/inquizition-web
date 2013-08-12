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

    window.ResultView = Backbone.View.extend({
        tagName: 'li',
        className: 'result',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#result-template').html());
            //this.model.bind('change',this.render);
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
            console.log('currentIndex',this.currentIndex);
            console.log('length', this.models.length);

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
                console.log(data);    
                console.log(data['correct']);

                $result = $('span.result');
                console.log($result);
                $result.addClass('label');
                if(data['correct'] == "True"){
                    $result.addClass('success');
                    $result.removeClass('alert');
                    $result.html('Correct!');
                } else {
                    $result.addClass('alert');
                    $result.removeClass('success');
                    $result.html('Incorrect!');
                }
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
            //$('span.countdown').html(window.secondsLeft);

            
            decisecondsLeft = secondsLeft * 10;
            window.countDownInterval = window.setInterval(function() {
                //console.log(decisecondsLeft);
                if(decisecondsLeft > 1) { 
                        decisecondsLeft--;
                        decisecondsTaken = 600 - decisecondsLeft;
                        percentage = decisecondsTaken / 6 + "%";
                        //console.log(percentage);
                        $('span.meter').css("width", percentage);
                        window.secondsLeft--;
                        window.secondsLeft = parseInt(window.secondsLeft) - 1;
                } else {
                    App.navigate('play?' + options.quiz_id,  true);
                }
                //$('span.countdown').html(window.secondsLeft);
            }, 100);
        },

        render: function() {
            $(this.el).html(this.template({}));
            $countdown = this.$('.countdown');

            return this;
        }
    });

    window.Inquizition = Backbone.Router.extend({
        initialize: function() {
            this.listView = new ListView({
                collection: window.list
            });
        },
        routes: {
            '': 'home',
            'countdown?:quizID': 'countdown',
            'play?:quizID': 'play',
            'results?:quizID': 'results',
        },
        home: function() {
            window.list.fetch();
            var $container = $('#container');
            $container.empty();
            $container.append(this.listView.render().el);
        },
        countdown: function(quizID) {
            var $container = $('#container');
            $container.empty();
            window.clearInterval(window.listCountInterval);
            window.clearInterval(window.listUpdateInterval);

            window.list.fetch();
            var quiz = window.list.get(quizID);
            if(quiz == undefined) {
                App.navigate('', true)
            } else {

                this.countDownView = new CountDownView({
                    secondsLeft: quiz.get('secondsLeft'),
                    quiz_id: quizID

                 });

                $container.append(this.countDownView.render().el);
                $('div#countdown').slideDown();
            }
        },
        play: function(quizID) {
            var $container = $('#container');
            $container.empty();

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
            
            window.results = new Results(quizID);

            window.results.fetch().complete(function() {
            window.resultsView = new ResultsView({collection: window.results});
            window.quiz_id = quizID;
            $container.append(resultsView.render().el);
            window.resultsInterval = window.setInterval(function() {
                window.results.fetch();
            }, 5000);

            });

        },
    });

    $(function() {
        window.App = new Inquizition();
        Backbone.history.start();
    });

})(jQuery)
