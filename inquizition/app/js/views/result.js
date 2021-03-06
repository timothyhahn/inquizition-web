var app = app || {};
(function(){
    app.ResultView = Backbone.View.extend({
        tagName: 'tr',
        className: 'result',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#quiz-result-template').html());
        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        },
    });


    app.ResultsView = Backbone.View.extend({
        tagName: 'section',
        className: 'results',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#quiz-results-template').html());
            this.collection.bind('reset', this.render);
        },
        render: function() {
            var $results,
                collection = this.collection;
            $(this.el).html(this.template({}));
            $results = this.$('.results');
            collection.each(function(result) {
                var view = new app.ResultView({
                    model: result
                });
                $results.append(view.render().el);
            });

            return this;
        },
    });


    app.UserResultView = Backbone.View.extend({
        tagName: 'tr',
        className: 'result',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#user-result-template').html());
        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        },
    });


    app.UserResultsView = Backbone.View.extend({
        tagName: 'section',
        className: 'results',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#user-results-template').html());
            this.collection.bind('reset', this.render);
        },
        render: function() {
            var $results,
                collection = this.collection;
            $(this.el).html(this.template({}));
            $results = this.$('.results');
            collection.each(function(result) {
                var view = new app.UserResultView({
                    model: result
                });
                $results.append(view.render().el);
            });

            return this;
        },
    });
})();