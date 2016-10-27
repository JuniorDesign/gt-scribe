$(function() {
	$('.file-upload').change(function(e) {
		var files = e.target.files || e.dataTransfer.files;
      	var file = files[0];
      	var formData = new FormData();
      	formData.append('file', file);
      	
      	console.log(file);
      	for (var pair of formData.entries()) {
    		console.log(pair[0]+ ', ' + pair[1]); 
		}
      	
      	$('.upload-btn').click(function() {
      		console.log('request sent!');
      		$.ajax({
	          contentType: false,
	          processData: false,
	          url: '/api/taker/notes',
	          method: 'POST',
	          data: formData,
	          async: true
	     	})
	     	.done(function(data) {
	          console.log('Connection successful!');
	          if (data.message != undefined){
	               console.log(data.message);
	          }
	     	})
	     	.fail(function(data) { //error messages come in as a diff format than success messages
	          console.log('Connection failed!');
	          var response = JSON.parse(data.responseText);
	          if (response.error != undefined){
              	console.log(response.error);
	            window.alert(response.error); //temporary feedback to user until we create a UI for this
	          }
	     	});

	     	return false;
      	});
	});
});