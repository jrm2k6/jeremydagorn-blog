var cells = [];
var MIN_SIZE = 400;

function getWidthAsStringFromCSSProperty(value) {
	return value.replace("px", "").toString();
}

function createSquareElement(i, _text) {
    return $('<div>', { id: "rect_" + i});
}

function getRandom(minValue, maxValue) {
	var p =  Math.round(Math.random() * (maxValue - minValue + 1)) + minValue;
	return p;
}	

function Cell() {	
	this.init = function(id, x, y, width, height, direction, color) {
		this.id = id
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.direction = direction;
		this.color = color;
	}

	this.applyCSSAndAnimate = function(_id, _rectangle, _width, _height, _left, _top, _direction, _color) {
		this.init(_id, _left, _top, _width, _height, _direction, _color);

		var cssParams = {
			id: _id,
			'background-color': _color,
			color: 'white',
			width: _width,
			height: _height,
			position: 'absolute',
			display: 'none',
		}

		var animParams = {
			opacity: "show",
		}

		var params = this.generateAnimationDirection(_direction);

		$.extend(cssParams, params[0]);
		$.extend(animParams, params[1]);
		_rectangle.css(cssParams).animate(animParams, 1000);
	}

	this.setLine = function(i) {
		if (i == 0) {
			this.line = 1;
		} else {
			this.line = Math.round(i/2);
		}
	}

	this.setProject = function(obj) {
		this.project = new Project();
		this.project.init(obj);

		this.displayProjectInformation();
	}

	this.displayProjectInformation = function() {
		var $rect = $("#rect_"+this.id);
		var statusId = this.project.status;

		var $statusIcon = $('<div>', {id: "status_icon_" + this.id});
		$statusIcon.css({"float": "right"});
		$statusIcon.addClass("glyphicon white " + this.project.getGlyphiconNameFromStatus())

		$rect.append($statusIcon);

		var $title = $('<div>', { id: "title_" + this.id, text: this.project.title});
		var $description = $('<div>', { id: "description_" + this.id, text: this.project.description});
		var $technologies = $('<div>', { id: "technologies_" + this.id, text: this.project.technologies.replace(",", ", ").toUpperCase()});
		
		$description.css({"margin-top" : "10px"});
		$technologies.css({"position" : "absolute", "bottom": "0px"});
		
		$rect.append($title);
		$rect.append($description);
		$rect.append($technologies);
	}

	this.generateAnimationDirection = function(direction) {
		var _cssParams = {};
		var _animParams = {};
		if (direction == "top") {
			_cssParams["top"] = this.y - this.height;
			_cssParams["left"] = this.x;

			_animParams["top"] = this.y;
		} else if (direction == "bottom") {
			_cssParams["top"] = this.y + this.height;
			_cssParams["left"] = this.x;

			_animParams["top"] = this.y;
		} else if (direction == "left") {
			_cssParams["top"] = this.y;
			_cssParams["left"] = this.x - this.width;

			_animParams["left"] = this.x;
		}  else if (direction == "right") {
			_cssParams["top"] = this.y;
			_cssParams["left"] = this.x + this.width;

			_animParams["left"] = this.x;
		}

		return [_cssParams, _animParams];
	}
};


function Project() {
	this.init = function(obj) {
		this.id = obj.id;
		this.title = obj.title;
		this.description = obj.description;
		this.status = obj.status;
		this.technologies = obj.technologies;
	}

	this.getStatusAsString = function() {
		var STATUS = ["DONE", "IN-PROGRESS"];
		var status = this.status-1
		if (this.status !== undefined) {
			if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." 
				 + "Have you referenced your new status in this array?")
			return STATUS[status];
		}
	}

	this.getGlyphiconNameFromStatus = function() {
		var STATUS = ["glyphicon-ok", "glyphicon-pencil"];
		var status = this.status-1
		if (this.status !== undefined) {
			if (status >= STATUS.length) throw new Error("Status id needs to be lower than the length of array STATUS." 
				 + "Have you referenced your new status in this array?")
			return STATUS[status];
		}
	}

	this.getTruncatedDescription = function() {
		if (this.description.length > 150) {
			return this.description.substring(0, 146) + "...";
		} else {
			return this.description;
		}
	}
}


function fetchProjects() {
	$.getJSON( "/fetch/projects", function(data) {
  		generateLayout(data);
	});
}

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
			if (i % 2 == 0) {
				d = DIRECTIONS[1];
			} else {
				d = DIRECTIONS[2];
			}
			break;
	}

	return d;
}

function getColor() {
	var COLORS = ["#0080FF", "#088A29", "#FE2E2E", "#FFBF00"];
	var c1;
	var c2;
	do {
		c1 = getRandom(0, COLORS.length-2);
		c2 = getRandom(0, COLORS.length-2);
	}
	while (c1 == c2);

	return [COLORS[c1], COLORS[c2]];
}

function generateLayoutLastProject(index, posY, gridTotalWidth, gridTotalHeight, $gridDomElement) {
	var square = createSquareElement(index, index.toString());
	var randomWidth = getRandom(MIN_SIZE, gridTotalWidth/2 - MIN_SIZE);
	var randomHeight = getRandom(MIN_SIZE, gridTotalHeight/2 - MIN_SIZE);

	var firstProjectWidth = randomWidth;
	var cell = new Cell();
	var cellColor = getColor()[0];
	
	$gridDomElement.append(square);

	cell.applyCSSAndAnimate(index, square, firstProjectWidth, randomHeight, 0, posY, "bottom", cellColor);
	cells.push(cell);
}

function generateLayout(projects) {
	var MAX_INDEX = projects.length-1;

	var $grid = $('#pgrid');
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
		generateLayoutLastProject(MAX_INDEX, posY, gridTotalWidth, gridTotalHeight, $grid);
	}

	for (var i=0; i<cells.length; i++) {
		cells[i].setProject(projects[i]);
	}
}

function displayProjectsAsList() {
	$("#listing").text("Display as cells layout");
	$("#pgrid").html("");
	for (var i=0; i<cells.length; i++) {
		var project = cells[i].project;
		var $container = $('<div>', { id: "container_project_"+i});
		$container.css({"margin-top": "20px"})
		var $divProjectTitle = $('<div>', { id: "project_title_" + i, text: project.title});
		var $divProjectDescription = $('<div>', {id: "project_description_"+i, text: project.getTruncatedDescription()});
		$divProjectTitle.css({color: "white", "font-size": "20px"});
		$divProjectTitle.attr("data-description", project.description);
		$("#pgrid").append($container);
		$container.append($divProjectTitle);
		$container.append($divProjectDescription);
	}
}

$(window).load(function() {
	if (window.CONFIG === undefined || !CONFIG.Test) {
		fetchProjects();
	}

	$("#listing").on("click", function() {
		displayProjectsAsList();
	})

});