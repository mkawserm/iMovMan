$.event.special.hoverintent = {
		setup: function() {
			$( this ).bind( "mouseover", jQuery.event.special.hoverintent.handler );
		},
		teardown: function() {
			$( this ).unbind( "mouseover", jQuery.event.special.hoverintent.handler );
		},
		handler: function( event ) {
			var currentX, currentY, timeout,
				args = arguments,
				target = $( event.target ),
				previousX = event.pageX,
				previousY = event.pageY;

			function track( event ) {
				currentX = event.pageX;
				currentY = event.pageY;
			};

			function clear() {
				target
					.unbind( "mousemove", track )
					.unbind( "mouseout", clear );
				clearTimeout( timeout );
			}

			function handler() {
				var prop,
					orig = event;

				if ( ( Math.abs( previousX - currentX ) +
						Math.abs( previousY - currentY ) ) < 7 ) {
					clear();

					event = $.Event( "hoverintent" );
					for ( prop in orig ) {
						if ( !( prop in event ) ) {
							event[ prop ] = orig[ prop ];
						}
					}
					// Prevent accessing the original event since the new event
					// is fired asynchronously and the old event is no longer
					// usable (#6028)
					delete event.originalEvent;

					target.trigger( event );
				} else {
					previousX = currentX;
					previousY = currentY;
					timeout = setTimeout( handler, 100 );
				}
			}

			timeout = setTimeout( handler, 100 );
			target.bind({
				mousemove: track,
				mouseout: clear
			});
		}
};

/**********************************************/
















function on_movie_context_menu_build()
{


function get_data(data)
{


//sort json data
new_data={};
key_array=Array();

for (var key in data) {key_array.push(key);}

key_array.sort(function(a,b){
    var a1=typeof a, b1=typeof b;
    return a1<b1 ? -1 : a1>b1 ? 1 : a<b ? -1 : a>b ? 1 : 0;});

    
for (i=0;i<key_array.length;i++)
{
new_data[key_array[i]]=data[key_array[i]];
}
//sorting done





//console.log(key_array);
   
/*********************Context Movie Menu***********************/
function on_movie_context_menu(data){
    /**************************************************
     * Context-Menu with Sub-Menu
     **************************************************/
    $.contextMenu({
        selector: '#movie-item-li', 
        callback: function(key, options) {
            var m = "clicked: " + key;
            
            //for (var key in options.items.send_to) {console.log(key);};
            
            window.console && console.log(m);
            //console.log(options[key]);
            
            
            if (key=="open"){
			//run_movie( $(this).attr("path") );
            $.getJSON("/oapi/?a=open&n=run_movie&o=path:-"+encodeURIComponent($(this).attr("path")),function(data){});
			console.log( $(this).attr("path") );
            }
            
            else if(key=="open_folder")
            {
            $.getJSON("/oapi/?a=open&n=open_folder&o=path:-"+encodeURIComponent($(this).attr("path")),function(data){});
            console.log( $(this).attr("path") );
            }
            
            
			else if(key=="add_to_watched")
			{
			$.getJSON("/oapi/?a=update&n=wstatus&o=path:-"+encodeURIComponent($(this).attr("path"))+"::wstatus:-1",function(data){});
			console.log( $(this).attr("path") );
			}
			
			else if(key=="add_to_want_to_watch")
			{
			$.getJSON("/oapi/?a=update&n=wstatus&o=path:-"+encodeURIComponent($(this).attr("path"))+"::wstatus:-2",function(data){});
			console.log( $(this).attr("path") );
			}
			
			else if(key=="add_to_not_watched")
			{
			$.getJSON("/oapi/?a=update&n=wstatus&o=path:-"+encodeURIComponent($(this).attr("path"))+"::wstatus:-0",function(data){});
			console.log( $(this).attr("path") );
			}
			
			else if(key=="update")
			{
				console.log( $(this).attr("path") );
				
			}
			
			
			else if(key=="delete")
			{
				console.log( $(this).attr("path") );
			}
			
            else if(key=="properties")
            {
            var imdbid=$(this).attr("imdbid");
            var title=$(this).attr("title");

            open_movie_details(title,imdbid); 
            //console.log( $(this).attr("path") );
            //console.log( imdbid );
            //console.log( title );
            }
            else if(key=="close"){
            
            }
            
            else{
              movie_send_to=options.items.send_to.items[key].path;
              if (movie_send_to !=undefined)
              {
              	$.getJSON("/oapi/?a=send&n=send_to_folder&o=src:-"+encodeURIComponent($(this).attr("path"))+"::dst:-"+encodeURIComponent(movie_send_to),function(data){});
              	
              	}
              	
              }            
        
        },
        items: {
            "open": {"name": "Open"},
			"open_folder": {"name": "Open Folder"},
			"sep0": "---------",
			"add_to_watched":{"name":"Add to Watched"},
			"add_to_not_watched":{"name":"Add to not Watched"},
			"add_to_want_to_watch":{"name":"Want To Watch"},
			"sep1": "---------",
			//"update":{"name":"Update IMDb id"},
			//"delete":{"name":"Delete From Db"},
			"sep2": "---------",
            
            "properties": {"name": "Properties"},
            "sep3": "---------",
            "send_to": {"name": "Send To","items":data},
			"sep5": "---------",
            "close": {"name": "Close"},
            "sep4": "---------"
        }
    });
}

on_movie_context_menu(new_data);




/**************************************/
}


$.getJSON("/oapi/?a=load&n=get_drives",get_data);
}




function refresh_drives()
{
$.contextMenu( 'destroy', "#movie-item-li" );
on_movie_context_menu_build();
} 

var gdata="";


function time_out_call()
{
//console.log("Time out call");

$.getJSON("/oapi/?a=update&n=usb_updates",function(data){
if(data[0]=="1") refresh_drives();


});
var t=setTimeout("time_out_call()",1000);
}


function refresh_movies()
{
$.getJSON("/json/refresh_movies",
    function(data){}
    );
}




    

    

/*Own JavaScript Library*/

    //open movie details
    function open_movie_details(title,imdbid)
    {
    
    $.getJSON("/api?q=True&amp;job=movie&amp;imdbid="+imdbid,
    function(data)
    {
    
    if(data){
    
     var items ="";
     items='<div class="movie_dialog"><div style="float: left;"><img width="214" height="317" src="/cover/'+data.local_cover+'"/></div>';
     items=items+'<p style="margin:5px;">'+data.plot+"<br/><br/>";
     items=items+"Genre: "+data.genre+"<br/>";
     items=items+"Actors: "+data.actors+"<br/>";
     items=items+"Directors: "+data.director+"<br/>";
     items=items+"Runtime: "+data.runtime+"<br/>";
     
     
     items=items+'</p></div>';
     
     
     
     var mid="movie_details_"+data.imdbid+"_"+Date.now();
     
     var movie_details="<div id='"+mid+"'></div>";
     
     $("#imovman_widget").append(movie_details);
     
     //movie Details dialog
     var dlg=$("#"+mid).dialog({
        autoOpen: false,
        draggable: true,
        resizable: false,
        height: 500,
        width:500,
        title:data.title+" ("+data.year+") : "+data.imdbrating,
        model:true,
        
        show:{
         effect: "bounce",
         duration: 1000
         },
        
        hide: {
         effect: "fade",
         duration: 1000
         },
         
        position:{
        my: "center bottom",
        at: "center bottom",
        of: "#header_container"
        },
        
        close: function() {
        $( this ).remove();
        }
      
    });
    //End Movie Details
    
    
    
    d_html='<img id="load_image" src="/image/ui-anim_basic_16x16.gif"/>';
    $("#"+mid).html(d_html);
    $("#"+mid).html(items);
    
    dlg.dialog('open');
    
    }
    
    else//error handler
     {
      var error_p="<div id='error_dlg'></div>";
     $("#imovman_widget").append(movie_details);
     
     //Error dialog
     var edlg=$("#error_dlg").dialog({
        autoOpen: false,
        draggable: true,
        resizable: false,
        height: 500,
        width:500,
        title:"Error",
        model:true,
        
        show:{
         effect: "bounce",
         duration: 1000
         },
        
        hide: {
         effect: "fade",
         duration: 1000
         },
         
        position:{
        my: "center bottom",
        at: "center bottom",
        of: "#header_container"
        },
        
        close: function() {
        $( this ).remove();
        }
      
      
    });
     
    $("#error_dlg").html("Data Fetching Error...");
    edlg.dialog('open');
    }

    
    
    });//end of get json


    
    
    }//end open movie details
/*************************************************/    








/*Position the loading image*/
function position(obj){
  $( "#load_image" ).position({of: $( obj ),my: "center center",at: "center center"});
}


/*Loading Image...*/  
function loading_image(){
  return '<img id="load_image" src="/image/ui-anim_basic_16x16.gif"/>';
}  



  
/*Start of function count Movies*/
function count_movies(term){
  var total_data=0;
  function get_data(data)
  {
  total_data=data.length;
  }
  $.getJSON("/count_movies?q="+term,get_data);
  return total_data;
}
/*End of function count Movies*/


function goToPage( id ) {

  var node = document.getElementById( id );
  
  // Check to see if valid node and if node is a SELECT form control
  
  if( node &&
    node.tagName == "SELECT" ) {

    // Go to web page defined by the VALUE attribute of the OPTION element

    //window.location.href = node.options[node.selectedIndex].value;
    load_movies(node.options[node.selectedIndex].value);
    
  } // endif
  
  
}


function get_genres()
{
  function html_maker_full(data)
  {
  dhtml='<select id="genl" onchange="goToPage(\'genl\')">';
  dhtml=dhtml+'<option value="All" onclick=\"load_movies(\'all\')">All</option>';
  
  //sdata=Array();
  data.sort(function(a,b){
    var a1=typeof a, b1=typeof b;
    return a1<b1 ? -1 : a1>b1 ? 1 : a<b ? -1 : a>b ? 1 : 0;});
    
  
  
  for(i=0;i<data.length;i++)
  {
  dhtml=dhtml+'<option value="'+data[i]+'" onclick=\"load_movies(\''+data[i]+'\')">'+data[i]+'</option>';
  };
  
  dhtml=dhtml+"</select>";
  $("#ogen").html(dhtml);
  
  }

  
  $.getJSON("/get_genres",html_maker_full);

}

  

function format_movie(i,field)
{
movie_html='<li id="movie-item-li" class="movie-item-li"'
            +' title="'+field.title+'"'
            +' imdbid="'+field.imdbid+'"'
            +' path="'+field.path+'"'
            +' status="'+field.status+'"'
            +' wstatus="'+field.wstatus+'"'
            +' cdate="'+field.cdate+'"'
            +' udate="'+field.udate+'"'
            +' imdbrating="'+Number(field.imdbrating).toFixed(1)+'"'
            +' year="'+field.year+'"'
            +' plot="'+field.plot+'"'
            +' rated="'+field.rated+'"'
            +' writer="'+field.writer+'"'
            +' director="'+field.director+'"'
            +' released="'+field.released+'"'
            +' actors="'+field.actors+'"'
            +' genre="'+field.genre+'"'
            +' runtime="'+field.runtime+'"'
            +' type="'+field.type+'"'
            +' imdbvotes="'+field.imdbvotes+'"'
            +' local_cover="'+field.local_cover+'" >'
            +'<table border="0" cellpadding="0" cellspacing="0">';
movie_html=movie_html+'<tr><td valign="baseline" width="214px" height="317px" background="/cover/'+field.local_cover+'">';
movie_html=movie_html+'<table border="0" cellpadding="0" cellspacing="0">';

if (typeof field.imdbrating == typeof 1)
{
movie_html=movie_html+'<tr><td align="right" valign="top" height="17px"><span class="movie_rating">'+field.imdbrating.toFixed(1)+'</span></td></tr>';
}
else
{
movie_html=movie_html+'<tr><td align="right" valign="top" height="17px"><span class="movie_rating">'+field.imdbrating+'</span></td></tr>';
}
movie_html=movie_html+'<tr><td valign="bottom" height="300px"><p class="movie_title_p">'+field.title+' ('+field.year+')'+'</P></td></tr>';
movie_html=movie_html+'</table></td></tr></table></li>';
return movie_html;
}




function form_json_from_node(node)
{
var jstr={};
jstr["title"]=node.getAttribute("title");
jstr["imdbid"]=node.getAttribute("imdbid");
jstr["path"]=node.getAttribute("path");
jstr["status"]=node.getAttribute("status");
jstr["wstatus"]=node.getAttribute("wstatus");
jstr["cdate"]=node.getAttribute("cdate");
jstr["udate"]=node.getAttribute("udate");
jstr["imdbrating"]=node.getAttribute("imdbrating");
jstr["year"]=node.getAttribute("year");
jstr["plot"]=node.getAttribute("plot");
jstr["rated"]=node.getAttribute("rated");
jstr["writer"]=node.getAttribute("writer");
jstr["director"]=node.getAttribute("director");
jstr["released"]=node.getAttribute("released");
jstr["actors"]=node.getAttribute("actors");
jstr["genre"]=node.getAttribute("genre");
jstr["runtime"]=node.getAttribute("runtime");
jstr["type"]=node.getAttribute("type");
jstr["imdbvotes"]=node.getAttribute("imdbvotes");
jstr["local_cover"]=node.getAttribute("local_cover");
return jstr;
}











function sort_movies(term)
{

window.movie_list=document.getElementById("movies_list").childNodes;
console.log(window.movie_list.length);

//var movie_list=document.getElementById("movie-item-li");
var movie_array1=[];
var movie_array2=[];

for (i=0;i<window.movie_list.length;i++)
{
var title=window.movie_list[i].getAttribute("title").toLowerCase();

if (title.search(term.toLowerCase())!=-1)
{
movie_array1.push(window.movie_list[i]);
}
else
{
movie_array2.push(window.movie_list[i]);
}
}

var movie_html="";
for (i=0;i<movie_array1.length;i++){movie_html=movie_html+format_movie(i,form_json_from_node(movie_array1[i]));}
for (i=0;i<movie_array2.length;i++){movie_html=movie_html+format_movie(i,form_json_from_node(movie_array2[i]));}
$("#movies_list").html(movie_html);


console.log("Done");
}



function bubbleSort(a)
{
    var swapped;
    do {
        swapped = false;
        for (var i=0; i < a.length-1; i++) {
            if (a[i].getAttribute("imdbrating") > a[i+1].getAttribute("imdbrating") ) {
                var temp = a[i];
                a[i] = a[i+1];
                a[i+1] = temp;
                swapped = true;
            }
        }
    } while (swapped);
}



/*Start of function Load Movies*/
function sort_by_rating(term){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=sort_rating&o=term:-"+term,movie_html_maker_full);
  //$.getJSON("/oapi/?a=send&n=send_to_folder&o=src:-"+encodeURIComponent($(this).attr("path"))+"::dst:-"+encodeURIComponent(movie_send_to),function(data){});



}


/*Start of function Load Movies*/
function sort_by_year(term){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=sort_year&o=term:-"+term,movie_html_maker_full);
  //$.getJSON("/oapi/?a=send&n=send_to_folder&o=src:-"+encodeURIComponent($(this).attr("path"))+"::dst:-"+encodeURIComponent(movie_send_to),function(data){});



}



/*Start of function Load Movies*/
function load_movies(term){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=load_movies&o=term:-"+term,movie_html_maker_full);
  //$.getJSON("/oapi/?a=send&n=send_to_folder&o=src:-"+encodeURIComponent($(this).attr("path"))+"::dst:-"+encodeURIComponent(movie_send_to),function(data){});



}
/*End of function Load Movies*/

/*Start of function Load Movies*/
function watched_movies(){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=watched_movies",movie_html_maker_full);
  //$.getJSON("/oapi/?a=send&n=send_to_folder&o=src:-"+encodeURIComponent($(this).attr("path"))+"::dst:-"+encodeURIComponent(movie_send_to),function(data){});



}


/*Start of function Load Movies*/
function notwatched_movies(){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=notwatched_movies",movie_html_maker_full);



}





/*Start of function Load Movies*/
function wanttowatch_movies(){
  var movie_content_id="movie_content";
  var mc_object=$("#"+movie_content_id);
  
  mc_object.html(loading_image());
  position($("#movie_container"));
  
  var movie_html='';
  
  function movie_html_make_single(i,field){
    movie_html=movie_html+format_movie(i,field);
    }
  
  function movie_html_maker_full(data)
  {
    $.each(data,movie_html_make_single);
    movie_html=movie_html;
    mc_object.html('<ul id="movies_list">'+movie_html+'</ul>');
  }

  
  $.getJSON("/oapi/?a=load&n=wanttowatch_movies",movie_html_maker_full);



}





function load_unique_windows()
{
var statistics_window="<div id='stat_window'></div>";

$("#imovman_widget").append(statistics_window);
$("#imovman_widget").append('<div id="settings_window"><div id="settings_window_in"></div></div>');
$("#settings_window_in").html("&nbsp;");
$("#settings_window_in").append('<h3>Movie Format</h3>     <div><p>Flv,Mp4</p></div>');
$("#settings_window_in").append('<h3>Movie Folder</h3>     <div><p>Folder Location</p></div>');
$("#settings_window_in").append('<h3>Your Hard Disk Drives</h3>     <div><p>C:\\,D:\\,E:\\,F:\\</p></div>');
$("#settings_window_in").append('<h3>Send To Type:</h3>     <div><p>Only File or Full parent Movie Folder</p></div>');
    

}



/***********************/
function settings_window()
{


//***
var dlg=$("#settings_window").dialog({
  autoOpen: false,
  draggable: false,
  resizable: false,
  height: 500,
  width:500,
  title:"Settings",
  modal:true,
  show:{
    effect: "fade",
    duration: 1000
    },
        
  hide:{
    effect: "fade",
    duration: 1000
    },
         
  position:{
    my: "center center",
    at: "center enter",
    of: window
    },
  open:function(){

    $( "#settings_window_in" ).accordion({
			event: "click"
		});
    }
    ,
  close: function(){
    //$("#settings_window_in").remove();
        //  $("#stat_window").hide();
     }
        
 });//settings window dialog definitation
 
//**/ 
//$("#settings_window_in").accordion();

dlg.dialog('open');
}

/************************/



/*Start of statistics function*/  
function window_statistics()
{

  
  var dlg=$("#stat_window").dialog({
        autoOpen: false,
        draggable: true,
        resizable: false,
        height: "auto",
        width:500,
        title:"Movie Stats",
        model:true,
        
        show:{
         effect: "bounce",
         duration: 1000
         },
        
        hide: {
         effect: "fade",
         duration: 1000
         },
         
        position:{
        my: "center center",
        at: "center enter",
        of: window
        },
        //close: function(){
        //  $("#stat_window").hide();
        //  }
        
    });//staistics window dialog definitation
    
    
    
  dlg.dialog('open');
  $("#stat_window").html(loading_image());
  var obj=$("#stat_window");
  position(obj);
  
  $.getJSON("/api?q=True&amp;job=stat",
        function(data){
          if(data){
            $("#stat_window").html("Total Movies: "+data.total_movies);
            
            }
        }
    );
    

  
    
    
}
/**End of Statistics Window**/








/**When The Document is ready this function will be called***/
function ready_load(){

  load_unique_windows();//load unique windows
  get_genres();
  load_movies("all");//load all available movies
  
  refresh_drives();
  var t=setTimeout("time_out_call()",3000);
//define anything here to load when page loaded

    
    //define movie information dialog box
    var movie_info="<div id='movie_info' title='Movie Information'></div>";
    $("#imovman_widget").append(movie_info);
    

    
    //movie info dialog settings
    $("#movie_info").dialog({
        autoOpen: false,
        draggable: true,
        resizable: false,
        height: 'auto',
        modal:true,
        
        show:{
         effect: "bounce",
         duration: 1000
         },
        
        hide: {
         effect: "fade",
         duration: 1000
         },
         
        position:{
        my: "center center",
        at: "center center",
        of: window
        },
        
        buttons: {
        OK: function() {
          $( this ).dialog( "close" );
        }
      }
    });
    //End Movie Info dialog settings
    
    
    
    
    
    

 
 
 
    
    //autocomplete definitation
    $("#search_box").autocomplete({
       source: function( request, response ){
        $.ajax({
          url: "/api",
          dataType: "json",
          
          data:
            {
            job: "search",
            stype: "all",
            q: request.term
            },
          
        success: function( data )
          {
          
           if (data.length==0){
            return response([{label:"Nothing found..",value:request.term}]);
            
            }
           else
           {
           
           var my_l=[];
           //loop through the data and make a array
           $.each(data,
             function(i, field){
              
              if (field.dtype=="title"){
                my_l.push({label:field.name,value:field.name,dtype:field.dtype,imdbid:field.imdbid});
              }
              else
              {
              my_l.push({label:field.name,value:field.name,dtype:field.dtype});
              }
              
              }
              );
           return response(my_l);
           
           
           }
            
            }
            
        });
      },
      
      minLength: 2,
      
      select: function( event, ui )
      {
      //$("#search_box").attr("value","");
      //log( ui.item ?"Selected: " + ui.item.label +" "+ui.item.dtype:"Nothing selected, input was " + this.value);
      //$('#movie_details').prop('title',);
      //$("#movie_details").append();
      
      if (ui.item.dtype=="title"){
      	//open_movie_details(ui.item.label,ui.item.imdbid);
      	load_movies(ui.item.value);
      	
      	}
      else{load_movies(ui.item.value);}
      //load_movies(ui.item.value);
      //$("#movie_details").dialog( "open" );
 
      }
      ,
      change:function(event,ui)
      {

      }
      ,
      
      open: function(){
       //console.log("open");
       sort_movies(this.value);
       //$("#movies_list").scrollTo(0);
       //$("#movie_container").addClass("ui-autocomplete-loading" );
       //$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
      },
      
      close: function() {
        //$( this ).removeClass( "ui-autocomplete-loading" ).addClass("search_box" );
        //$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
      }
      
    });
    //auto complete search end here
    


$(document).on('click', '#btn_what', function(e){
    var offest = $(this).offset();
    var height = $(this).height();
    //$('#movie_info').dialog("option", "position", [offest.left, offest.top+height]);
    $('#movie_info').dialog('open');
});


$("#genl").attr("selectedIndex", -1);
$("#genl").change(function()
            {
            	load_movies($("#genl option:selected").val());
                //$("#answer").text();
            });
            
            
}
/***End Of ready_load***/



$(document).ready(ready_load);//now load the ready load function




$(document).bind("contextmenu", function(event) {
    //event.preventDefault();
    /*
    $("<div class='custom-menu'>Custom menu</div>")
        .appendTo("body")
        .css({top: event.pageY + "px", left: event.pageX + "px"});
        */
});


$(document).bind("click", function(event) {
/*
    $("div.custom-menu").hide();
    */
    
});













        

