//selectCourses.js
var currSubject = undefined;
var currNumber = undefined;
var currSection = undefined;

function populateCourseNumbers(courseNumbers){
	var newList = "";
	for(var i=0; i<courseNumbers.length; i++){
		newList += "<li class='number' id='"+courseNumbers[i]+"'>"+courseNumbers[i]+"</li>";
	}
	$(".courseNumber ol").html(newList);
}

function populateCourseSections(courseSections){
	var newList = "";
	for(var i=0; i<courseSections.length; i++){
		newList += "<li class='section' id='"+courseSections[i]+"'>"+courseSections[i]+"</li>";
	}
	$(".courseSection ol").html(newList);
}

function clearCourseNumbers(){
	currNumber = undefined;
	$(".courseNumbers ol").empty();
}

function clearCourseSections(){
	currSection = undefined;
	$(".courseSection ol").empty();
}

//highlights the item selected
$("li.subject").click(function(){
	$("li.subject").css("background-color", "white");
	$(this).css("background-color", "yellow");
	var subject = $(this).attr('id');
	$.ajax({
    	contentType: "application/json",
        url: "/api/courses/distinct/"+subject,
        method: "GET",
        async: true
    }).done(function(data) {
        console.log("Connection successful!");
        clearCourseNumbers();
        clearCourseSections();
        currSubject = subject; //save so we can use it if the user selects this course
        var courseNumbers = data;
        if(courseNumbers != undefined){
        	populateCourseNumbers(courseNumbers);
        }

    }).fail(function(data){
        console.log("Connection failed!");
        currSubject = undefined;
        var response = JSON.parse(data.responseText);
        if(response.error != undefined){
            console.log(response.error);
            window.alert(response.error);
       	}
    });
});

$("ol").on("click", "li.number", function(){
	$("li.number").css("background-color", "white");
	$(this).css("background-color", "yellow");
	var number = $(this).attr('id');
	$.ajax({
    	contentType: "application/json",
        url: "/api/courses/distinct/"+currSubject+"/"+number,
        method: "GET",
        async: true
    }).done(function(data) {
        console.log("Connection successful!");
        currNumber = number; //save so we can use it if the user selects this course
        clearCourseSections();
        var courseSections = data;
        if(courseSections != undefined){
        	populateCourseSections(courseSections);
        }

    }).fail(function(data){
        console.log("Connection failed!");
        var response = JSON.parse(data.responseText);
        if(response.error != undefined){
            console.log(response.error);
            window.alert(response.error);
       	}
    });
});

$("ol").on("click", "li.section", function(){
	$("li.section").css("background-color", "white");
	$(this).css("background-color", "yellow");
	currSection = $(this).attr('id');
});

