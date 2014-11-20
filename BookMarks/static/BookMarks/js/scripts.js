/* Wai for document to be ready*/
$(document).ready(function()
{
	/* Submit form */
	$(document).on('submit','form', function( e )
	{
		// define the form that has been submited
		var formClicked = $( this );
		var formAction  = $( this ).attr('action');


		// submit the form for logging in
		if ( formAction == '/accounts/login/' || formAction == '/register/' )
		{
			$(this).submit();
			return;
		}


		$.post( formAction, $(this).serialize() ).done( function( data ) 
		{
			// if it was successful 
			if( data.added )
			{
				// 1UP animation
				$("#loadn").removeClass().addClass('success').html( data.added.msg ).oneUp();
				// find the right table
				if ( $( "#tbl-lists" ).length )
				{
					var tbl  = $( '#tbl-lists' );
					var icon = 'folderIcon';
					var inp  = 'lists';
				} else if ( $( '#tbl-links' ).length )
				{
					var tbl  = $( '#tbl-links' );
					var icon = 'linkIcon';
					var inp  = 'links';
				}

				// Use Hidden object to clone
				// Hide it in order to edit it and animate it
				var clone = $( '.clone-me' ).clone().hide();

				// select the class of the cloned element
				cloneClass = $( '.clone-me' ).attr('class').split(' ')[1];

				// add the record id
				clone.attr('id', 'record_' + data.added.id );

				// make sure the class cycles
				if( cloneClass == 'tbl-row-light' )
				{
					clone.attr( 'class', 'tbl-row-dark' );
					$( '.clone-me' ).removeClass('tbl-row-light').addClass('tbl-row-dark');
				}else { 
					clone.attr( 'class', 'tbl-row-light' )
					$( '.clone-me' ).removeClass('tbl-row-dark').addClass('tbl-row-light');
				}
				// change the link
				clone.find('a').attr( "href", data.added.url ).text( data.added.name );

				// select the right icon
				clone.find('.icon').addClass( icon );

				// add the right input 
				clone.find('input[type="checkbox"]').attr( 'name', inp + '[]' ).attr( 'value', data.added.id );

				// add the element to the list
				tbl.append( clone );

				// slide down like a boss
				clone.slideDown('slow');

				// clear the form
				formClicked.each(function(){
					$('span[class*="error_"').fadeOut( 500, function() 
						{ 
							$(this).empty();
							$(this).show();
						});
				    this.reset();
				});

			// else if an Exception was thrown
			} else if( data.error ) {
				// 1UP animation
				$("#upDelete").removeClass().addClass('error').html( 'Error: ' + data.error ).oneUp();
			// else if the form was rejected.
			} else if( data.deleted ) {
				// 1UP animation
				$("#upDelete").removeClass().addClass('success').html( data.deleted.msg ).oneUp();
				$.each( data.deleted.items, function( i, record ){
					$( '#record_' + record ).fadeOut('Slow', function() {
						$(this).remove();
					});
				});
			} else {
				// 1UP animation
				$("#loadn").removeClass().addClass('error').html( 'Error!' ).oneUp();
				$.each(data, function(i, item) {
					formClicked.find('span[class="error_' + i + '"]').html( item, 500 );
				})
			}

		}) // End .done ( function (data ) )
	  	.fail( function(){ alert( 'There was a problem' ); });


	// Prevent the form from being submited.  
	return false;
	}); // End on submit.
});