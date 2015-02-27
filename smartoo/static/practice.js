// --------------------------------------------------------------------------
// Servicies
// --------------------------------------------------------------------------

smartooApp.service('smartooService', ['$http', function ($http) {

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
    // TODO: and send back information about done exercise
    this.nextExercise = function() {
        return $http.post('/interface/next-exercise')
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };

    // TODO: more  functions
}]);


// --------------------------------------------------------------------------
//  Controllers
// --------------------------------------------------------------------------
smartooApp.controller('practiceController',
    ['$scope', '$location', '$http', 'smartooService',
            function($scope, $location, $http, smartooService) {

        function startSession(topic) {
            smartooService.startSession(topic).then(function(response) {
                if (response.success) {
                    buildKnowledge();

                } else {
                    errorState(response.message);
                }
            });
        }

        function buildKnowledge() {
            $scope.infoMessage = "Building knowledge..."
            smartooService.buildKnowledge().then(function(response) {
                if (response.success) {
                    createExercises();
                } else {
                    errorState(response.message);
                }
            });
        }

        function createExercises() {
            $scope.infoMessage = "Creating exercises..."
            smartooService.createExercises().then(function(response) {
                if (response.success) {
                    // retrieve first exercise
                    nextExercise();
                } else {
                    errorState(response.message);
                }
            });
        }

        // TODO: posilat zpetnou vazbu
        function nextExercise() {
            smartooService.nextExercise().then(function(response) {
                if (response.success) {
                    $scope.state = "exercise";
                    console.log(response.exercise);
                } else {
                    errorState(response.message);
                }
            });
        }

        function errorState(message) {
            $scope.errorMessage = message;
            $scope.state = "error";
        }

        // initial state is "waiting"
        $scope.errorMessage = null;
        $scope.infoMessage = "";
        $scope.state = "waiting";

        var topic = parseTopic(window.location.pathname);
        startSession(topic);

}]);




// TODO: call after each new card display
fullHeightWorkingArea()

// ===========================================================================
//  Helper functions
// ===========================================================================

// sets minimum height of the working area to tu full page height (minus footer
// height and margins)
function fullHeightWorkingArea() {
    var footerTop = $("#footer").offset().top;
    var margin = parseInt($("#working-area").css("marginTop"));
    var fullHeight = footerTop - 2 * margin;

    //$("#working-area").height(footerTop - 2 * margin);
    $("#working-area").css("min-height", fullHeight);
}



// returns response object (makes shure success and message attributes are set)
function createFailResponse(response) {
    var data = response.data;
    console.log(data);

    if (typeof(data) == "string") {
        fail_response = {
            'success': false,
            'message': 'Server error',
            'data': data
        };

        return fail_response;
    }

    // make sure success is false
    data.success = false;

    // if there is no error message in the response, use "Server error")
    if (!data.message) {
        data.message = "Server error";
    }
    return data;
}

// returns topic for given path or null if the topic is invalid
function parseTopic(path) {
    var match = /^\/practice\/([^/]+)/.exec(path);
    if (match && match.length == 2) {
        topic = match[1];
        return topic;
    } else {
        return null;
    }
}
