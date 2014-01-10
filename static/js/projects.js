var cells = [];

function getWidthAsStringFromCSSProperty(value) {
	return value.replace("px", "").toString();
}

function createSquareElement(i, _text) {
    return $('<div>', { id: "rect_" + i, text: _text});
}

function getRandom(minValue, maxValue) {
	var p =  Math.round(Math.random() * (maxValue - minValue + 1)) + minValue;
	console.log(p);
	return p;
}	

function Cell() {	
	this.init = function(x, y, width, height) {
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
	}

	this.applyCSS = function(rectangle, _width, _height, _left, _top) {
		
		this.init(_left, _top, _width, _top);

		rectangle.css({
			'background-color': 'gray',
			width: _width,
			height: _height,
			position: 'absolute',
			top: _top,
			left: _left,
			border: '1px green solid'
		});
	}

	this.setLine = function(i) {
		if (i ==0) {
			this.line = 1;
		} else {
			this.line = Math.round(i/2);
		}
	}
};


function Project() {
}


function fetchProjects() {
	$.getJSON( "/fetch/projects", function(data) {
  		generateLayout(data);
	});
}

function generateLayout(projects) {
	var WIDTH=200;
	var HEIGTH=200;
	var MIN_SIZE=200;

	var grid = $('#pgrid');
	var gridTotalWidth = getWidthAsStringFromCSSProperty(grid.css('width'));
	var gridTotalHeight = getWidthAsStringFromCSSProperty(grid.css('height'));

	var firstProjectWidth = randomWidth;
	var secondProjectWidth = gridTotalWidth - randomWidth;
	
	var posX = 0;
	var posY = 0;

	 for (var i=0; i<4; i+=2) {
	 	var squareDivLeft = createSquareElement(i, i.toString());
		var squareDivRight = createSquareElement(i+1, i.toString());
		
		var randomWidth = getRandom(MIN_SIZE, gridTotalWidth - MIN_SIZE);
		var randomHeight = getRandom(MIN_SIZE, gridTotalHeight - MIN_SIZE);
		
		var firstProjectWidth = randomWidth;
		var secondProjectWidth = gridTotalWidth - randomWidth;
		var cellLeft = new Cell();
		cellLeft.applyCSS(squareDivLeft, firstProjectWidth, randomHeight, posX, posY);
		var cellRight = new Cell();
		cellRight.applyCSS(squareDivRight, secondProjectWidth, randomHeight, firstProjectWidth, posY);
		cellLeft.setLine(i);
		cellRight.setLine(i+1);

		cells = cells.concat([cellLeft, cellRight]);
		
		grid.append(squareDivLeft);
		grid.append(squareDivRight);

		posY += randomHeight;
	}
}

$(window).load(function() {
	fetchProjects();
});