javascript:
{
	function removeElementById(id)
	{
		var elem = document.getElementById(id);
		if(elem == null) return;
		elem.parentNode.removeChild(elem);
	}

	var cssRulez = ".fbDockWrapperRight { right: 0 !important; } /* remove chats right margin */
					.fbNubFlyoutInner > div:nth-child(2) { height: 800px !important; } /* chat height */
					";

	/* add custom styles */
	var styleNode = document.createElement("style");
	styleNode.type = "text/css";
	styleNode.appendChild(document.createTextNode(cssRulez));
	document.head.appendChild(styleNode);

	/* change title */
	document.title = "Fakelook";

	/* remove useless stuff */
	removeElementById("BuddylistPagelet");
	removeElementById("pagelet_sidebar");
	removeElementById("globalContainer");
}
