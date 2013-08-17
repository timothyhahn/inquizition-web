var app = app || {};
(function(){
    app.QuizInfoView = Backbone.View.extend({
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
            $.post('/quiz/join/' + quizID, {user_id: app.loginView.user_id});
            app.inquizition.navigate('countdown?' + quizID,  true);

        },
    });

    app.ListQuizInfoView = app.QuizInfoView.extend({
        
    });

	var ListView = Backbone.View.extend({
        tagName: 'section',
        className: 'list',
        events: {
            'click .add': 'add',
        },
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#list-template').html());
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.render);
        },

        render: function() {
            var $quizInfo,
                collection = this.collection;
            
            $(this.el).html(this.template({}));
            $quizInfo = this.$('.quizInfo');
            collection.each(function(quizInfo) {
                var view = new app.ListQuizInfoView({
                    model: quizInfo,
                    collection: collection
                });
                $quizInfo.append(view.render().el);
            });

            return this;
        },
        add: function() {
            //console.log('fire');
        },
    });
    app.listView = new ListView({
        collection: app.list
    });
})();