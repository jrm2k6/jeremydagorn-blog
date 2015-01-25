'use strict';

var REGEX_LIST_FIELDS = /[\'\[\]\' ']/g;

var getResourcePath = function(that) {
	var modelName = $(that).closest('table').data('model-name');
	var selectedId = $(that).closest('tr').find('td#id')[0].textContent.trim();

	return modelName + '/' + selectedId;
};

function removeAlerts() {
    setTimeout(function(){
        var selectedEffect = 'blind';
        var options = {};
        $(".alert").hide();
     }, 5000);
}

$(document).ready(function() {
	removeAlerts();

	$(".delete-btn" ).click(function() {
		var that = $(this);
		$.post('/delete/' + getResourcePath(this), function(data) {
			that.parent().parent().remove();
		});
	});

	$(".edit-btn").click(function() {
		getResourcePath(this);
		var listFields = $(this).closest('table').data('list-fields');
		listFields = listFields.replace(REGEX_LIST_FIELDS, "").split(',');
		
		var modelName = $(this).closest('table').data('model-name');
		var editables = $(this).closest('tr').find('td.editable').each(function() {
			var text = $(this).text();
			var currentId = $(this).attr("id");
			$(this).replaceWith('<td><input class="edited" id="'+ currentId +'" type="text" value="' + text +'"></input></td>');
		});

		$(this).addClass("btn-success").val("Update").click(function() {
			var newValuesForModelFields = {};
			var idToUpdate;
			for (var i = 0; i < listFields.length; i++) {
				var key = listFields[i];
				var inputStr = 'input#' + key;
				if (key === "id") {
					var cellId = $(this).closest('tr').find('td#id')[0];
					idToUpdate = cellId.textContent.trim();
				} else {
					var inputValue = $(this).closest('tr').find(inputStr).val();
					newValuesForModelFields['_'+key] = inputValue;
				}
			}
			
			modelName = modelName + '/' + idToUpdate;

			$.ajax({
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify(newValuesForModelFields),
				dataType: 'json',
				url: '/update/' + modelName
			});

			$(this).removeClass("btn-success").val("Edit");

			var inputs = $(this).closest('tr').find('.edited').each(function() {
				var text = $(this).val();
				var currentId = $(this).attr("id");
				$(this).replaceWith('<td style="border:none;" class="editable" id="'+currentId+'">' + text.trim() +'</td>');
			});
		});
	});


        $('.export-database-btn').click(function() {
            $.ajax({
                type: 'POST',
                url: '/export_database'
            })
        });

        $('#archive-export').click(function() {
            $.ajax({
                type: 'GET',
                url: '/export_archive',
            }).success(function(data) {
                showAvailableFilesToExport(data["exportablePosts"], true);
            })
        });

        $('.authorize-export-posts-btn').click(function(event) {
            var exportBtnElement = $(event.target);
            var exportType = exportBtnElement.data('exportType');
        	$.ajax({
        		type: 'GET',
        		url: '/authorize_posts_backup/' + exportType,
        		dataType: 'json'
        	}).success(function(data) {
        		$('.authorize-url').css('display', 'block');
        		$('.authorize-url').html("<div><a href=" + data["aurl"] + " target=_blank>" + data["aurl"] + "</a><div>"
        			+"<div><form id=\"form-verification-code\" method=\"post\" role=\"form\">"
        			+ "<input type=\"text\" class=\"export-form-input\" name=\"verification-code\"></input>"
        			+"<input type=\"button\" class=\"export-verification-code-btn btn btn-primary disabled\" value=\"Submit code\">"
        			+ "</input></form>");
        		
        		$('input[class=export-form-input]').bind("propertychange input paste", function() {
        			$(".export-verification-code-btn").removeClass("disabled");
        		});

        		$('.export-verification-code-btn').click(function() {
        			$.ajax({
        				type: 'POST',
        				url: '/submit_verification_code',
        				dataType: 'json',
        				data: $('#form-verification-code').serialize()
        			}).success(function(data) {
        				showAvailableFilesToExport(data["exportablePosts"], false);
        				$('.btn-posts-choice').click(function() {
        					$.ajax({
        						type: 'POST',
        						url: '/export_files',
        						dataType: 'json',
        						data: $('#form-posts-choice').serialize()
        					}).success(function(data) {
                                $('.authorize-url').css('display', 'block');
                                $('.authorize-url').html("<div class=\"alert alert-success alert-dismissible\" role=\"alert\">"
                                    + "File(s) successfully exported!</div>");
                            }).error(function(data) {
                                $('.authorize-url').css('display', 'block');
                                $('.authorize-url').html("<div class=\"alert alert-error alert-dismissible\" role=\"alert\">"
                                    + "Oops, something went wrong!</div>");
                            });
        				});
        			}).error( function(data) {
        				$('.authorize-url').css('display', 'block');
        				$('.authorize-url').html("<div class=\"alert alert-error alert-dismissible\" role=\"alert\">"
        				+ "Oops, the code you submitted is wrong!</div>");
        			})
        		});
        	}).error(function(data) {
        		$('.authorize-url').css('display', 'block');
        		$('.authorize-url').html("<div class=\"alert alert-error alert-dismissible\" role=\"alert\">"
        			+ "Oops, something went wrong!</div>");
        	})
        });

	var showAvailableFilesToExport = function(exportablePosts, isDirectDownload) {
        var btnType = (isDirectDownload) ? "submit" : "button";
        var formDeclaration = "";
        if (isDirectDownload) {
            formDeclaration = "<form id=\"form-posts-choice\" method=\"post\" role=\"form\" action=\"/export_files\">";
        } else {
            formDeclaration = "<form id=\"form-posts-choice\" method=\"post\" role=\"form\">";
        }

		$('.authorize-url').css('display', 'block');
        $('.authorize-url').html("<div class=\"div-exportable-files\">"
        	+ formDeclaration
        	+"<fieldset class=\"group\">"
        	+"<legend>Available files to export</legend>"
			+"<ul class=\"ul-exportable-files\">"
			+"</ul>" 
			+"</fieldset>"
			+"<input type=" + btnType +" class=\"btn-posts-choice btn btn-primary\" value=\"Export files\">"
        	+"</input></form></div>");

        for (var i=0; i<exportablePosts.length; i++) {
        	$('.ul-exportable-files').append('<li><input type=\"checkbox\" name=\"v'+i+'\" value=\"'+exportablePosts[i]+'\"/><label for=\"v'+i+'\">'+exportablePosts[i]+'</label></li>');
        }

	}

    $('.left-menu-item').click(function(event) {
        var menuItem = $(this);
        var tabToOpen = menuItem.data('content');
        var tabElems = $("div[id$='-tab']");

        tabElems.each(function(index, elem) {
            var $elem = $(elem);
            if ($elem.attr('id') === tabToOpen) {
                $elem.css('display', 'block');
            } else {
                $elem.css('display', 'none');
            }
        });
    })
});
