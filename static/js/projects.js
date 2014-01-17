var cells = [];

function getWidthAsStringFromCSSProperty(value) {
	return value.replace("px", "").toString();
}

function createSquareElement(i, _text) {
    return $('<div>', { id: "rect_" + i, text: _text});
}

function getRandom(minValue, maxValue) {
	var p =  Math.round(Math.random() * (maxValue - minValue + 1)) + minValue;
	return p;
}	

function Cell() {	
	this.init = function(id, x, y, width, height, direction) {
		this.id = id
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.direction = direction;
	}

	this.applyCSSAndAnimate = function(_id, _rectangle, _width, _height, _left, _top, _direction) {
		
		this.init(_id, _left, _top, _width, _height, _direction);

		var cssParams = {
			id: _id,
			'background-color': 'gray',
			width: _width,
			height: _height,
			position: 'absolute',
			border: '1px green solid',
			display: 'none',
		}


		var animParams = {
			opacity: "show",
		}

		var params = generateAnimationDirection(_direction);

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

	this.generateAnimationDirection = function(direction) {
	var generateAnimationDirection = function(direction) {
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
}


function fetchProjects() {
	$.getJSON( "/fetch/projects", function(data) {
  		generateLayout(data);
	});
}

function getDirection(i, maxIndex) {
	var DIRECTIONS = ["top", "left", "right", "bottom"];
	var d;
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

function generateLayout(projects) {
	var WIDTH=100;
	var HEIGTH=100;
	var MIN_SIZE=100;
	var MAX_INDEX = projects.length-1;

	var grid = $('#pgrid');
	var gridTotalWidth = getWidthAsStringFromCSSProperty(grid.css('width'));
	var gridTotalHeight = getWidthAsStringFromCSSProperty(grid.css('height'));
	
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

		grid.append(squareDivLeft);
		grid.append(squareDivRight);
		
		var cellDirectionLeft = getDirection(i, MAX_INDEX);
		var cellDirectionRight= getDirection(i+1, MAX_INDEX);

		cellLeft.applyCSSAndAnimate(i, squareDivLeft, firstProjectWidth, randomHeight, posX, posY, cellDirectionLeft);
		cellRight.applyCSSAndAnimate(i+1, squareDivRight, secondProjectWidth, randomHeight, firstProjectWidth, posY, cellDirectionRight);
		cellLeft.setLine(i);
		cellRight.setLine(i+1);

		cells = cells.concat([cellLeft, cellRight]);


		posY += randomHeight;
	}
}

$(window).load(function() {
	fetchProjects();
});