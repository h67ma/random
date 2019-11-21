javascript:
{
	if (/https:\/\/www.youtube.com\/playlist\?list=/.test(window.location.href))
	{
		let videoList = document.body.innerHTML
			.replace(/^(?:[^](?!<tr))+/, "")
			.replace(/(?:[^](?<!<\/tr>))+$/, "")
			.replace(/(?:\r|\n)/g, "")
			.replace(
				/<tr[^>]*data-video-id="([^"]+)"(?:.(?<!<\/tr>))*<a class="pl-video-title-link[^>]*>\s*([^<]+)\s*<\/a>\s*(?:<div class="pl-video-owner">[^<]*by <a[^>]*>([^<]+)<\/a>)?(?:.(?<!<\/tr>))*<div class="more-menu-wrapper">\s*(?:<div class="timestamp"><span[^>]*>([^<]+)<\/span>)?(?:.(?<!<\/tr>))*<\/tr>/g,
				"<tr><td><a href=\"https://www.youtube.com/watch?v=$1\"><img src=\"https://img.youtube.com/vi/$1/0.jpg\"/></a></td><td><a href=\"https://www.youtube.com/watch?v=$1\">$2</a></td><td><a href=\"https://youtube.com/user/$3\">$3</a></td><td>$4</td></tr>\n"
			)
			.replace(/\n +/g, "\n");
			
		videoList = "<!DOCTYPE html><html><body><table border=\"1\"><tr><th>image</th><th>title</th><th>channel</th><th>duration</th></tr>" + videoList + "</table></body></html>";

		let element = document.createElement('a');
		element.setAttribute("href", "data:text/html;charset=utf-8," + encodeURIComponent(videoList));
		element.setAttribute("download", document.title.replace(".", "_"));

		element.style.display = "none";
		document.body.appendChild(element);

		element.click();

		document.body.removeChild(element);
	}
	else
	{
		alert("I don't think this is a Youtube playlist...");
	}
}
