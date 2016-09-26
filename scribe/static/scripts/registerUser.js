var selectedType=""; //for registration

/**
* Determines type of account the user will have in the DB.
* Grabs the value off of the dropdown type menu and stores it in the variable.
* This is a jQuery eventlistener added to each drop-down item.
*/
$(".register-type-btn").click(function(e){
     //this works because it seeks a 'value' attribute on the thing we click
     selectedType = e.target.attributes["value"].value;
     });

/**
* Registers the user's input into the database.
* Grabs the variables from the form via query selectors on the id names.
* Creates a JSON file with them that corresponds to the expected keys
* in our api.py file. Creates an ajax POST request to the endpoint we
* described in routes.py, which we assigned the UserRegistration resource to,
* which is again defined in api.py.
* We then wait for a response from the endpoint (success or fail).
*/
$("#registerUserForm").submit(function(){
     var username = $("#usernameInput").val();
     var firstName= $("#firstNameInput").val();
     var lastName = $("#lastNameInput").val();
     var password = $("#passwordInput").val();
     var body = {
          "username": username,
          "password": password,
          "firstName": firstName,
          "lastName": lastName,
          "type": selectedType
     }
     $.ajax({
          contentType: "application/json",
          url: "/api/register",
          method: "POST",
          data: JSON.stringify(body),
          async: true
     }).done(function(data) {
          console.log("Connection successful!");
          if(data.message != undefined){
               console.log(data.message);
          }
          //and redirect to another page here

     }).fail(function(data){ //error messages come in as a diff format than success messages
          console.log("Connection failed!");
          var response = JSON.parse(data.responseText);
          if(response.error != undefined){
               console.log(response.error);
          }
     });

     return false;
});