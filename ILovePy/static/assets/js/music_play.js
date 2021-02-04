// JavaScript Document

window.onload = function(){
	var audio = document.getElementById('music');
	audio.pause();//打开页面时无音乐
}

function play() {
	var audio = document.getElementById('music');
	if(audio.paused) {
		audio.play();
		document.getElementById('musicImg').src="images/banner_3.jpg";
	}
	else{
		audio.pause();
		//audio.currentTime = 0;//让音乐回到开始，去掉的话就仅仅是暂停
		document.getElementById('musicImg').src="images/banner_3.5.jpg";
	}
}

