// Main javascript file for the whole Smartoo site
var smartooApp = angular.module('smartooApp', ['ngCookies']).
    config(['$httpProvider', function($httpProvider, $cookies){
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]).
    run(['$http','$cookies', function($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);

// TODO: mainController (footer buttons etc.)
smartooApp.controller('mainController', ['$scope', function($scope) {
    // TODO
    //$scope.focusTextArea = function() {
    //    m = $('#message-text');
    //    console.log(m);
    //    $('#message-text').focus();
    //};
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
