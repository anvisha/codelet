$.widget( "ui.timespinner", $.ui.spinner, {
    options: {
      // seconds
      step: 60 * 1000,
      // hours
      page: 60
    },
 
    _parse: function( value ) {
      if ( typeof value === "string" ) {
        // already a timestamp
        if ( Number( value ) == value ) {
          return Number( value );
        }
        return +Globalize.parseDate( value );
      }
      return value;
    },
 
    _format: function( value ) {
      return Globalize.format( new Date(value), "t" );
    }
  });
 
  $(function() {
	console.log("got here")
    $( "#remind_tod" ).timespinner();
 
    $( "#culture" ).change(function() {
      var current = $( "#remind_tod" ).timespinner( "value" );
      Globalize.culture( $(this).val() );
      $( "#remind_tod" ).timespinner( "value", current );
    });
  });