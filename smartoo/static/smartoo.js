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
}]);
