smartooApp.controller('practiceController',
    ['$scope', '$location', '$http', function($scope, $location, $http) {

        // initial state is "waiting"
        $scope.errorMessage = null;
        $scope.state = "waiting";

        var topic = parseTopic(window.location.pathname);

        $http.post('/interface/start-session', {topic: topic}).
        success(function(data, status, headers, config) {
            console.log("success");
            console.log(data);
            console.log(status);
            if (data.success == false) {
                $scope.errorMessage = data.message;
                $scope.state = "error";
            }
        }).
        error(function(data, status, headers, config) {
            console.log("error");
            console.log(data);
            console.log(status);
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
