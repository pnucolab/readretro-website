// @ts-ignore

let site_root = "https://retroapi.pnucolab.com/";

export async function load(uri) {
	let resp = await fetch(site_root + uri);
	let rtn = await resp.json();
	return rtn;
}
