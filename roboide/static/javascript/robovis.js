function RoboVis() {
	//hold the tab object
	this.tab = null;

	//hold signals for the page
	this._signals = new Array();

	//hold status message for the page
	this._prompt = null;

	//hold the number of frames
	this._frameCount = null;

	//hold the frames
	this._frames = null;

	//hold the id of the currently selected frame
	this._chosenFrame = null;

	//hold blob list for the currently selected frame
	this._blobs = null;
}

/* *****	Initialization code	***** */
RoboVis.prototype.init = function() {
	if(!this._inited) {
		logDebug("RoboVis: Initializing");

		/* Initialize a new tab for RoboVis - Do this only once */
		this.tab = new Tab( "RoboVis" );
		this._signals.push(connect( this.tab, "onfocus", bind( this._onfocus, this ) ));
		this._signals.push(connect( this.tab, "onblur", bind( this._onblur, this ) ));
		this._signals.push(connect( this.tab, "onclickclose", bind( this._close, this ) ));
		tabbar.add_tab( this.tab );

		this._signals.push(connect( 'robovis-frame-down', "onclick", bind( this.decrementFrame, this ) ));
		this._signals.push(connect( 'robovis-frame-choice', "onchange", bind( this.chooseFrame, this, -10 ) ));
		this._signals.push(connect( 'robovis-frame-up', "onclick", bind( this.incrementFrame, this ) ));

		this._signals.push(connect( 'robovis-view-blobs', "onclick", bind( this.viewBlobs, this ) ));
		this._signals.push(connect( 'robovis-view-overlay', "onclick", bind( this.viewOverlay, this ) ));
		this._signals.push(connect( 'robovis-view-image', "onclick", bind( this.viewImage, this ) ));

		/* Initialise indiviual page elements */
		this.getBlobs(FRAMELIST);
		this.Draw();

		/* remember that we are initialised */
		this._inited = true;
	}

	/* now switch to it */
	tabbar.switch_to(this.tab);
}
/* *****	End Initialization Code 	***** */

/* *****	Tab events: onfocus, onblur and close	***** */
RoboVis.prototype._onfocus = function() {
	setStyle('robovis-page', {'display':'block'});
}

RoboVis.prototype._onblur = function() {
	/* Clear any prompts */
	if( this._prompt != null ) {
		this._prompt.close();
		this._prompt = null;
	}
	/* hide RoboVis page */
	setStyle('robovis-page', {'display':'none'});
}

RoboVis.prototype._close = function() {
	/* Disconnect all signals */
	for(var i = 0; i < this._signals.length; i++) {
		disconnect(this._signals[i]);
	}
	this._signals = new Array();

	/* Close tab */
	this._onblur();
	this.tab.close();
	this._inited = false;
}
/* *****	End Tab events	***** */


var FRAMELIST = {"count":3,"framelist":{1:[
 {width:40, height:30, x:27, y:60, colour: 'red'},
 {width:23, height:30, x:10, y:10, colour: 'blue'},
 {width:15, height:12, x:70, y:70, colour: 'red'}
],2:[
 {width:6, height:40, x:27, y:60, colour: 'red'},
 {width:19, height:23, x:10, y:10, colour: 'blue'},
 {width:16, height:15, x:70, y:70, colour: 'red'}
],3:[
 {width:42, height:6, x:27, y:60, colour: 'red'},
 {width:12, height:19, x:10, y:10, colour: 'blue'},
 {width:27, height:16, x:70, y:70, colour: 'red'}
]}};


/* *****	Blob list fetching Code	***** */
RoboVis.prototype.getBlobs = function(nodes) {
	log("RoboVis: Retrieving blob list");

	this._frames = nodes.framelist;
	this._frameCount = nodes.count;
	this.chooseFrame(nodes.count);
	$('robovis-frame-count').innerHTML = nodes.count;
}
/* *****	End Student blog feed listing code	***** */

/* *****	View switching code	***** */
RoboVis.prototype.viewBlobs = function() {
	removeElementClass('robovis-blobs-box', 'image');
	removeElementClass('robovis-blobs-box', 'overlay');
	addElementClass('robovis-blobs-box', 'blobs');
}
RoboVis.prototype.viewOverlay = function() {
	removeElementClass('robovis-blobs-box', 'blobs');
	removeElementClass('robovis-blobs-box', 'image');
	addElementClass('robovis-blobs-box', 'overlay');
}
RoboVis.prototype.viewImage = function() {
	removeElementClass('robovis-blobs-box', 'blobs');
	removeElementClass('robovis-blobs-box', 'overlay');
	addElementClass('robovis-blobs-box', 'image');
}
/* *****	End View switching code	***** */

/* *****	Frame switching code	***** */
RoboVis.prototype.incrementFrame = function() {
	this.chooseFrame(this._chosenFrame + 1);
}
RoboVis.prototype.decrementFrame = function() {
	this.chooseFrame(this._chosenFrame - 1);
}
RoboVis.prototype.chooseFrame = function(frame) {
	if(frame == -10)
		frame = $('robovis-frame-choice').value;
	log('RoboVis: choosing frame '+frame);
	this._chosenFrame = Math.max(1, Math.min(this._frameCount, frame));	//limit between 1 and the number of frames
	$('robovis-frame-choice').value = this._chosenFrame;
	if(this._chosenFrame == 1) {
		$('robovis-frame-down').disabled = true;
		$('robovis-frame-up').disabled = false;
	} else if(this._chosenFrame == this._frameCount){
		$('robovis-frame-down').disabled = false;
		$('robovis-frame-up').disabled = true;
	} else {
		$('robovis-frame-down').disabled = false;
		$('robovis-frame-up').disabled = false;
	}
	this._blobs = this._frames[this._chosenFrame];
	this.Draw();
}
/* *****	End Frame switching code	***** */

/* *****	Blob drawing code	***** */
RoboVis.prototype.Draw = function() {
	log('RoboVis: drawing frame '+this._chosenFrame);
	replaceChildNodes('robovis-blobs-box');
	var scale = 1;
	for( var i=0; i<this._blobs.length; i++) {
		var blob = this._blobs[i];
		var l = blob.x * scale;
		var t = blob.y * scale;
		var h = blob.height * scale;
		var w = blob.width * scale;
		var box = DIV({'style': 'left:'+l+'px; top:'+t+'px; height:'+h+'px; width:'+w+'px; border-color:'+blob.colour+'; background-color:'+blob.colour+';',
			'title':'X: '+blob.x+
				'; Y: '+blob.y+
				'; Height: '+blob.height+
				'; Width: '+blob.width+
				'; Mass: '+blob.x * blob.y});
		appendChildNodes('robovis-blobs-box', box);
	}
}
/* *****	End Blob drawing code	***** */
