/* global $, document, window, CONFIG, removeCurrentActiveClass*/
'use strict';


var cells = [];
var _projects;
var MIN_SIZE = 400;
var listLayout;
var cellsLayout;

function getWidthAsStringFromCSSProperty(value) {
	return value.replace("px", "").toString();
}

function createSquareElement(i, _text) {
    var $rect = $('<div>', { id: "rect_" + i});
    return $rect;
}

function getRandom(minValue, maxValue) {
	var p =  Math.round(Math.random() * (maxValue - minValue + 1)) + minValue;
	return p;
}	

function Cell() {}

Cell.prototype = {
	init : function(id, rectangle, x, y, width, height, direction, color) {
		this.id = id;
		this.rectangle = rectangle;
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.direction = direction;
		this.color = color;
	},

	applyCSSAndAnimate : function(_id, _rectangle, _width, _height, _left, _top, _direction, _color) {
		this.init(_id, _rectangle, _left, _top, _width, _height, _direction, _color);

		var cssParams = {
			id: _id,
			'background-color': _color,
			color: 'white',
			width: _width,
			height: _height,
			position: 'absolute',
			display: 'none',
		};

		var animParams = {
			opacity: "show",
		};

		var params = this.generateAnimationDirection(_direction);

		$.extend(cssParams, params[0]);
		$.extend(animParams, params[1]);
		_rectangle.css(cssParams).animate(animParams, 1000);
		_rectangle.data('bg-color', _color);

		this.setMouseListeners();
	},

	setMouseListeners : function() {
		this.rectangle.on("mouseover", function() {
			$(this).css({
						"background-color": "gray",
						"-webkit-transition": "0.5s",
						"-moz-transition": "0.5s",
						"-o-transition": "0.5s",
						"-ms-transition": "0.5s",
						"transition": "0.5s"
			});
		});

		this.rectangle.on("mouseout", function() {
			var color = $(this).data("bg-color");
			$(this).css({
						"background-color": color,
						"-webkit-transition": "0.5s",
						"-moz-transition": "0.5s",
						"-o-transition": "0.5s",
						"-ms-transition": "0.5s",
						"transition": "0.5s"
					});
		});
	},

	removeMouseListeners : function() {
		this.rectangle.unbind("mouseover");
		this.rectangle.unbind("mouseout");

		this.rectangle.css("background-color", this.color);
	},

	setLine : function(i) {
		if (i === 0) {
			this.line = 1;
		} else {
			this.line = Math.round(i/2);
		}
	},

	setProject : function(obj) {
		this.project = new Project();
		this.project.init(obj);

		this.displayProjectInformation();
	},

	displayProjectInformation : function() {
		var $rect = $("#rect_"+this.id);
		$rect.css({
			"padding-top": "10px",
			"padding-left": "10px",
			"spacing": "5px",
		});
		var statusId = this.project.status;

		var $statusIcon = $('<div>', {id: "status_icon_" + this.id});
		$statusIcon.addClass("status-floating glyphicon white " + this.project.getGlyphiconNameFromStatus());

		$rect.append($statusIcon);

		var $title = $('<div>', { id: "title_" + this.id, text: this.project.title});
		var $description = $('<div>', { id: "description_" + this.id, text: this.project.getTruncatedDescription()});
		var $technologies = $('<div>', { id: "technologies_" + this.id, text: this.project.technologies.replace(",", ", ").toUpperCase()});
		
		$title.css({"font-size" : "22px", "padding-bottom" : "5px", "border-bottom" : "2px solid white"});
		$description.css({"margin-top" : "10px", "font-size" : "18px"});
		$technologies.css({"width" : "100%", "position" : "absolute", "bottom": "10px", "padding" : "5px 5px 0px 5px", "border-left" : "4px solid white"});
		
		$rect.append($title);
		$rect.append($description);
		$rect.append($technologies);
	},

	generateAnimationDirection : function(direction) {
		var _cssParams = {};
		var _animParams = {};
		if (direction == "top") {
			_cssParams.top = this.y - this.height;
			_cssParams.left = this.x;

			_animParams.top = this.y;
		} else if (direction == "bottom") {
			_cssParams.top = this.y + this.height;
			_cssParams.left = this.x;

			_animParams.top = this.y;
		} else if (direction == "left") {
			_cssParams.top = this.y;
			_cssParams.left = this.x - this.width;

			_animParams.left = this.x;
		}  else if (direction == "right") {
			_cssParams.top = this.y;
			_cssParams.left = this.x + this.width;

			_animParams.left = this.x;
		}

		return [_cssParams, _animParams];
	}
};


function Project() {}

Project.prototype = {
	
	init : function(obj) {
		this.id = obj.id;
		this.title = obj.title;
		this.description = obj.description;
		this.status = obj.status;
		this.technologies = obj.technologies;
	},

	getStatusAsString : function() {
		var STATUS = ["DONE", "IN-PROGRESS"];
		var status = this.status-1;
		if (this.status !== undefined) {
			if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." +
				"Have you referenced your new status in this array?");
			return STATUS[status];
		}
	},

	getGlyphiconNameFromStatus : function() {
		var STATUS = ["glyphicon-ok", "glyphicon-pencil"];
		var status = this.status-1;
		if (this.status !== undefined) {
			if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." +
				"Have you referenced your new status in this array?");
			return STATUS[status];
		}
	},

	getTruncatedDescription : function() {
		if (this.description.length > 150) {
			return this.description.substring(0, 146) + "...";
		} else {
			return this.description;
		}
	}
};

function ListLayout() {}

ListLayout.prototype = {
	createContainerProject : function(i) {
		var $container = $('<div>', { id: "container_project_" + i});
		$container.css({"margin-top": "20px"});
		return $container;
	},

	createProjectTitleDiv : function(i, project) {
		var $div = $('<div>', { id: "title_" + i, text: project.title});
		$div.css({color: "white", "font-size": "20px"});
		$div.attr("data-status", project.getStatusAsString());
		$div.attr("data-description", project.getTruncatedDescription());
		$div.mouseover(function() {
			$div.css("color", "#e77471");
		});

		$div.mouseout(function() {
			$div.css("color", "white");
		});
		var self = this;
		$div.on("click", function() {
			self.closeOpenItem();
			self.displayProjectDetails(_projects[i], $(this).attr("data-status"));
		});

		return $div;
	},

	closeOpenItem : function(){
		if (this.openItem === undefined) return;

		var id = parseInt(this.openItem.attr("id").split("_")[2], 10);
		var idFullDivs = id + 1;
		
		this.openItem.removeClass("list_layout_detailed_project");

		$("#description_" + idFullDivs).remove();
		$("#technologies_" + idFullDivs).remove();
		$("#status_" + idFullDivs).remove();
		var $title = this.openItem.find(">:first-child");
		$title.css("border-bottom", "none");
		var shortDescription = $title.attr("data-description");
		var $description = $('<div>', {id: "description_" + id, text: shortDescription});
		$description.addClass("pink-description");
		this.openItem.append($description);

	},

	displayProjectDetails : function(project, statusAsString) {
		var id = project.id - 1;
		var $container = $("#container_project_" + id);

		$("#description_"+ id).remove();
		this.openItem = $container;
		
		$container.addClass("list_layout_detailed_project");

		var $title = $("#title_" + id);
		$title.css({"padding-bottom": "3px", "border-bottom":"1px solid #ffa5d2", "color" : "#e77471"});

		var $description = $('<div>', {id: "description_" + project.id, text: project.description});
		$description.css({"color": "white", "size" : "18px"});
		$container.append($description);

		var $technologies = $('<div>', {id: "technologies_" + project.id, text: project.technologies});
		$technologies.css({"color": "#a1a8a3", "size" : "17px"});
		$container.append($technologies);

		var $status = $('<div>', {id: "status_" + project.id, text: statusAsString});
		$status.css({"color": "#ffa5d2", "size" : "17px"});
		$container.append($status);
	},

	createProjectDescriptionDiv : function(i, project) {
		return $('<div>', {id: "description_" + i, text: project.getTruncatedDescription()}).addClass("pink-description");
	},

	displayProjectsAsList : function() {
		$("#pgrid").css("height", 800);
		$("#listing").text("Display as cells layout");
		$("#listing").attr("data-layout", 1);
	
		fadeOutCellsAndDisplayProjectsAsList();
		
		for (var i=0; i<cells.length; i++) {
			var project = cells[i].project;
			var $container = this.createContainerProject(i);
			var $divProjectTitle = this.createProjectTitleDiv(i, project);
			var $divProjectDescription = this.createProjectDescriptionDiv(i, project);
			
			$("#pgrid").append($container);
			$container.append($divProjectTitle);
			$container.append($divProjectDescription);
		}
	}
};

function CellLayout() {}

CellLayout.prototype = {
	translateProjectsToRightExceptDiv: function (index) {
		var $rectangles = $("[id^=rect_]");

		$rectangles.each(function(i) {
			if (i != index) {
				$(this).fadeOut({queue: false, duration: 200});
				$(this).animate(
				{
					left: "+=400px"
				}, 1500);
			}
		});
	},

	addCrossToProjectDiv: function($div) {
		var self = this;
		var $closeButton = $('<div>');
			$closeButton.css({"position": "absolute", "top": "0px", "right": "0px"});
			$closeButton.addClass("glyphicon white glyphicon-remove");
		$div.append($closeButton);

		$closeButton.on("click", function() {
			self.displayProjectsAsCells(_projects);
		});

		$(document).keyup(function(event) {
			if (event.which == 27) {
				self.displayProjectsAsCells(_projects);
				$(document).unbind("keyup");
			}
		});
	},

	goProjectFullView: function($div) {
		var index = $div.attr("id").split("_")[1];
		this.moveProjectDivToTopLeft($div);
		this.createProjectFullView(index);
		this.translateProjectsToRightExceptDiv(index);
	},


	moveProjectDivToTopLeft: function($div){
		var $pgrid = $("#pgrid");
		var _width = $pgrid.css("width");
		var _height = $pgrid.css("height");
		$div.animate({
			top: 0,
			left: 0,
			width: _width,
		}, 1500);
	},

	createProjectFullView: function(index) {
		var cell = cells[index];

		this.addCrossToProjectDiv(cell.rectangle);

		var $status = $("#status_icon_" + index);
		$status.removeClass("glyphicon " + cell.project.getGlyphiconNameFromStatus());
		$status.html("");

		var $statusAsString = $('<div>', { id: "status_" + index, text: cell.project.getStatusAsString()});
		$statusAsString.css({"font-size": "22px", "float" : "left", "position" : "absolute", "top" : "10px", "left" : "5px"});
		cell.rectangle.append($statusAsString);
		$(".glyphicon").css({"font-size": "48px", "top" : "5px", "right" : "5px"});

		var $title = $("#title_" + index);
		$title.css({color: "white", "font-size": "35px", "text-align": "center"});

		var $description = $("#description_" + index);
		$description.text(cell.project.description);
		$description.css({color: "white", "font-size": "18px", "padding-bottom" : "10px"});

		var $technologies =  $("#technologies_" + index);
		$technologies.text("Technologies used: " + cell.project.technologies.toUpperCase().replace(' ', '').split(',').join(" | "));
		$technologies.css({color: "white", "font-size": "22px"});	
	},

	displayProjectsAsCells: function(projects) {
		var self = this;
		if (projects.length === 0) {
			$("#listing").css('display', 'none');
		}
		clearMainDiv();
		cells = [];
		$("#listing").attr("data-layout", 0);
		
		_projects = projects;
		
		var MAX_INDEX = projects.length-1;

		var $grid = $('#pgrid');
		$grid.css({'width': '800px', 'height': '800px'});
		var gridTotalWidth = getWidthAsStringFromCSSProperty($grid.css('width'));
		var gridTotalHeight = getWidthAsStringFromCSSProperty($grid.css('height'));
		
		var posX = 0;
		var posY = 0;


		for (var i=0; i<MAX_INDEX; i+=2) {
			var squareDivLeft = createSquareElement(i, i.toString());
			var squareDivRight = createSquareElement(i+1, (i+1).toString());
			
			var randomWidth = getRandom(300, gridTotalWidth/2);
			var randomHeight = getRandom(300, gridTotalWidth/3);
			
			var firstProjectWidth = randomWidth;
			var secondProjectWidth = gridTotalWidth - randomWidth;
			
			var cellLeft = new Cell();
			var cellRight = new Cell();

			$grid.append(squareDivLeft);
			$grid.append(squareDivRight);
			
			var cellDirectionLeft = getDirection(i, MAX_INDEX);
			var cellDirectionRight= getDirection(i+1, MAX_INDEX);

			var cellColors = getColor();
			cellLeft.applyCSSAndAnimate(i, squareDivLeft, firstProjectWidth, randomHeight, posX, posY, cellDirectionLeft, cellColors[0]);
			cellRight.applyCSSAndAnimate(i+1, squareDivRight, secondProjectWidth, randomHeight, firstProjectWidth, posY, cellDirectionRight, cellColors[1]);
			cellLeft.setLine(i);
			cellRight.setLine(i+1);

			cells = cells.concat([cellLeft, cellRight]);

			posY += randomHeight;
		}

		if (projects.length % 2 == 1) {
			this.displayLastProject(MAX_INDEX, posY, gridTotalWidth, gridTotalHeight, $grid);
		}

		for (i=0; i<cells.length; i++) {
			var cell = cells[i];
			cell.setProject(projects[i]);
			cell.rectangle.on("click", {'cellClicked' : cell }, function(event) {
				event.data.cellClicked.removeMouseListeners();
				self.goProjectFullView($(this));
			});
		}

		var lastCell = cells[cells.length-1];
		var lastTop = lastCell.y + lastCell.height;
		this.updateHeightGridDiv(lastTop);
	},

	updateHeightGridDiv : function(height) {
		$("#pgrid").css("height", height + 20);
	},

	displayLastProject: function(index, posY, gridTotalWidth, gridTotalHeight, $gridDomElement) {
		var square = createSquareElement(index, index.toString());
		var randomWidth = getRandom(300, gridTotalWidth/2);
		var randomHeight = getRandom(300, gridTotalHeight/3);

		var firstProjectWidth = randomWidth;
		var cell = new Cell();
		var cellColor = getColor()[0];
		
		$gridDomElement.append(square);

		cell.applyCSSAndAnimate(index, square, firstProjectWidth, randomHeight, 0, posY, "bottom", cellColor);
		cells.push(cell);
	}
};

function getDirection(i, maxIndex) {
	var DIRECTIONS = ["top", "left", "right", "bottom"];
	var d;

	if (i > maxIndex) throw new Error("Current index cannot be bigger than maxIndex");

	switch (i) {
		case 0:
		case 1:
			d = DIRECTIONS[0];
			break;
		case maxIndex - 1:
		case maxIndex - 2:
			d = DIRECTIONS[3];
			break;
		default:
			if (i % 2 === 0) {
				d = DIRECTIONS[1];
			} else {
				d = DIRECTIONS[2];
			}
			break;
	}

	return d;
}

function getColor() {
	var COLORS = ["#FF7575", "#6094DB", "#FFCB2F", "#AAAAFF", "#1BA63B"];
	var c1;
	var c2;
	do {
		c1 = getRandom(0, COLORS.length-2);
		c2 = getRandom(0, COLORS.length-2);
	}
	while (c1 == c2);

	return [COLORS[c1], COLORS[c2]];
}

function fadeOutCellsAndDisplayProjectsAsList() {
	var $rectangles = $("[id^=rect_]");
	var lastIndex = $rectangles.length - 1;
	var displayListCallback = function() {};
	
	$rectangles.each(function(i, val) {
		if (i === lastIndex) {
			displayListCallback = function() {
				clearMainDiv();
				listLayout.displayProjectsAsList();
			};
		}

		$(this).fadeOut(1000, displayListCallback);
	});
}

function fetchProjects() {
	$.getJSON( "/fetch/projects", function(data) {
		cellsLayout.displayProjectsAsCells(data);
	});
}


function clearMainDiv() {
	$("#pgrid").html("");
}





$(window).load(function() {
	removeCurrentActiveClass();
	cellsLayout = new CellLayout();
	
	$(".projects").addClass("active");

	if (window.CONFIG === undefined || !CONFIG.Test) {
		fetchProjects();
	}

	$("#listing").on("click", function() {
		if ($("#listing").attr("data-layout") === "0") {
			listLayout = new ListLayout();
			listLayout.displayProjectsAsList();
		} else {
			cellsLayout.displayProjectsAsCells(_projects);
		}
	});
});