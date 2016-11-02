//selectCourses.js

function populateCourseNumbers(courseNumbers){

}

window.onload = populateSubjects();

//highlights the item selected
$("li.subject").click(function(){
	$("li.subject").css("background-color", "white");
	$(this).css("background-color", "yellow");
	var subject = $(this).attr('id')
	//do ajax
	$.ajax({
    	contentType: "application/json",
        url: "/api/courses/distinct/"+subject,
        method: "GET",
        async: true
    }).done(function(data) {
        console.log("Connection successful!");
        var courseNumbers = data;
        console.log(courseNumbers);
        if(courseNumbers != undefined){
        	populateCourseNumbers(courseNumbers);
        }

    }).fail(function(data){ //error messages come in as a diff format than success messages
        console.log("Connection failed!");
        var response = JSON.parse(data.responseText);
        if(response.error != undefined){
            console.log(response.error);
            window.alert(response.error); //temporary feedback to user until we create a UI for this
       	}
    });
});


