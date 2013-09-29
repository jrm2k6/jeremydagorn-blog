
$(document).ready(function() {
	$(".delete-btn" ).click(function() {
		var id = $(this).closest('tr')[0].id;
		id = id.replace('_', '/')
		$.post('/delete/' + id, function(data) {
			console.log(data);
		});
	});
});