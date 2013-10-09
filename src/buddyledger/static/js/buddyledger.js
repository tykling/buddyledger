// this function shows a row in the add/edit expense table
function showrow(userid) {
	$( '#row'+userid ).show();
	$( '#expensepart-'+userid ).prop("checked", true);
	$( '#buttonp-'+userid ).hide();
	updatecalc();
	
	// find out if all rows are now hidden, hide the whole table if so
	var temp = "allhidden";
	$( ".personp" ).each(function( index ) {
		if( $( this ).css("display") != "none" ) {
			temp = "atleastoneisvisible";
		};
	});
	if(temp == "atleastoneisvisible") {
		$( "#peoplebox" ).show();
	} else {
		$( "#peoplebox" ).hide();
	};
};

// hides a row in the add/edit expense table
function hiderow(userid) {
	$( '#row'+userid ).hide();
	$( '#expensepart-'+userid ).prop("checked", false);
	$( '#buttonp-'+userid ).show();
	updatecalc();
	
	// show the box if it is hidden
	if( $( "#peoplebox" ).css("display") == "none") {
		$( "#peoplebox" ).show();
	};
};


function toggleautoamount(id) {
	// if checkbox is checked...
	if ( $( '#autoamount-'+id ).prop( "checked" ) ) {
		// enable textbox
		document.getElementById("customamount-"+id).className="input-small";
		document.getElementById("customamount-"+id).disabled="";
	} else {
		// disable textbox
		document.getElementById("customamount-"+id).className="uneditable-input input-small";
		document.getElementById("customamount-"+id).disabled="disabled";
	};

	// toggle checkbox
	$( '#autoamount-'+id ).click();
	
	// toggle button visibility
	$( '#customamount-button-'+id ).toggle();
	$( '#autoamount-button-'+id ).toggle();

	// update calculation
	updatecalc();
};

function setMessage(message,type) {
	$( '#messages' ).removeClass().addClass( "alert " + type );
	$( '#messages' ).html("<p>" + message + "</p>");
};

function updatecalc() {
	setMessage("Working...","alert-info")
	
	// check if we have a valid name for this expense
	if(document.getElementById('name').value == '') {
		$( '#controlgroup-name' ).removeClass().addClass( "control-group error" );
		setMessage("Please add a name for this expense!","alert-warning");
		$( '#controlgroup-name' ).focus();
		$( '#peoplediv' ).hide();
		return;        
	};
	
	// check if we have a valid total expense amount in the form
	if(document.getElementById('amount').value == '') {
		$( '#controlgroup-amount' ).removeClass().addClass( "control-group error" );
		setMessage("Please specify a total amount for this expense!","alert-warning");
		$( '#controlgroup-amount' ).focus();
		$( '#peoplediv' ).hide();
		return;            
	}
	if(!$.isNumeric(document.getElementById('amount').value)) {
		$( '#controlgroup-amount' ).removeClass().addClass( "control-group error" );
		setMessage("Invalid expense amount specified!","alert-error");
		$( '#controlgroup-amount' ).focus();
		$( '#peoplediv' ).hide();
		return;
	} else {
		$( '#controlgroup-amount' ).removeClass().addClass( "control-group" );
		$( '#peoplediv' ).show();
	};
	
	// check each of the customamount fields
	var success = true;
	$( "input[name^='person-customamount-']" ).each(function( index ) {
		// find userid from element name
		userid = $(this).attr( "name" ).substring(20);
		// is this user a part of this expense ?
		if (document.getElementById('expensepart-'+userid).checked == true) {
			// remove any error classes on this control group
			$( '#controlgroup-customamount-'+userid ).removeClass().addClass( "control-group" );
			// is autoamount unchecked ?
			if (document.getElementById('autoamount-'+userid).checked == false) {
				// check if anything has been entered in the field
				if ( $( this ).val() == '' ) {
					setMessage("Please specify how much of the expense this user should pay for","alert-warning");
					$( '#controlgroup-customamount-'+userid ).removeClass().addClass( "control-group error" );
					$( '#controlgroup-customamount-'+userid ).focus();
					success = false;
				};
				
				// check if the entered value is numeric
				if ( !$.isNumeric( $( this ).val() ) ) {
					setMessage("Invalid amount specified: " + $(this).val(),"alert-error");
					$( '#controlgroup-customamount-'+userid ).removeClass().addClass( "control-group error" );
					$( '#controlgroup-customamount-'+userid ).focus();
					success = false;
					return;
				};
			};
		};
	});
	if(!success) {
		return;
	};
	
	// find the userids of customamount and autoamount people in this calculation
	autoids = new Array();
	customids = new Array();
	$( "input[name^='person-customamount-']" ).each(function( index ) {
		// find userid from element name
		userid = $(this).attr( "name" ).substring(20);
		if (document.getElementById('expensepart-'+userid).checked == true) {
			if (document.getElementById('autoamount-'+userid).checked == true) {
				autoids.push(userid);
			} else {
				customids.push(userid);
			};
		};
	});
	
	if(customids.length + autoids.length == 0) {
		setMessage("No people selected","alert-warning");
		return;
	};
	
	// arrays autoids and customids now contain the userid's for the calculation,
	// first do some sanity checking to check that the customamounts are less than the total expense amount
	customtotal = 0;
	if (customids.length > 0) {
		for (var i=0;i<customids.length;i++) {
			customtotal = customtotal + Number($( "#customamount-" + customids[i] ).val());
		};
	};

	// if the total customamount exceeds the amount...
	if (customtotal > Number(document.getElementById('amount').value)) {
		// mark the expense amount and the customamount fields with red to indicate where the problem is
		document.getElementById('controlgroup-amount').className="control-group error";
		$( "input[name^='person-customamount-']" ).each(function( index ) {
			// only mark fields with non-zero value in red
			if(this.value != '' && this.value != 0) {
				// find userid from element name
				userid = $(this).attr( "name" ).substring(20);
				// mark this field red (class goes on the controlgroup not the field)
				document.getElementById('controlgroup-customamount-'+userid).className="control-group error";
			};
		});
		setMessage("Custom amounts total exceeds expense amount","alert-error");
		return;
	};
	
	// now find the amount that remains after custom amounts have been substracted,
	// divide by the number of autoamount people, and add it to their amount textboxes
	divamount = Number((document.getElementById('amount').value-customtotal)/autoids.length);
	
	$( "input[name^='person-customamount-']" ).each(function( index ) {
		// find userid from element name
		userid = $(this).attr( "name" ).substring(20);
		if (document.getElementById('expensepart-'+userid).checked == true) {
			if (document.getElementById('autoamount-'+userid).checked == true) {
				document.getElementById('customamount-'+userid).value = divamount.toFixed(2);
			};
		};
	});
	
	// find the total calculated amount (autoamount)
	autototal = 0;
	if (autoids.length > 0) {
		for (var i=0;i<autoids.length;i++) {
			autototal = autototal + divamount;
		};
	};
	
	// sanity: check if the total amount owed equal the total expense amount
	totalowed = Number(autototal+customtotal).toFixed(2)
	if(totalowed != Number(document.getElementById('amount').value).toFixed(2)) {
		setMessage("Error: The total amount owed (" + totalowed + ") should equal the expense amount (" + document.getElementById('amount').value + ")!","alert-error");
		$( '#controlgroup-amount' ).removeClass().addClass( "control-group error" );
		if (customids.length > 0) {
			for (var i=0;i<customids.length;i++) {
				$( "#controlgroup-customamount-" + customids[i] ).removeClass().addClass( "control-group error" );
			};
		};
		return false;
	};
	
	// find the total amount paíd
	totalpaid = 0;
	$( "input[name^='person-paymentamount-']" ).each(function( index ) {
		userid = $(this).attr( "name" ).substring(20);
		if( $( this ).val() != '') {
			if ( !$.isNumeric( $( this ).val() ) ) {
					setMessage("Invalid amount specified: " + $(this).val(),"alert-error");
					$( '#controlgroup-paymentamount-'+userid ).removeClass().addClass( "control-group error" );
					$( '#controlgroup-paymentamount-'+userid ).focus();
					success = false;
					return;
			} else {
				// amount OK, remove any error classes on this field
				totalpaid = totalpaid + Number($( this ).val());
				$( '#controlgroup-paymentamount-'+userid ).removeClass();
			};
		};
	});
	
	if(!success) {
		return;
	};
	
	// check that the total amount paid equals the expense amount
	if(totalpaid.toFixed(2) != Number(document.getElementById('amount').value).toFixed(2)) {
		userid = $(this).attr( "name" ).substring(20);
		$( "input[name^='person-paymentamount-']" ).each(function( index ) {
			$( '#controlgroup-paymentamount-'+userid ).removeClass().addClass( "control-group error" );
		});
		setMessage("Error: Payments do not add up to the expense amount","alert-error");
		return;
	};
	
	if(!success) {
		return;
	};
	
	setMessage("Bueno!","alert-success");
};

$().ready(function(){
	// update calculation on input and change in textfields
	$( "#amount,#name,input[name^='person-customamount-']" ).on('input change',function() {
		updatecalc();
	});        

	// reset form
	$( "input[name^='person-customamount-']" ).each(function( index ) {
		// find userid from element name
		userid = $(this).attr( "name" ).substring(20);
		
		// remove content from textfields
		$( "#customamount-"+userid ).val(0);
		$( "input[name^='person-paymentamount-']" ).val(0);
		
		// remove classes from payment fields
		$( "input[name^='person-paymentamount-']" ).removeClass();
		
		// add uneditable-input and disabled to the customamount textfield
		$( "#customamount-"+userid ).addClass("uneditable-input");
		$( "#customamount-"+userid ).prop( "disabled", true );
		
		// uncheck expensepart
		$( "#expensepart-"+userid ).prop("checked", false);
		$( "#expensepart-" + userid + " + a" ).removeClass("checked");
		
		// check autoamount
		$( "#autoamount-"+userid ).prop("checked", true);
		$( "#autoamount-" + userid + " + a" ).addClass("checked");
		
		// hide and show autoamount buttons
		$( '#customamount-button-'+userid ).show();
		$( '#autoamount-button-'+userid ).hide();
	});

	// initial calculation
	updatecalc();
});
