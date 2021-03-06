//turns the whole row of the table clickable
$(".course").click(function() {
    var url = "notes/"+$(this).attr('id');
    window.location = url;
});

//deletes a class out of the unmatched courses list
$(".delete").click(function() {
    var crnToDelete = $(this).attr('id');
    console.log("I've clicked: "+ $(this).attr('id'));
    var body = {
        "course_id": crnToDelete
    }
    $.ajax({
        contentType: "application/json",
        url: "/api/enrollment/delete",
        method: "DELETE",
        data: JSON.stringify(body),
        async: true
    }).done(function(data) {
        console.log("Connection successful!");
        if(data.message != undefined){
            console.log(data.message);
            removeCourseFromSchedule(data.crn);
        }

    }).fail(function(data){ //error messages come in as a diff format than success messages
        console.log("Connection failed!");
        console.log(data);
        var response = JSON.parse(data.responseText);
        if(response.error != undefined){
            console.log(response.error);
            window.alert(response.error); //temporary feedback to user until we create a UI for this
        }
    });
});

//removes the deleted course from the dom
function removeCourseFromSchedule(crn){
	console.log("I removed the course, "+crn);
    $(".unmatchedCourse[crn="+crn+"]").remove()
}