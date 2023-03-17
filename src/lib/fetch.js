// @ts-ignore
export async function load(url) {
	let resp = await fetch(url);
	let rtn = await resp.json();
	return rtn;
}
