$(function() {
	$('.file-upload').change(function(e) {
		var files = e.target.files || e.dataTransfer.files;
      	var file = files[0];
      	var userID = $('#username').text();
      	var courseID = $('#course-id').text();
      	var formData = new FormData();
      	
      	formData.append('file', file);
      	formData.append('user_id', userID);
      	formData.append('course_id', courseID);
      	
      	for (var pair of formData.entries()) {
    		console.log(pair[0]+ ', ' + pair[1]); 
		}
      	
      	$('.upload-btn').click(function() {
      		console.log('Request Sent!');
      		$.ajax({
	          contentType: false,
	          processData: false,
	          url: '/api/taker/notes',
	          method: 'POST',
	          data: formData,
	          async: true
	     	})
	     	.done(function(data) {
	          console.log('Connection Successful!');
	     	})
	     	.fail(function(data) { //error messages come in as a diff format than success messages
	          console.log('Connection failed!');
	          var response = JSON.parse(data.responseText);
	          if (response !== null && response !== undefined && 
	          	  response.error !== null && response.error !== undefined) { 
              	console.log(response.error);
	            window.alert(response.error); //temporary feedback to user until we create a UI for this
	          }
	     	});

	     	return false;
      	});
	});
});