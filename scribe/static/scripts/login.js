$("#loginForm").submit(function(){
     var username = $("#usernameInput").val();
     var password = $("#passwordInput").val();
     var body = {
          "username": username,
          "password": password,
     }
     $.ajax({
          contentType: "application/json",
          url: "/api/login",
          method: "POST",
          data: JSON.stringify(body),
          async: true
     }).done(function(data) {
          console.log("Connection successful!");
          if(data.message != undefined){
               console.log(data.message);
               console.log("Welcome user: "+ data.username);
               console.log("User account type: " + data.accountType);
               window.location.href = data.accountType.toLowerCase();
          }
          //if you get back out here before the location change, something went wrong.

     }).fail(function(data){ //error messages come in as a diff format than success messages
          console.log("Connection failed!");
          var response = JSON.parse(data.responseText);
          if(response.error != undefined){
               console.log(response.error);
               window.alert(response.error); //temporary feedback to user until we create a UI for this
          }
     });

     return false;
});
