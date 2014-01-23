var cells = [];
var MIN_SIZE = 100;

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
		console.log("this.height, y", this.height, this.y);
		this.direction = direction;
		this.color = color;
	}

	this.applyCSSAndAnimate = function(_id, _rectangle, _width, _height, _left, _top, _direction, _color) {
		this.square = _rectangle;
		this.init(_id, _left, _top, _width, _height, _direction, _color);

		var cssParams = {
			id: _id,
			'background-color': _color,
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
		this.animParams = animParams;
		_rectangle.css(cssParams);
		.animate(animParams, 1000, function() {
			var $statusText = $("#status_text_"+this.id);
			var widthText = $statusText.css('width');
			var top = this.y + this.height/2 - getWidthAsStringFromCSSProperty(widthText)/4;
			var statusTextCss = {
				'-webkit-transform' : 'rotate(-90deg)', 
				'-moz-transform': 'rotate(-90deg)',
				'display': 'block',
				'position': 'relative',
				'top': top
			}
			
			$statusText.css(statusTextCss);
		});
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
		var $statusDiv = $('<div>', { id: "status_" + this.id});

		var statusDivCss = {
			'background-color' : 'white',
			'color' : this.color,
			'float' : 'right',
			'width' : '30px',
			'height' : this.height,
		}

		var $statusText = $('<div>', {id: "status_text_"+this.id, text: this.project.getStatusAsString(this.project.status)}); 

		$statusDiv.css(statusDivCss);
		$statusDiv.append($statusText);
		$rect.append($statusDiv);

		var widthText = $statusText.css('width');
		var top = this.y + this.height/2 - getWidthAsStringFromCSSProperty(widthText)/4;

		var statusTextCss = {
			'class' : 'status-text',
			'color' : this.color,
			'-webkit-transform' : 'rotate(-90deg)', 
			'-moz-transform': 'rotate(-90deg)',
			'display': 'block',
			'position': 'relative',
			'top': top
		}
		
		$statusText.css(statusTextCss);

		var $title = $('<div>', { id: "title_" + this.id, text: this.project.title});
		var $description = $('<div>', { id: "description_" + this.id, text: this.project.description});
		var $technologies = $('<div>', { id: "technologies_" + this.id, text: this.project.technologies.replace(",", ", ").toUpperCase()});
		
		$description.css({"margin-top" : "10px"});
		$technologies.css({"position" : "absolute", "bottom": "0px"});
		
		$rect.append($title);
		$rect.append($description);
		$rect.append($technologies);
		var that = this
		this.square.animate(this.animParams, 1000, function() {
			var widthText = $statusText.css('width');

			var top = that.y + that.height/2 - getWidthAsStringFromCSSProperty(widthText)/4;
			console.log(this.id, widthText, top);
			var statusTextCss = {
				'-webkit-transform' : 'rotate(-90deg)', 
				'-moz-transform': 'rotate(-90deg)',
				'display': 'block',
				'position': 'relative',
				'top': top
			}
			
			$statusText.css(statusTextCss);
		});
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
	var COLORS = ["cyan", "#0000FF", "green", "orange", "red", "#FFD700", "#FF00FF"];
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
		
		var randomWidth = getRandom(MIN_SIZE, gridTotalWidth/2 - MIN_SIZE);
		var randomHeight = getRandom(MIN_SIZE, gridTotalHeight/2 - MIN_SIZE);
		
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

$(window).load(function() {
	if (window.CONFIG === undefined || !CONFIG.Test) {
		fetchProjects();
	}
});