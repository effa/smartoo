// Main javascript file for the whole Smartoo site
var smartooApp = angular.module('smartooApp', ['ngCookies']).
    config(['$httpProvider', function($httpProvider, $cookies){
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]).
    run(['$http','$cookies', function($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);


smartooApp.controller('mainController', ['$scope', 'smartooService',
        function($scope, smartooService) {

    $scope.message = {
        text: "",
        email: "",
        success: false,
        failure: false
    };

    $scope.sendMessage = function() {
        message = {
            text: $scope.message.text,
            email: $scope.message.email
        };
        smartooService.sendMessage(message).then(function(response) {
            if (response.success) {
                $scope.message.failure = false;
                $scope.message.success = true;
            } else {
                $scope.message.success = false;
                $scope.message.failure = true;
            }
        });
    }
}]);


// visual properties (NOTE: ideally visual properties should be in directives)
$(document).ready(function() {
    $('#writeUsModal').on('shown.bs.modal', function(e){
        // focus text area
        $("#message-text").focus();

        // unfocus modal trigger button
        $('#writeUsBtn').one('focus', function(e){
            $(this).blur();
        });
    });
});


// ===========================================================================
//  Helper functions
// ===========================================================================

// returns response object (makes sure success and message attributes are set)
function createFailResponse(response) {
    var data = response.data;
    //console.log(data);

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

