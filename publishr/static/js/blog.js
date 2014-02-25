'use strict';

$(window).load(function() {
	removeCurrentActiveClass();
	$(".blog").addClass("active");
	$(".post-content").find("pre").each(function() {
		$(this).addClass("code-snippet");
	});
});