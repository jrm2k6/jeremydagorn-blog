
$(document).ready(function() {
	var test;

	$(".delete-btn" ).click(function() {
		var id = $(this).closest('tr')[0].id;
		id = id.replace('_', '/');
		$.post('/delete/' + id, function(data) {
			console.log(data);
		});
	});

	$(".edit-btn").click(function() {
		var listFields = $(this).closest('table').data('list-fields');
		var editables = $(this).closest('tr').find('td.editable').each(function() {
			var text = $(this).text();
			var currentId = $(this).attr("id");
			$(this).replaceWith('<td><input id="'+currentId+'" type="text" value="' + text +'"></input></td>');
		});

		$(this).addClass("btn-success").val("Update").click(function() {
			var id = $(this).closest('tr')[0].id;
			id = id.replace('_', '/');

			var _username = $(this).closest('tr').find('input#username').val();
			var _email = $(this).closest('tr').find('input#email').val();

			$.ajax({
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify({'_username': _username, '_email': _email}),
				dataType: 'json',
				url: '/update/' + id
			});

			$(this).removeClass("btn-success").val("Edit");

			var inputs = $(this).closest('tr').find('input').each(function() {
				var text = $(this).val();
				var currentId = $(this).attr("id");
				// $(this).replaceWith('<td class="editable" id=><input id="'+currentId+'"' + text +'</td>');
			});
		});
	});
});