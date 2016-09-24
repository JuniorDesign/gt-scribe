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
                    console.log("Welcome user: "+data.username);
               }
          //and redirect to another page

     }).fail(function(data){ //error messages come in as a diff format than success messages
          console.log("Connection failed!");
          var response = JSON.parse(data.responseText);
          if(response.error != undefined){
               console.log(response.error);
          }
     });

     return false;
});