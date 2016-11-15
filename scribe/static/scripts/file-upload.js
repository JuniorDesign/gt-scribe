$(function() {
	$('.file-upload').change(function(e) {
		var files = e.target.files || e.dataTransfer.files;
      	var file = files[0];
      	var courseID = window.location.href.match(/.*\/notes\/(\d+)\W*.*/);
      	var courseID = courseID.length <= 1 ? '' : courseID[1] 
      	var formData = new FormData();

      	formData.append('file', file);
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
				location.reload();
	     	})
	     	.fail(function(data) {
	        	console.log('Connection failed!');
	     	});

	     	return false;
      	});
	});
});
