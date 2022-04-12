/*  File: jsfile.js
	Author: G.J.H. Schuurman
	Date: 12/04/2022
	Its main function is to send and receive data to/from process.py
	using ajax. Also contains several other functions for usability 
	on the webpage webpage.html */

$(document).ready(function() {
	/* Ensures the colored faces scroll simultaniously with the text */
	$('#successAlert').on('scroll', function () {
		$('#background').scrollTop($(this).scrollTop());
	});
	$('#successAlert').on('input', function () {
		$('#background').scrollTop($(this).scrollTop());
	});
}); 

function loadFile(){
	/* Takes .txt file from file input, and sends contents to ajaxCall() */
	let input = document.getElementById('fileInput');
    let file = input.files[0];
    if(file != null && file.name.endsWith('.txt')) {
        let fileReader = new FileReader();
        fileReader.onload = () => {
            ajaxCall(fileReader.result, true);
        };
        fileReader.readAsText(file);
    }
}

function ajaxCall(indata, refresh){
	/* receives indata as string to process, sends it to process.py using
	   ajax, and prints the results on webpage. Boolean refresh is used to 
	   indicate whether the textarea needs to be refreshed or not. */
	if(indata == ''){
        $('#otherData').text('Oeps, het is niet gelukt de resultaten te berekenen!');
		return
	}
	   
	$.ajax({
        data: {
            input_text: indata
        },
            type: 'POST',
            url: '/process'
    })
    .done(function (data) {
        if (data.other) {
			if (refresh) {
				document.getElementById('successAlert').value = data.out;
			}
			$('#background').html(data.html_text.replace(/\n/g, "<br />").replace(/en/g, "<span class='mistake'>en</span>").replace(/on/g, "<span class='orange' title='hallo'>on</span>")+' ');
            $('#otherData').html("<table>" + data.other + "</table>");
        } else {
            $('#otherData').text('Oeps, het is niet gelukt de resultaten te berekenen!');
        }
    });
}

function collapseSidebar() {
	/* Toggles collapse and expand on sidebar and textarea in webpage.html */
	var el = document.getElementById("otherData");
	el.classList.toggle("collapse");
	var other_el = document.getElementById("text");
	other_el.classList.toggle("openup");
}

function saveText() {
	/* Downloads the data in textarea in NTB-[date].txt format */
	let data = document.querySelector('#successAlert').value;
	let filename = "NTB-" + Date.now();
	let file = filename + '.txt';

	let link = document.createElement('a');
	link.download = file;
	let blob = new Blob(['' + data + ''], {
		type: 'text/plain'
	});
	link.href = URL.createObjectURL(blob);
	link.click();
	URL.revokeObjectURL(link.href);
}