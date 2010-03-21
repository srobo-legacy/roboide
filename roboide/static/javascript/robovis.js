function RoboVis() {
	//hold the tab object
	this.tab = null;

	//hold signals for the page
	this._signals = new Array();

	//hold status message for the page
	this._prompt = null;

	//hold blob list
	this._blobs = null;
}

/* *****	Initialization code	***** */
RoboVis.prototype.init = function() {
	if(!this._inited) {
		logDebug("RoboVis: Initializing");

		/* Initialize a new tab for RoboVis - Do this only once */
		this.tab = new Tab( "RoboVis" );
		connect( this.tab, "onfocus", bind( this._onfocus, this ) );
		connect( this.tab, "onblur", bind( this._onblur, this ) );
		connect( this.tab, "onclickclose", bind( this._close, this ) );
		tabbar.add_tab( this.tab );

		/* Initialise indiviual page elements */
		this.getBlobs();
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


var bloblist = [
 {width:40, height:30, x:27, y:60, colour: 'red'},
 {width:23, height:30, x:10, y:10, colour: 'blue'},
 {width:15, height:12, x:70, y:70, colour: 'red'}
];


/* *****	Blob list fetching Code	***** */
RoboVis.prototype.getBlobs = function() {
	log("RoboVis: Retrieving blob list");

	this.blobs = bloblist;
}
/* *****	End Student blog feed listing code	***** */

/* *****	Blob drawing code	***** */
RoboVis.prototype.Draw = function() {
	replaceChildNodes('robovis-blobs-box');
	var scale = 1;
	for( var i in this.blobs ) {
		var blob = this.blobs[i];
		var l = blob.x * scale;
		var t = blob.y * scale;
		var h = blob.height * scale;
		var w = blob.width * scale;
		var box = DIV({'style': 'left:'+l+'px; top:'+t+'px; height:'+h+'px; width:'+w+'px; border-color:'+blob.colour+';'});
		appendChildNodes('robovis-blobs-box', box);
	}
}
/* *****	End Blob drawing code	***** */
