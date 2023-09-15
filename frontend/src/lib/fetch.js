// @ts-ignore

let site_root = 'https://readretro.net/api/v1/';

export async function load(uri, method = 'GET', file = null) {
	let resp;
	if (method == 'GET') {
		resp = await fetch(site_root + uri);
	} else if (method == 'POST') {
		let data = null;
		if (file) {
			data = new FormData();
			data.append('file', file);
		}
		resp = await fetch(site_root + uri, {
			method: 'POST',
			body: data
		});
	}
	let rtn = await resp.json();
	return rtn;
}
