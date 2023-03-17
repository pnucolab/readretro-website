// @ts-ignore

let site_root = "https://retro.pnucolab.com/api/v1/";

export async function load(uri) {
	let resp = await fetch(site_root + uri);
	let rtn = await resp.json();
	return rtn;
}
