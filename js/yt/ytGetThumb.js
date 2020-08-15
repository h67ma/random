javascript:{
	let urlParams = new URLSearchParams(window.location.search);
	let vidId = urlParams.get("v");
	window.location.href = "https://img.youtube.com/vi/" + vidId + "/0.jpg";
}
