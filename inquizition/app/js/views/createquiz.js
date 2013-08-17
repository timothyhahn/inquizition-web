var app = app || {};
(function(){
    app.CreateQuizView = Backbone.View.extend({
        el: $('#quizCreateModal'),
        events: {
            'click .change': 'change',
            'click .create': 'create',
            'keypress input#quizName': 'handleEnter'
        },
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#quiz-create-modal-template').html());

        },
        render: function() {
            var renderedContent = this.template({quizName: this.quizName, seconds: this.seconds});
            $modal = $('div#quizCreateModal');
            $modal.html(renderedContent);
        },
        getName: function() {
            $.get('/name', function(data) {
                app.createQuizView.quizName = data;
                }).done(function() {
                   app.createQuizView.render();
               });
        },
        change: function(ev) {
            this.seconds = $(ev.target).data('id');
            this.render();
        },
        create: function() {
            // Sends POST to create quiz
            this.quizName = $('input#quizName').val();
            $('#createQuizButton').addClass('disabled');
            $.post('/quiz/create', { quiz_name: this.quizName, user_id: app.loginView.user_id, seconds: this.seconds},function(data) {
                $('#quizCreateModal').foundation('reveal', 'close');
                $('img#quizLoader').show();
                app.list.fetch().complete(function() {
                    app.listView.render();
                    $('img#quizLoader').hide();
                });
                $('#createQuizButton').removeClass('disabled');
                $('#quizCreateModal').foundation('reveal', 'close');
                $('#quizCreateModal').empty();
            });
        },
        show: function() {
            this.quizName = '';
            this.seconds = 30;
            this.getName();
            this.render();

            $("#quizCreateModal").foundation('reveal', 'open');
        },
        handleEnter: function(ev) {
            if (ev.which === ENTER_KEY) {
                this.create();
            }
        },
    });
})();