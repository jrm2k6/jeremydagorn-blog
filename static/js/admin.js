var REGEX_LIST_FIELDS = /[\'\[\]\' ']/g;

$(document).ready(function() {

	$(".delete-btn" ).click(function() {
		var modelName = $(this).closest('table').data('model-name');
		$.post('/delete/' + modelName, function(data) {
			console.log(data);
		});
	});

	$(".edit-btn").click(function() {
		var listFields = $(this).closest('table').data('list-fields');
		listFields = listFields.replace(REGEX_LIST_FIELDS, "").split(',')
		
		var modelName = $(this).closest('table').data('model-name');
		var editables = $(this).closest('tr').find('td.editable').each(function() {
			var text = $(this).text();
			var currentId = $(this).attr("id");
			$(this).replaceWith('<td><input id="'+ currentId +'" type="text" value="' + text +'"></input></td>');
		});

		$(this).addClass("btn-success").val("Update").click(function() {
			var newValuesForModelFields = {}
			var idToUpdate;
			for (var i = 0; i < listFields.length; i++) {
				var key = listFields[i];
				var inputStr = 'input#' + key;
				if (key === "id") {
					// get id of object
				} else {
					var inputValue = $(this).closest('tr').find(inputStr).val();
					newValuesForModelFields['_'+key] = inputValue;
				}
			};

			// $.ajax({
			// 	type: 'POST',
			// 	contentType: 'application/json',
			// 	data: JSON.stringify(newValuesForModelFields),
			// 	dataType: 'json',
			// 	url: '/update/' + modelName
			// });

			$(this).removeClass("btn-success").val("Edit");

			var inputs = $(this).closest('tr').find('input').each(function() {
				var text = $(this).val();
				var currentId = $(this).attr("id");
				// $(this).replaceWith('<td class="editable" id=><input id="'+currentId+'"' + text +'</td>');
			});
		});
	});
});