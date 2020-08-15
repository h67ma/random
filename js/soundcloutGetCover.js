javascript:
{
	/* can't just search on current page cause soundclout does some weird stuff when you click links, and the page source is the *first* page source that you visit */
	fetch(document.location.href)
		.then(response => response.text())
		.then(pageSource => window.location.href = pageSource.match(/<meta property="og:image" content="([^"]+)">/)[1]);
}
