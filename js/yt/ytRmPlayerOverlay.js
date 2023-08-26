javascript:
{
	document.getElementById("ytd-player").style.borderRadius = 0;

	let muda = [
		"ytp-chrome-bottom",
		"ytp-gradient-bottom",
		"ytp-gradient-top",
		"ytp-chrome-top"
	];

	muda.forEach(useless =>
	{
		let elem = document.getElementsByClassName(useless)[0];
		elem.parentNode.removeChild(elem);
	});
}
