// ---------------------------------------------------------
//  Event handlers
// ---------------------------------------------------------

function nextExerciseClick() {
    newExercise();
}

function answerClick() {
    if (answered) {
        return;
    }
    answered = true;
    evaluateAnswer(this);
}


// ----------------------------------------------------------
//  Ajax callbacks
// ----------------------------------------------------------
function exerciseDelivered(exercise) {
    console.log(response);
    newExercise(exercise);
}


// ----------------------------------------------------------
//  Exercise session actions
// ----------------------------------------------------------

function startExerciseSession() {
    // TODO: use AngularJS
    $.ajax({
        url: "/interface/create-ontology",
        type: "POST",
        datatype: "json",
        data: JSON.stringify({"url":url}),
        success: exerciseDelivered
    });
}

function newExercise(exerciseHtml) {
    // use AngluarJS
    $("#working-area").html(exerciseHtml);
    //$("#exercise .choices .button.active").click(answerClick);
    //$("#new-exercise").click(nextExerciseClick);
    answered = false;
}

