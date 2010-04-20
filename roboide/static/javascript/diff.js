function DiffPage() {
	//hold the tab object
	this.tab = null;

	//hold signals for the page
	this._signals = new Array();

	//hold status message for the page
	this._prompt = null;

	//store inited state
	this._inited = false;
}

/* *****	Initialization code	***** */
DiffPage.prototype.init = function() {
	if(!this._inited) {
		logDebug("Diff: Initializing");

		/* Initialize a new tab for Diff - Do this only once */
		this.tab = new Tab( "File Difference" );
		this._signals.push(connect( this.tab, "onfocus", bind( this._onfocus, this ) ));
		this._signals.push(connect( this.tab, "onblur", bind( this._onblur, this ) ));
		this._signals.push(connect( this.tab, "onclickclose", bind( this._close, this ) ));
		tabbar.add_tab( this.tab );

		/* remember that we are initialised */
		this._inited = true;
	}

	/* now switch to it */
	tabbar.switch_to(this.tab);
}
/* *****	End Initialization Code 	***** */

/* *****	Tab events: onfocus, onblur and close	***** */
DiffPage.prototype._onfocus = function() {
	showElement('diff-page');
}

DiffPage.prototype._onblur = function() {
	/* Clear any prompts */
	if( this._prompt != null ) {
		this._prompt.close();
		this._prompt = null;
	}
	/* hide Diff page */
	hideElement('diff-page');
}

DiffPage.prototype._close = function() {
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

/* *****	Team editing Code	***** */
DiffPage.prototype._recieveDiff = function(nodes) {
	$('diff-page-diff').innerHTML = nodes.diff;
	this.init();
}

DiffPage.prototype._errDiff = function(nodes) {
	return;
}

DiffPage.prototype.diff = function(file, rev) {
	var d = loadJSONDoc("./diff", {
				team: team,
				file: file,
				rev: rev
			});

	d.addCallback( bind( this._recieveDiff, this) );
	d.addErrback( bind( this._errDiff, this) );
}
/* *****	End Diff loading Code 	***** */
