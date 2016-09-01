  
  //var lastInput = {{ entries | tojson }};
  //var merge = document.getElementById('merge').innerHTML;
  //document.getElementById('merge-s1').style.visibility = "hidden";
  //document.getElementById('merge-s2').style.visibility = "hidden";
  //document.getElementById('merge-s').style.visibility = "hidden";


  $('#undo-2').click(function(){
  	//var _lastSent = document.getElementById("reverse-1").innerHTML;
  	//var lastSent = _lastSent.replace(/^\s*<br\s*\/?>|<br\s*\/?>\s*$/g,'');
  	//console.log(lastSent)
  	//var merge2 = lastSent + document.getElementById("reverse-2").innerHTML;
  	//console.log(merge2)
  	//document.getElementById("reverse-1").innerHTML = '';
    //the 2nd sent is the child of the s1 or s2?
    var merge2 = document.getElementById('merge-s1').innerHTML;
  	$('#reverse-1').remove();
    document.getElementById("reverse-2").innerHTML = merge2;

    //document.getElementById('undo-2').style.visibility='hidden';
    $('#undo-2').remove();

  });

  $('#undo-4').click(function(){
  	//var _lastSent = document.getElementById("reverse-2").innerHTML;
  	//var lastSent = _lastSent.replace(/^\s*<br\s*\/?>|<br\s*\/?>\s*$/g,'');
  	//console.log(lastSent)
  	//var merge3 = lastSent + document.getElementById("reverse-3").innerHTML;
  	//document.getElementById("reverse-2").innerHTML = '';
    
    var merge3 = document.getElementById('merge-s2').innerHTML;	
    document.getElementById("reverse-4").innerHTML = merge3;

    //document.getElementById('undo-3').style.visibility='hidden';  
    $('#undo-3').remove();
  });

  $('#undo-5').click(function(){  // s2 doesn't have the children
    //var _lastSent = document.getElementById("reverse-3").innerHTML;
    //var lastSent = _lastSent.replace(/^\s*<br\s*\/?>|<br\s*\/?>\s*$/g,'');
    //console.log(lastSent)
    //var merge4 = lastSent + document.getElementById("reverse-4").innerHTML;

    var merge6 = document.getElementById('merge-s').innerHTML; 
    //console.log(merge4)
    document.getElementById("reverse-5").innerHTML = merge6;

    //document.getElementById('undo-4').style.visibility='hidden';
    $('#reverse-1').remove();  // remove s1
    $('#undo-5').remove();
  }); 

  $('#undo-6').click(function(){  // s2 has the children
  	//var _lastSent = document.getElementById("reverse-3").innerHTML;
  	//var lastSent = _lastSent.replace(/^\s*<br\s*\/?>|<br\s*\/?>\s*$/g,'');
  	//console.log(lastSent)
  	//var merge4 = lastSent + document.getElementById("reverse-4").innerHTML;

    var merge4 = document.getElementById('merge-s2').innerHTML; 
    //console.log(merge4)
    document.getElementById("reverse-6").innerHTML = merge4;

    //document.getElementById('undo-4').style.visibility='hidden';
    $('#reverse-5').remove();
    $('#undo-6').remove();
  }); 