// --------------------------------------------------------------------------
// Factoriries and servicies
// --------------------------------------------------------------------------

//smartooApp.factory('smartooFactory', function($http) {
//    return {
//        // TODO: ?? $q ??
//        buildKnowledge: function() {
//            return $http.post('/interface/start-session', {topic: topic})
//                .then(function(result) {
//                    console.log(result);
//                    console.log('****************************88');
//                    return result
//                    //return result.data;
//                });
//        }
//        // TODO: more  functions
//    }
//});
smartooApp.service('smartooService', ['$http', function ($http) {

    this.buildKnowledge = function(topic) {
        return $http.post('/interface/start-session', {topic: topic})
            .then(function(response) {
                return response.data;
            }, function(response) {
                data = response.data

                // make sure success is false
                data.success = false;

                // if there is no error message in the response, use "Server
                // error")
                if (!data.message) {
                    data.message = "Server error";
                }
                return data;
            });
    }

    // TODO: more  functions
}]);


// --------------------------------------------------------------------------
//  Controllers
// --------------------------------------------------------------------------
smartooApp.controller('practiceController',
    ['$scope', '$location', '$http', 'smartooService',
            function($scope, $location, $http, smartooService) {

        // initial state is "waiting"
        $scope.errorMessage = null;
        $scope.infoMessage = "Building knowledge..."
        $scope.state = "waiting";

        var topic = parseTopic(window.location.pathname);

        smartooService.buildKnowledge(topic).then(function(response) {
            if (response.success) {
                console.log(response);
                $scope.infoMessage = "Creating exercises..."
                // TODO ... create exercises
            } else {
                $scope.errorMessage = data.message;
                $scope.state = "error";
            }
        });
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
