smartooApp.service('smartooService', ['$http', function ($http) {

    // POST request to send feedback message
    this.sendMessage = function(message) {
        return $http.post('/interface/feedback-message', message)
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // POST request to start a new session with given topic
    this.startSession = function(topic) {
        return $http.post('/interface/start-session', {topic: topic})
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // POST request to build knowledge
    this.buildKnowledge = function() {
        return $http.post('/interface/build-knowledge')
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // POST request to create exercises
    this.createExercises = function() {
        return $http.post('/interface/create-exercises')
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // POST request to get new exercise
    // (also sends back information about done exercise)
    this.nextExercise = function(previousExercise) {
        // make sure previousExercise is null, not undefined
        if (!previousExercise) {
            previousExercise = null;
        }
        return $http.post('/interface/next-exercise', {feedback: previousExercise})
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // POST request to provide session feedback
    this.finalFeedback = function(rating) {

        var value = 0.5;

        if (rating == 'good') {
            value = 1.0;
        } else if (rating == 'bad') {
            value = 0.0;
        }

        return $http.post('/interface/session-feedback', {rating: value})
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };
}]);


