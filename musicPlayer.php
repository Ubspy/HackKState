<?php

$mode = $_POST["mode"];
$data = $_POST["data"];

if($mode == "0")
{

	$data = explode(",", $data);

	$songs = $data[0];
	$notes = $data[1];
	$tempo = $data[2];
	$synth = $data[3];

	$uniq = uniqid();

	$fileLocation = "/var/www/html/randomsongs/".$uniq.".wav";
	$pre = "/var/www/html/";
	$relativeLoc = "randomsongs/".$uniq.".mp3";

	exec("guidedmusicgen ".$notes." ".$synth." ".$songs." ".$tempo." ".$fileLocation);

}
elseif($mode == "1")
{
	#bpm,length,key,synth
	$data = explode(",",$data);

	$bpm = $data[0];
	$length = $data[1];
	$key = $data[2];
	$synth = $data[3];

	$uniq = uniqid();

	$fileLocation = "/var/www/html/randomsongs/".$uniq.".wav";
	$pre = "/var/www/html/";
	$relativeLoc = "randomsongs/".$uniq.".mp3";

	exec("proceduralmusicgen ".$bpm." ".$length." ".$key." ".$synth." ".$fileLocation);
}

?> 

<style>
#thefile {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 100;
}

#canvas {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}

audio {
  position: fixed;
  left: 10px;
  bottom: 10px;
  width: calc(100% - 20px);
}
</style>

<div id="content">
  <canvas id="canvas"></canvas>
  <audio id="audio" controls preload="auto"></audio>
</div>

<script>
window.onload = function() {
  
  	var audio = document.getElementById("audio");
  
	var files = this.files;
	audio.src = "<?php echo $relativeLoc; ?>";
	//audio.load();
	audio.play();
	var context = new AudioContext();
	var src = context.createMediaElementSource(audio);
	var analyser = context.createAnalyser();

	var canvas = document.getElementById("canvas");
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	var ctx = canvas.getContext("2d");

	src.connect(analyser);
	analyser.connect(context.destination);

	analyser.fftSize = 256;

	var bufferLength = analyser.frequencyBinCount;
	console.log(bufferLength);

	var dataArray = new Uint8Array(bufferLength);

	var WIDTH = canvas.width;
	var HEIGHT = canvas.height;

	var barWidth = (WIDTH / bufferLength) * 2.5;
	var barHeight;
	var x = 0;

	function renderFrame() {
	  requestAnimationFrame(renderFrame);

	  x = 0;

	  analyser.getByteFrequencyData(dataArray);

	  ctx.fillStyle = "#000";
	  ctx.fillRect(0, 0, WIDTH, HEIGHT);

	  for (var i = 0; i < bufferLength; i++) {
	    barHeight = dataArray[i];
	    
	    var r = barHeight + (25 * (i/bufferLength));
	    var g = 250 * (i/bufferLength);
	    var b = 50;

	    ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
	    ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

	    x += barWidth + 1;
	  }
	}

	audio.play();
	renderFrame();
	};
</script>