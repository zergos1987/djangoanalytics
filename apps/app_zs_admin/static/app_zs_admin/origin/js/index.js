// /*tesseract*/
// //Canvas
// const canvas = document.getElementById('c1');
// const c = canvas.getContext('2d');
// //Pixel Dimensions
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;
// c.translate(canvas.width/2, canvas.height/2);
// let rx = 0;
// let ry = 0;
// let rz = 0;
// let rw = 0;
// //Camera Data
// const Camera = {
// 	//Focal Length
// 	focalLength: 35,
// 	wFocalLength: 12,
// 	//Pinhole Location
// 	x: 0, y: 0, z: 0, w: 0,
// 	//Camera Rotation
// 	rotX: 0, rotY: 0, rotZ: 0
// };
// Camera.z = -(Camera.focalLength**2);
// Camera.w = -(Camera.wFocalLength**2);
// //Vertex Object
// class Vertex {
// 	constructor(x, y, z, w) {
// 		this.loc = [x/Camera.focalLength, y/Camera.focalLength, z/Camera.focalLength, w/Camera.focalLength];
// 		this.ploc = [];
// 	}
// 	//3D Rotation Transformation
// 	rotate(xr, yr, zr, wr) {
// 		//4D Rotation on YW Axis
// 		let yy = this.loc[1];
// 		this.loc[1] = yy*Math.cos(wr)-this.loc[3]*Math.sin(wr);
// 		this.loc[3] = yy*Math.sin(wr)+this.loc[3]*Math.cos(wr);
// 		//Constants
// 		let x = this.loc[0];
// 		let y = this.loc[1];
// 		let z = this.loc[2];
// 		//Rotation Data
// 		let sx = Math.sin(xr);
// 		let sy = Math.sin(yr);
// 		let sz = Math.sin(zr);
// 		let cx = Math.cos(xr);
// 		let cy = Math.cos(yr);
// 		let cz = Math.cos(zr);
// 		//Repeating Parts of Equation
// 		let eq1 = sz*y+cz*x;
// 		let eq2 = cz*y-sz*x;
// 		let eq3 = cy*z+sy*eq1;
// 		//Applying Transformations
// 		this.loc[0] = cy*eq1-sy*z;
// 		this.loc[1] = sx*eq3+cx*eq2;
// 		this.loc[2] = cx*eq3-sx*eq2;
// 	}
// 	//Projected 2D Coordinates
// 	project() {
// 		//Projects 4D to 3D
// 		this.loc[3] -= Camera.w/Camera.wFocalLength;
// 		this.loc[0] = -this.loc[0]/this.loc[3]*Camera.wFocalLength;
// 		this.loc[1] = -this.loc[1]/this.loc[3]*Camera.wFocalLength;
// 		this.loc[2] = -this.loc[2]/this.loc[3]*Camera.wFocalLength;
// 		//Camera Location
// 		let x = this.loc[0]-Camera.x/Camera.focalLength;
// 		let y = this.loc[1]-Camera.y/Camera.focalLength;
// 		let z = this.loc[2]-Camera.z/Camera.focalLength;
// 		//Camera Rotation
// 		let sx = Math.sin(Camera.rotX);
// 		let sy = Math.sin(Camera.rotY);
// 		let sz = Math.sin(Camera.rotZ);
// 		let cx = Math.cos(Camera.rotX);
// 		let cy = Math.cos(Camera.rotY);
// 		let cz = Math.cos(Camera.rotZ);
// 		//Repeating Parts of Equation
// 		let eq1 = sz*y+cz*x;
// 		let eq2 = cz*y-sz*x;
// 		let eq3 = cy*z+sy*eq1;
// 		//Camera Transformations
// 		let dx = cy*eq1-sy*z;
// 		let dy = sx*eq3+cx*eq2;
// 		let dz = cx*eq3-sx*eq2;
// 		//Projection
// 		this.ploc = [Camera.focalLength/dz*dx*Camera.focalLength, Camera.focalLength/dz*dy*Camera.focalLength];
// 	}
// }
// //Face Object
// class Face {
// 	constructor(v1, v2, v3, v4, noCull) {
// 		this.vertices = [v1, v2, v3, v4];
// 		if (noCull == true) this.noCull = noCull;
// 	}
// 	show() {
// 		//Drawing Face
// 		c.beginPath();
// 		c.moveTo(this.vertices[0].ploc[0], this.vertices[0].ploc[1]);
// 		for (let i = 1; i < this.vertices.length; i++) c.lineTo(this.vertices[i].ploc[0], this.vertices[i].ploc[1]);
// 		c.closePath();
// 		c.stroke();
// 	}
// }
// function draw() {
// 	requestAnimationFrame(draw);
// 	c.clearRect(-canvas.width/2, -canvas.height/2, canvas.width, canvas.height);
// 	ry = (ry-0.012)%(Math.PI*2);
// 	rw = (rw-0.01)%(Math.PI*2);
// 	let faces = [];
// 	let w = 300;
// 	//Vertices
// 	let v = [];
// 	v[0] = new Vertex(-w/2, w/2, -w/2, w/2);
// 	v[1] = new Vertex(w/2, w/2, -w/2, w/2);
// 	v[2] = new Vertex(w/2, w/2, w/2, w/2);
// 	v[3] = new Vertex(-w/2, w/2, w/2, w/2);
// 	v[4] = new Vertex(-w/2, -w/2, -w/2, w/2);
// 	v[5] = new Vertex(w/2, -w/2, -w/2, w/2);
// 	v[6] = new Vertex(w/2, -w/2, w/2, w/2);
// 	v[7] = new Vertex(-w/2, -w/2, w/2, w/2);
// 	v[8] = new Vertex(-w/2, w/2, -w/2, -w/2);
// 	v[9] = new Vertex(w/2, w/2, -w/2, -w/2);
// 	v[10] = new Vertex(w/2, w/2, w/2, -w/2);
// 	v[11] = new Vertex(-w/2, w/2, w/2, -w/2);
// 	v[12] = new Vertex(-w/2, -w/2, -w/2, -w/2);
// 	v[13] = new Vertex(w/2, -w/2, -w/2, -w/2);
// 	v[14] = new Vertex(w/2, -w/2, w/2, -w/2);
// 	v[15] = new Vertex(-w/2, -w/2, w/2, -w/2);
// 	//Rotating and Projecting vertices
// 	for (let i = 0; i < v.length; i++) {
// 		//If Rotation is Needed
// 		if (Math.abs(rx)+Math.abs(ry)+Math.abs(rz)+Math.abs(rw) > 0) v[i].rotate(rx, ry, rz, rw);
// 		v[i].project();
// 	}
// 	//Faces
// 	faces.push(new Face(v[0], v[1], v[2], v[3]));
// 	faces.push(new Face(v[4], v[7], v[6], v[5]));
// 	faces.push(new Face(v[0], v[4], v[5], v[1]));
// 	faces.push(new Face(v[2], v[6], v[7], v[3]));
// 	faces.push(new Face(v[8], v[9], v[10], v[11]));
// 	faces.push(new Face(v[12], v[15], v[14], v[13]));
// 	faces.push(new Face(v[8], v[12], v[13], v[9]));
// 	faces.push(new Face(v[10], v[14], v[15], v[11]));
// 	faces.push(new Face(v[0], v[1], v[9], v[8]));
// 	faces.push(new Face(v[2], v[3], v[11], v[10]));
// 	faces.push(new Face(v[4], v[7], v[15], v[12]));
// 	faces.push(new Face(v[6], v[5], v[13], v[14]));
// 	for (let i = 0; i < faces.length; i++) faces[i].show();
// }
// draw();




// black hole background
// blackhole('#blackhole');



// function blackhole(element) {
// 	var h = $(element).height(),
// 	    w = $(element).width(),
// 	    cw = w,
// 	    ch = h,
// 	    maxorbit = 255, // distance from center
// 	    centery = ch/2,
// 	    centerx = cw/2;

// 	var startTime = new Date().getTime();
// 	var currentTime = 0;

// 	var stars = [],
// 	    collapse = false, // if hovered
// 	    expanse = false; // if clicked

// 	var canvas = $('<canvas/>').attr({width: cw, height: ch}).appendTo(element),
// 	    context = canvas.get(0).getContext("2d");

// 	context.globalCompositeOperation = "multiply";

// 	function setDPI(canvas, dpi) {
// 		// Set up CSS size if it's not set up already
// 		if (!canvas.get(0).style.width)
// 			canvas.get(0).style.width = canvas.get(0).width + 'px';
// 		if (!canvas.get(0).style.height)
// 			canvas.get(0).style.height = canvas.get(0).height + 'px';

// 		var scaleFactor = dpi / 96;
// 		canvas.get(0).width = Math.ceil(canvas.get(0).width * scaleFactor);
// 		canvas.get(0).height = Math.ceil(canvas.get(0).height * scaleFactor);
// 		var ctx = canvas.get(0).getContext('2d');
// 		ctx.scale(scaleFactor, scaleFactor);
// 	}

// 	function rotate(cx, cy, x, y, angle) {
// 		var radians = angle,
// 		    cos = Math.cos(radians),
// 		    sin = Math.sin(radians),
// 		    nx = (cos * (x - cx)) + (sin * (y - cy)) + cx,
// 		    ny = (cos * (y - cy)) - (sin * (x - cx)) + cy;
// 		return [nx, ny];
// 	}

// 	setDPI(canvas, 192);

// 	var star = function(){

// 		// Get a weighted random number, so that the majority of stars will form in the center of the orbit
// 		var rands = [];
// 		rands.push(Math.random() * (maxorbit/2) + 1);
// 		rands.push(Math.random() * (maxorbit/2) + maxorbit);

// 		this.orbital = (rands.reduce(function(p, c) {
// 			return p + c;
// 		}, 0) / rands.length);
// 		// Done getting that random number, it's stored in this.orbital

// 		this.x = centerx; // All of these stars are at the center x position at all times
// 		this.y = centery + this.orbital; // Set Y position starting at the center y + the position in the orbit

// 		this.yOrigin = centery + this.orbital;  // this is used to track the particles origin

// 		this.speed = (Math.floor(Math.random() * 2.5) + 1.5)*Math.PI/180; // The rate at which this star will orbit
// 		this.rotation = 0; // current Rotation
// 		this.startRotation = (Math.floor(Math.random() * 360) + 1)*Math.PI/180; // Starting rotation.  If not random, all stars will be generated in a single line.  

// 		this.id = stars.length;  // This will be used when expansion takes place.

// 		this.collapseBonus = this.orbital - (maxorbit * 0.7); // This "bonus" is used to randomly place some stars outside of the blackhole on hover
// 		if(this.collapseBonus < 0){ // if the collapse "bonus" is negative
// 			this.collapseBonus = 0; // set it to 0, this way no stars will go inside the blackhole
// 		}

// 		stars.push(this);
// 		this.color = 'rgba(255,255,255,'+ (1 - ((this.orbital) / 255)) +')'; // Color the star white, but make it more transparent the further out it is generated

// 		this.hoverPos = centery + (maxorbit/2) + this.collapseBonus;  // Where the star will go on hover of the blackhole
// 		this.expansePos = centery + (this.id%100)*-10 + (Math.floor(Math.random() * 20) + 1); // Where the star will go when expansion takes place


// 		this.prevR = this.startRotation;
// 		this.prevX = this.x;
// 		this.prevY = this.y;

// 		// The reason why I have yOrigin, hoverPos and expansePos is so that I don't have to do math on each animation frame.  Trying to reduce lag.
// 	}
// 	star.prototype.draw = function(){
// 		// the stars are not actually moving on the X axis in my code.  I'm simply rotating the canvas context for each star individually so that they all get rotated with the use of less complex math in each frame.



// 		if(!expanse){
// 			this.rotation = this.startRotation + (currentTime * this.speed);
// 			if(!collapse){ // not hovered
// 				if(this.y > this.yOrigin){
// 					this.y-= 2.5;
// 				}
// 				if(this.y < this.yOrigin-4){
// 					this.y+= (this.yOrigin - this.y) / 10;
// 				}
// 			} else { // on hover
// 				this.trail = 1;
// 				if(this.y > this.hoverPos){
// 					this.y-= (this.hoverPos - this.y) / -5;
// 				}
// 				if(this.y < this.hoverPos-4){
// 					this.y+= 2.5;
// 				}
// 			}
// 		} else {
// 			this.rotation = this.startRotation + (currentTime * (this.speed / 2));
// 			if(this.y > this.expansePos){
// 				this.y-= Math.floor(this.expansePos - this.y) / -140;
// 			}
// 		}

// 		context.save();
// 		context.fillStyle = this.color;
// 		context.strokeStyle = this.color;
// 		context.beginPath();
// 		var oldPos = rotate(centerx,centery,this.prevX,this.prevY,-this.prevR);
// 		context.moveTo(oldPos[0],oldPos[1]);
// 		context.translate(centerx, centery);
// 		context.rotate(this.rotation);
// 		context.translate(-centerx, -centery);
// 		context.lineTo(this.x,this.y);
// 		context.stroke();
// 		context.restore();


// 		this.prevR = this.rotation;
// 		this.prevX = this.x;
// 		this.prevY = this.y;
// 	}


// 	$('.centerHover').on('click',function(){
// 		collapse = false;
// 		expanse = true;

// 		$(this).addClass('open');
// 		$('.fullpage').addClass('open');
// 		setTimeout(function(){
// 			$('.header .welcome').removeClass('gone');
// 		}, 500);
// 	});
// 	$('.centerHover').on('mouseover',function(){
// 		if(expanse == false){
// 			collapse = true;
// 		}
// 	});
// 	$('.centerHover').on('mouseout',function(){
// 		if(expanse == false){
// 			collapse = false;
// 		}
// 	});

// 	window.requestFrame = (function(){
// 		return  window.requestAnimationFrame       ||
// 			window.webkitRequestAnimationFrame ||
// 			window.mozRequestAnimationFrame    ||
// 			function( callback ){
// 			window.setTimeout(callback, 1000 / 60);
// 		};
// 	})();

// 	function loop(){
// 		var now = new Date().getTime();
// 		currentTime = (now - startTime) / 50;

// 		context.fillStyle = 'rgba(25,25,25,0.2)'; // somewhat clear the context, this way there will be trails behind the stars 
// 		context.fillRect(0, 0, cw, ch);

// 		for(var i = 0; i < stars.length; i++){  // For each star
// 			if(stars[i] != stars){
// 				stars[i].draw(); // Draw it
// 			}
// 		}

// 		requestFrame(loop);
// 	}

// 	function init(time){
// 		context.fillStyle = 'rgba(25,25,25,1)';  // Initial clear of the canvas, to avoid an issue where it all gets too dark
// 		context.fillRect(0, 0, cw, ch);
// 		for(var i = 0; i < 2500; i++){  // create 2500 stars
// 			new star();
// 		}
// 		loop();
// 	}
// 	init();
// }