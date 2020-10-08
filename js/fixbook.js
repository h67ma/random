javascript:
{
	/* change title */
	document.title = "Fakelook";

	/* bigger chats, hide annoying chat baloon notifications */
	var customCss = `div[role='region'] { height: 3000px !important; width: 400px !important; }
	div[data-pagelet='root'] > div:first-child > div:nth-child(8) > div:last-child { display: none !important; }`;

	/* add custom styles */
	var styleNode = document.createElement("style");
	styleNode.type = "text/css";
	styleNode.appendChild(document.createTextNode(customCss));
	document.head.appendChild(styleNode);

	/* remove useless stuff */
	var pageContent = document.getElementsByTagName("iframe")[0];
	pageContent.parentNode.removeChild(pageContent);

	var topNav = document.querySelectorAll("[role='banner']")[0];
	topNav.removeChild(topNav.children[0]); /* logo */
	topNav.removeChild(topNav.children[0]); /* search thing */
	topNav.removeChild(topNav.children[0]); /* random buttons */
}
