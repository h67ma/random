javascript:
{
	/* it's easier to find high quality "topic" version of a song on yt music. then use this script to go to normal youtube. */
	window.location.href = "https://www.youtube.com/watch?v=" + window.location.href.match(/\?v=([^&]+)/)[1];
}
