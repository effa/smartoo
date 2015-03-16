// --------------------------------------------------------------------------
// Directives
// --------------------------------------------------------------------------

//smartooApp.directive('unfocus', function($timeout, $document) {
//  return {
//    link: function(scope, element, attrs) {
//      element.bind('click', function() {
//        $timeout(function() {
//          //element.parent().focus();
//            console.log('unfocus');
//            body = $document[0].body;
//            body.focus();
//            console.log($document[0].body);
//        });
//      });
//    }
//  };
//});

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
        if (rating == 'good') {
            var value = 1.0;
        } else if (rating = 'bad') {
            var value = 0.0;
        } else {
            var value = 0.5;
        }

        return $http.post('/interface/session-feedback', {rating: value})
            .then(function(response) {
                return response.data;
            }, function(response) {
                return createFailResponse(response);
            });
    };
}]);


// --------------------------------------------------------------------------
//  Controllers
// --------------------------------------------------------------------------
smartooApp.controller('practiceController',
    ['$scope', '$location', '$http', '$window', '$document', 'smartooService',
            function($scope, $location, $http, $window, $document, smartooService) {

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
                    $scope.nextExercise();
                } else {
                    errorState(response.message);
                }
            });
        }

        // TODO: posilat zpetnou vazbu
        $scope.nextExercise = function(feedback) {
            // unless it's request for the first exercise, mark current
            // exercise as finnished
            if ($scope.exercise) {
                $scope.exercise.finnished = true;
            }

            if (feedback == "irrelevant") {
                $scope.exercise.irrelevant = true;
            } else if (feedback == "invalid") {
                $scope.exercise.invalid = true;
            }

            // if it's not first exercise, also send a feedback for the
            // previous exercise
            smartooService.nextExercise($scope.exercise).then(function(response) {
                if (response.success) {
                    if (response.finnished) {
                        // show final feedback form
                        $scope.state = 'final-feedback';
                    } else {
                        //console.log(response.exercise);
                        $scope.exercise = response.exercise;
                        $scope.exercise.answered = false;
                        $scope.exercise.correct = false;
                        $scope.exercise.invalid = false;
                        $scope.exercise.irrelevant = false;
                        // finnishi = clicked next / invalid / irrelevant
                        $scope.exercise.finnished = false;

                        // modify options (add selected and correct fields)
                        $scope.exercise.options = [];
                        angular.forEach(response.exercise['choices'], function(option) {
                            $scope.exercise.options.push({
                                text: option,
                                selected: false,
                                correct: option == $scope.exercise['correct-answer']
                            });
                        });
                        $scope.state = "exercise";
                    }
                } else {
                    errorState(response.message);
                }
            });
        }


        $scope.finalFeedback = function(rating) {
            smartooService.finalFeedback(rating).then(function(response) {
                if (response.success) {
                    $scope.state = "after-final-feedback";
                } else {
                    errorState(response.message);
                }
            });
        }

        function errorState(message) {
            $scope.errorMessage = message;
            $scope.state = "error";
        }

        $scope.answerSelected = function(option) {
            option.selected = true;
            $scope.exercise.answered = true;
            $scope.exercise.correct = option.correct;
        }

        function resize() {
            fullHeightWorkingArea();
        }

        // initial visual settings
        resize();

        // initial state is "waiting"
        $scope.errorMessage = null;
        $scope.infoMessage = "";
        $scope.state = "waiting";

        // TODO: lepsi by bylo posilat topic jiz v ramci js ze serveru
        var topic = parseTopic(window.location.pathname);
        startSession(topic);

        // bind events
        angular.element($window).bind('resize', function () {
            resize();
        });
}]);




// ===========================================================================
//  Helper functions
// ===========================================================================

// sets minimum height of the working area to tu full page height (minus footer
// height and margins)
function fullHeightWorkingArea() {
    var workingArea = $("#working-area")

    var footerHeight = $("#footer").outerHeight();  // outerHeight -> include padding
    var windowHeight = $(window).height();
    var marginTop = parseInt(workingArea.css("marginTop"));
    var marginBottom = parseInt(workingArea.css("marginBottom"));

    var fullHeight = windowHeight - footerHeight - marginTop - marginBottom;
    workingArea.css("min-height", fullHeight);
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
