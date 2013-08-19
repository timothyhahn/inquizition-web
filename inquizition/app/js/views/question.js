var app = app || {};
(function(){
     var QuestionView = Backbone.View.extend({
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
            $('img#responseLoader').show();
            var answer = $(ev.target).data('id');
            $.post('/quiz/answer/' + app.quiz_id, { user_id: app.loginView.user_id, question_id: app.question_id, answer: answer},function(data){

                $result = $('div#result');

                $result.css('visibility', 'hidden');
                if(data['correct'] == "True"){
                    $result.addClass('success');
                    $result.removeClass('alert');
                    $result.html('Correct!');
                } else {
                    $result.addClass('alert');
                    $result.removeClass('success');
                    $result.html('Incorrect! The answer was: ' + data['text']);
                }
                $result.css('visibility', 'visible');
                $result.fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);
                $('h5#points').html(data['score']);
                $('img#responseLoader').hide();

                app.questionsView.proceedNext();
                app.questionsView.showCurrent();

            });
                app.questionsView.hideCurrent();
        }
    });


    app.QuestionsView = Backbone.View.extend({
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
            $('h5#quizName').html(this.collection.name);
            return this;
        },
        showCurrent:function() {
            var collection = this.collection;
            var id = collection.getCurrent().get('id');
            select = '.question#question_' + id
            $(select).slideDown();
        },
        hideCurrent:function(){
           select = '.question#question_' + app.question_id;
            $(select).slideUp();

        },
        proceedNext:function() {
            var collection = this.collection;
            this.hideCurrent();
            collection.next();
        },

    });

})();