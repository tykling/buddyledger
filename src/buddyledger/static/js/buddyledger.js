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


// configures a row for edit expense page
function configrow(id, autoamount, haspaid, shouldpay, expensepart) {
    if(autoamount=='True') {
        $( '#autoamount-'+id ).prop('checked', true);
        $( '#customamount-'+id).removeClass().addClass("input-small uneditable-input");
        $( '#customamount-'+id).prop('disabled', true);
        $( '#customamount-button-'+id ).show();
        $( '#autoamount-button-'+id ).hide();
        $( '#customamount-'+id ).val(shouldpay);
        $( '#paymentamount-'+id ).val(haspaid);
    } else {
        $( '#autoamount-'+id ).prop('checked', false);
        $( '#customamount-'+id).removeClass().addClass("input-small");
        $( '#customamount-'+id).prop('disabled', false);
        $( '#customamount-button-'+id ).hide();
        $( '#autoamount-button-'+id ).show();
        $( '#customamount-'+id ).val(shouldpay);
        $( '#paymentamount-'+id ).val(haspaid);
    };
    $( '#expensepart-'+id ).prop('checked', expensepart);
};


function toggleautoamount(id) {
    // if checkbox is checked...
    if ( $( '#autoamount-'+id ).prop( "checked" ) ) {
        // enable textbox
        document.getElementById("customamount-"+id).className="input-small";
        document.getElementById("customamount-"+id).disabled="";
        // show/hide buttons
        $( '#customamount-button-'+id ).hide();
        $( '#autoamount-button-'+id ).show();
    } else {
        // disable textbox
        document.getElementById("customamount-"+id).className="uneditable-input input-small";
        document.getElementById("customamount-"+id).disabled="disabled";
        // show/hide buttons
        $( '#customamount-button-'+id ).show();
        $( '#autoamount-button-'+id ).hide();
    };

    // toggle checkbox
    $( '#autoamount-'+id ).click();

    // update calculation
    updatecalc();
};


function setMessage(message,type) {
    $( '#messages' ).removeClass().addClass( "alert " + type );
    $( '#messages' ).html("<p>" + message + "</p>");
};


function updatecalc() {
    setMessage("Working...","alert-info")
    $( "#submit" ).prop( "disabled", true );
    
    // check if we have a valid name for this expense
    if(document.getElementById('name').value == '') {
        $( '#controlgroup-name' ).removeClass().addClass( "control-group warning" );
        setMessage("Please add a name for this expense!","alert-warning");
        $( '#controlgroup-name' ).focus();
        $( '#peoplediv' ).hide();
        return;        
    };
    
    // check if we have a valid total expense amount in the form
    if(document.getElementById('amount').value == '') {
        $( '#controlgroup-amount' ).removeClass().addClass( "control-group warning" );
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
        // clear classes
        $( '#controlgroup-amount' ).removeClass().addClass( "control-group" );
        // show peoplediv
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
        setMessage("Custom amounts total (" + customtotal + ") exceeds expense amount (" + Number(document.getElementById('amount').value) + ")","alert-error");
        return;
    };

    // now find the amount that remains after custom amounts have been substracted,
    // divide by the number of autoamount people, and add it to their amount textboxes
    divamount = Number((document.getElementById('amount').value-customtotal)/autoids.length).toFixed(2);
    remainder = Number(Number(document.getElementById('amount').value-customtotal)-(divamount*autoids.length)).toFixed(2);
    $( "input[name^='person-customamount-']" ).each(function( index ) {
        // find userid from element name
        userid = $(this).attr( "name" ).substring(20);
        if (document.getElementById('expensepart-'+userid).checked == true) {
            if (document.getElementById('autoamount-'+userid).checked == true) {
                document.getElementById('customamount-'+userid).value = Number(divamount)+Number(remainder);
                remainder = 0;
            };
        };
    });
    
    // find the total calculated amount (autoamount)
    totalowed = 0
    $( "input[name^='person-customamount-']" ).each(function( index ) {
        userid = $(this).attr( "name" ).substring(20);
        if (document.getElementById('expensepart-'+userid).checked == true) {
            totalowed = totalowed + Number(this.value);
        };
    });
    
    // sanity: check if the total amount owed equal the total expense amount
    if(totalowed.toFixed(2) != Number(document.getElementById('amount').value)) {
        setMessage("Error: The total amount owed (" + totalowed + ") should equal the expense amount (" + document.getElementById('amount').value + ")!","alert-error");
        $( '#controlgroup-amount' ).removeClass().addClass( "control-group error" );
        if (customids.length > 0) {
            for (var i=0;i<customids.length;i++) {
                $( "#controlgroup-customamount-" + customids[i] ).removeClass().addClass( "control-group error" );
            };
        };
        return false;
    };
    
    // reset classes on payment fields
    $( "div[id^='controlgroup-paymentamount-']" ).removeClass().addClass( "control-group" );
    
    // find the total amount paíd
    totalpaid = 0;
    $( "input[name^='person-paymentamount-']" ).each(function( index ) {
        userid = $(this).attr( "name" ).substring(21);
        if (document.getElementById('expensepart-'+userid).checked == true) {
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
        };
    });
    
    if(!success) {
        return;
    };
    
    // check that the total amount paid equals the expense amount
    if(totalpaid != Number($( '#amount' ).val())) {
        // give an appropriate message
        if(totalpaid == 0) {
            $( "div[id^='controlgroup-paymentamount-']" ).removeClass().addClass( "control-group warning" );
            setMessage("Please add payments in the 'Amount paid' column to indicate who paid for this expense. The payments must add up to the expense amount: " + document.getElementById('amount').value,"alert-warning");
        } else {
            $( "div[id^='controlgroup-paymentamount-']" ).removeClass().addClass( "control-group error" );
            setMessage("Error: Payments do not add up (" + totalpaid.toFixed(2) + ") to the expense amount (" + Number(document.getElementById('amount').value).toFixed(2) + ")","alert-error");
        };
        return;
    };
    
    if(!success) {
        return;
    };
    
    setMessage("Bueno!","alert-success");
    $( "#submit" ).prop( "disabled", false );
};


function updatecurrency() {
    $( ".currencylabel" ).html($( "#id_currency option:selected" ).text());
};

$().ready(function(){
    if (typeof pagetype === 'undefined') {
        // do nothing
    } else {
        // update calculation on input and change in textfields
        $( "#amount,#name,input[name^='person-customamount-'],input[name^='person-paymentamount-']" ).on('input change',function() {
            updatecalc();
        });

        // update currency labels on input and change
        $( "#id_currency" ).on('input change',function() {
            updatecurrency();
        });

        if(pagetype == "edit_expense") {
            // this is the add/edit expense page...
            updatecurrency();
        } else {
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
        };
    };
});
