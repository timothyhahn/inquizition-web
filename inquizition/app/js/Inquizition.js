(function($) {
    window.Quiz = Backbone.Model.extend({
    });

    window.Quizzes = Backbone.Collection.extend({
        model: Quiz,
        url: '/quiz',
        parse: function(response) {
            return response.quizzes;
        }
    });

    window.QuizView = Backbone.View.extend({
        tagName: 'li',
        className: 'quiz',
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('change',this.render);
            this.template = _.template($('#quiz-template').html());
        },

        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        }

    });

    window.list = new Quizzes();

    window.ListQuizView = QuizView.extend({
        
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
            var $quizzes,
                collection = this.collection;
            
            $(this.el).html(this.template({}));
            $quizzes = this.$('.quizzes');
            collection.each(function(quiz) {
                var view = new ListQuizView({
                    model: quiz,
                    collection: collection
                });
                $quizzes.append(view.render().el);
            });

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
        },
        home: function() {
            var $container = $('#container');
            $container.empty();
            $container.append(this.listView.render().el);
        },
    });

    $(function() {
        window.App = new Inquizition();
        Backbone.history.start();
    });

})(jQuery);
