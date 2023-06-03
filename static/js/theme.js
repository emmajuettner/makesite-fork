function theme_set(theme_name) {
	console.log("switching to theme " + theme_name);
	switch(theme_name) {
		case "halloween":
			document.getElementById('style-halloween').disabled=false;
			document.getElementById('style-dark').disabled = true;
			document.getElementById('style-light').disabled = true;
			break;
		case "dark":
			document.getElementById('style-halloween').disabled=true;
			document.getElementById('style-dark').disabled = false;
			document.getElementById('style-light').disabled = true;
			break;
		case "light":
		default:
			document.getElementById('style-halloween').disabled=true;
			document.getElementById('style-dark').disabled = true;
			document.getElementById('style-light').disabled = false;
			break;
	}
}

function theme_save(theme_name) {
	console.log("saving theme preference " + theme_name + " in localStorage");
	localStorage.setItem('current-theme', theme_name);
}

// on startup
if (localStorage.getItem('current-theme') !== undefined && localStorage.getItem('current-theme') !== null) {
	console.log("using previously set theme preference of " + localStorage.getItem('current-theme'));
	theme_set(localStorage.getItem('current-theme'));
} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
	console.log("theme preference not set but dark mode preferred, using dark theme");
	theme_set("dark");
} else {
	console.log("no previous theme preference and no dark mode preference, using light theme");
	theme_set("light");
}
