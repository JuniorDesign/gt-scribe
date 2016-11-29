//selectCourses.js
var currSubject = undefined;
var currNumber = undefined;
var currSection = undefined;

function populateCourseNumbers(courseNumbers){
    var newList = "";
    for(var i=0; i<courseNumbers.length; i++){
        newList+="<tr class='number' id='"+courseNumbers[i]+"'><td>"+courseNumbers[i]+"</td></tr>";
    }
    $(".courseNumber .scroll table").html(newList);
}

function populateCourseSections(courseSections){
    var newList = "";
    for(var i=0; i<courseSections.length; i++){
        newList+="<tr class='section' id='"+courseSections[i]+"'><td>"+courseSections[i]+"</td></tr>";
    }
    $(".courseSection .scroll table").html(newList);
}

function clearCourseNumbers(){
    currNumber = undefined;
    $(".courseNumbers .scroll table").empty();
}

function clearCourseSections(){
    currSection = undefined;
    $(".courseSection .scroll table").empty();
}

function displayCurrCourse(){
    $("#currCourse").html(currSubject+" "+currNumber+" section "+currSection);
}

function clearCurrCourse(){
    $("#currCourse").html("...");
}

//adds course to the schedule on the dom
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
                    var newCourse = "<div class='enrolledCourse' crn='"+crn+"'>"
                        +"<button class='btn btn-danger btn-sm delete' id='"+crn+"']}}'>X</button> "
                        +thisCourseSubject+" "+thisCourseNumber+" section "+thisCourseSection
                        +"</div>";
                    $(".mySchedule .scroll").append(newCourse);
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

//removes the deleted course from the dom
function removeCourseFromSchedule(crn){
    $(".enrolledCourse[crn="+crn+"]").remove()
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


//selecs the course and adds it to the user's schedule in the db, calls a function to update the dom
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
                        addCourseToSchedule(data.crn);
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

//delete course on red X click, deletes database info and then calls to update the dom
$(".scroll").on("click", ".enrolledCourse .delete", function(){
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