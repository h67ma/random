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
				"https://www.youtube.com/watch?v=$1,$2,$3,$4\n"
			)
			.replace(/\n +/g, "\n");
			
		videoList = "href,title,channel,length\n" + videoList;

		let element = document.createElement('a');
		element.setAttribute("href", "data:text/csv;charset=utf-8," + encodeURIComponent(videoList));
		element.setAttribute("download", document.title.replace(".", "_") + ".csv");

		element.style.display = "none";
		document.body.appendChild(element);

		element.click();

		document.body.removeChild(element);
	}
}
