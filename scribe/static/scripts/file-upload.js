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
	        	url: '/api/notes',
	        	method: 'POST',
	        	data: formData,
	        	async: true
	     	})
	     	//consider putting a spinner here to show loading
	     	.done(function(data) {
				console.log('Connection Successful!');
				window.alert("You've successfully uploaded "+file.name);
	     	})
	     	.fail(function(data) {
	        	console.log('Connection failed!');
	     	});

	     	return false;
      	});
	});
});