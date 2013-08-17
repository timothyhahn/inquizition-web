var app = app || {};
(function(){
    var LoginView = Backbone.View.extend({
        el: $('#loginModal'),
        events: {
            'click .loginUser': 'loginModal',
            'keypress input#username': 'handleEnter',
        },
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#login-modal-template').html());
            this.user_id = this.readCookie('user_id');
            this.username = this.readCookie('username');
            if(this.username != null)
                $('a#userName').html(this.username);
            this.render();
        },
        render: function(){
            var renderedContent = this.template();
            $modal = $('div#loginModal');
            $modal.html(renderedContent);
        },
        loginUser: function(username) {
            $.post('/login', {
                username: username
            }).done(function(data){
                app.loginView.user_id = data.id;
                app.loginView.username = data.name;
                $('#loginModal').foundation('reveal', 'close');
                app.loginView.createCookie('user_id', data.id, 7);
                app.loginView.createCookie('username', data.name, 7);
                $('a#userName').html(data.name);
            });
        },
        loginModal: function(ev){
            this.loginUser($('input#username').val());
        },
        createCookie: function(name,value,days) {
            if (days) {
                var date = new Date();
                date.setTime(date.getTime()+(days*24*60*60*1000));
                var expires = "; expires="+date.toGMTString();
            }
            else var expires = "";
            document.cookie = name+"="+value+expires+"; path=/";
        },


        readCookie: function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        },

        eraseCookie: function(name) {
            this.createCookie(name,"",-1);
        },

        handleEnter: function(ev) {
            if (ev.which === ENTER_KEY) {
                this.loginModal();
            }
        },

        logoutUser: function(){
            this.eraseCookie('user_id');
            this.eraseCookie('username');
            this.user_id = undefined;
            this.username = undefined;
            $('a#userName').html('User');
            this.validateUser();
        },

        validateUser: function() {
            // Login User
            if(this.readCookie('username') !== null){
                this.username = this.readCookie('username');
                this.loginUser(this.username);
            } else {
                $('#loginModal').foundation('reveal', 'open');
            }
        },


    });
    
    app.loginView = new LoginView({

    });
})();