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
//  Controllers
// --------------------------------------------------------------------------
smartooApp.controller('practiceController',
    ['$scope', '$location', '$http', '$window', '$document', 'smartooService',
            function($scope, $location, $http, $window, $document, smartooService) {

        function startSession(topic) {
            smartooService.startSession(topic).then(function(response) {
                if (response.success) {
                    $scope.topic.name = response.topic;
                    $scope.topic.uri = "http://en.wikipedia.org/wiki/" + response.topic.replace(" ", "_");
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

        $scope.reloadPage = function() {
            window.location.reload();
        }

        $scope.blur = function($event) {
            //console.log($event);
            // unfocus
            $event.target.blur();
        }

        function resize() {
            fullHeightWorkingArea();
        }

        // initial visual settings
        resize();

        // initial state is "waiting"
        $scope.errorMessage = null;
        $scope.infoMessage = "Building knowledge..."
        $scope.state = "waiting";
        $scope.topic = {name:'', uri:''};

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
