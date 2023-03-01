<script>
	import Select from 'svelte-select';
	import { onMount } from 'svelte';

	/**
	 * @type {any}
	 */
	let pathway = { value: 9, label: 10 };
	let iterations = { value: 99, label: 100 };
	let beam_size = { value: 49, label: 50 };
	let on = true;
	let off = false;
	let target_molecule = { value: 'rr', label: 'rr' };

	// @ts-ignore
	async function load() {
		console.log('adsf');
		let retrieval = on ? true : false;
		const res = await fetch(
			'https://retro.pnucolab.com/run?product=' +
				target_molecule.value +
				'&route_topk=' +
				pathway.label +
				'&iterations=' +
				iterations.label +
				'&beam_size=' +
				beam_size.label +
				'&retrieval=' +
				on,
			{
				method: 'GET'

				//headers: { Authorization: 'Basic ' + base64.encode(username + ':' + password) }
			}
		);
		console.log(res);
		const articles = await res.json();
		console.log(articles);
	}

	{
		/*async function flowerCheck(img, threshold) {
		const response = await fetch(img.uri);
		const blob = await response.blob();
		if (!blob) return;
		const sotrageRef = ref(firebaseInit.storage, 'checkingFile/check.png');
		await uploadBytesResumable(sotrageRef, blob);
		const res = await axios.post(
			'http://34.64.231.30:8000/flowerChecking?threshold=' + threshold.toString()
		);
		if (res.data.flower_name == 'unknown') return null;
		const flowerName = res.data.flower_name;
		for (const info of plant) {
			if (info.name == flowerName) {
				return info.name;
			}
		}
		return null;
	}*/
	}

	onMount(() => {
		console.log('mounted');
		load();
	});
</script>

<div class="h-full w-10/12 bg-white flex flex-col justify-items-start px-24 p-3">
	<div class="w-full flex my-10">
		<p class="w-3/12 text-xl font-bold mr-4">Target molecule</p>
		<input
			class="w-9/12 h-10 rounded-lg border border-point px-5 "
			type="text"
			id="first"
			name="first"
			placeholder="SMILES"
			required
			value={target_molecule.label}
		/>
	</div>

	<div class="w-full flex">
		<h1 class="text-xl font-bold mr-8">Options</h1>

		<div class="w-full">
			<div class="flex p-5">
				<p class="w-4/12"># of pathway generation</p>
				<Select
					class="w-1/2"
					items={[...Array(20).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
					bind:value={pathway}
				/>
			</div>
			<div class="flex p-5">
				<p class="w-4/12"># of iterations</p>
				<Select
					items={[...Array(120).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
					bind:value={iterations}
				/>
				<p>{iterations.label}</p>
			</div>
			<div class="flex p-5">
				<p class="w-4/12">beam size</p>
				<Select
					items={[...Array(50).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
					bind:value={beam_size}
				/>
				<p>{beam_size.label}</p>
			</div>

			<div class="flex p-5">
				<p class="w-4/12">retriever usage</p>
				<div class="w-full">
					<button
						class={on
							? 'bg-blue-500 text-blue-700 font-semibold text-white py-2 px-4 border border-blue-500 border-transparent rounded mr-5'
							: 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded mr-5'}
						on:click={() => {
							on = !on;
							off = !off;
						}}
					>
						On
					</button>
					<button
						class={off
							? 'bg-blue-500 text-blue-700 font-semibold text-white py-2 px-4 border border-blue-500 border-transparent rounded mr-5'
							: 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded mr-5'}
						on:click={() => {
							on = !on;
							off = !off;
						}}
					>
						Off
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
