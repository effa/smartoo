smartooApp.controller('practiceController', ['$scope', function($scope) {
    // TODO
}]);

// for each new card displayed:
function fullHeightWorkingArea() {
    var footerTop = $("#footer").offset().top;
    var margin = parseInt($("#working-area").css("marginTop"));
    var fullHeight = footerTop - 2 * margin;
    console.log(footerTop);
    console.log(margin);
    console.log(fullHeight);


    //$("#working-area").height(footerTop - 2 * margin);
    $("#working-area").css("min-height", fullHeight);
}

// TODO: call after each new card display
fullHeightWorkingArea()
