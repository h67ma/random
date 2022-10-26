javascript:
{
	/* works for "yt music" and "shorts" */
	window.location.href = "https://www.youtube.com/watch?v=" + window.location.href.match(/(?:(?:\?|&)v=|\/shorts\/)([^&?]+)/)[1];
}
