//selectCourses.js

function populateSubjects(){}

window.onload = populateSubjects();


//highlights the item selected
$("li.subject").click(function(){
  $("li.subject").css("background-color", "white");
  $(this).css("background-color", "yellow");
  var subject = $('#test').attr('id')
  //do ajax
  $.ajax({
          contentType: "application/json",
          url: "/api/courses/"+subject,
          method: "GET",
          async: true
     }).done(function(data) {
          console.log("Hey!!!");
          /*if(data.message != undefined){
               console.log(data.message);
               console.log("Welcome user: "+ data.username);
               console.log("User account type: " + data.accountType);
               currUsername = data.username;
               window.location.href = "/";
          }*/
          //if you get back out here before the location change, something went wrong.

     }).fail(function(data){ //error messages come in as a diff format than success messages
          console.log("Connection failed!");
          /*var response = JSON.parse(data.responseText);
          if(response.error != undefined){
               console.log(response.error);
               window.alert(response.error); //temporary feedback to user until we create a UI for this
          }*/
     });
});


