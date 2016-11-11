//selectCourses.js
var currSubject = undefined;
var currNumber = undefined;
var currSection = undefined;

function populateCourseNumbers(courseNumbers){
	var newList = "";
	for(var i=0; i<courseNumbers.length; i++){
		newList += "<div class='number' id='"+courseNumbers[i]+"'>"+courseNumbers[i]+"</div>";
	}
	$(".courseNumber .scroll").html(newList);
}

function populateCourseSections(courseSections){
	var newList = "";
	for(var i=0; i<courseSections.length; i++){
		newList += "<div class='section' id='"+courseSections[i]+"'>"+courseSections[i]+"</div>";
	}
	$(".courseSection .scroll").html(newList);
}

function clearCourseNumbers(){
	currNumber = undefined;
	$(".courseNumbers .scroll").empty();
}

function clearCourseSections(){
	currSection = undefined;
	$(".courseSection .scroll").empty();
}

function displayCurrCourse(){
  $("#currCourse").html(currSubject+" "+currNumber+" section "+currSection);
}

function clearCurrCourse(){
  $("#currCourse").html("...");
}

function addCourseToSchedule(crn){
	var thisCourseSubject = undefined;
	var thisCourseNumber = undefined;
	var thisCourseSection = undefined;

	$.ajax({
    	contentType: "application/json",
        url: "/api/courses/crn/"+crn,
        method: "GET",
        async: true
    }).done(function(data) {
        console.log("Connection successful!");
        var course = data;
        if(course != undefined){
        	thisCourseSubject = course.subject;
        	thisCourseNumber = course.course_number;
    			thisCourseSection = course.section;
    			var newCourse = "<div class='enrolledCourse' crn='"+crn+"'> <a href='#''>[remove course, currently not functional]</a> "+thisCourseSubject+" "+thisCourseNumber+" section number "+thisCourseSection+"</div>";
          $(".mySchedule").append(newCourse);
        }

    }).fail(function(data){
        console.log("Connection failed!");
        var response = JSON.parse(data.responseText);
        if(response.error != undefined){
            console.log(response.error);
            window.alert(response.error);
       	}
    });
	
	
}

//highlights the subject selected
$(".scroll .subject").click(function() {
	$(".scroll .subject").css("background-color", "transparent");
	$(this).css("background-color", "#A3A3A3");
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
        clearCurrCourse();
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

//highlights the number selected
$(".scroll").on("click", ".number", function(){
	$(".scroll .number").css("background-color", "transparent");
	$(this).css("background-color", "#A3A3A3");
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
        clearCurrCourse();
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

//highlights the section selected
$(".scroll").on("click", ".section", function(){
	$(".scroll .section").css("background-color", "transparent");
	$(this).css("background-color", "#A3A3A3");
	currSection = $(this).attr('id');
  displayCurrCourse();
});

$("#selectClass").submit(function(e){
	e.preventDefault();
	if(!(currSubject && currNumber && currSection)){
		window.alert("You must select a course subject, course number, and a course section to register.");
		return false;
	}
    var body = {
          "subject": currSubject,
          "course_number": currNumber,
          "section": currSection
    }
    $.ajax({
          contentType: "application/json",
          url: "/api/course/register",
          method: "POST",
          data: JSON.stringify(body),
          async: true
    }).done(function(data) {
          console.log("Connection successful!");
          if(data.message != undefined){
               console.log(data.message);
               console.log("Hey user: "+ data.username);
               console.log("Got your CRN: " + data.crn);
               console.log("Matches???: " + data.matchedCourses);
               //add a thing to that myschedule block
               addCourseToSchedule(data.crn);
               //check for a match here.
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

    return false;
});