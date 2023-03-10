<script>
	import Select from 'svelte-select';

	import { load } from './fetch';
	import Result from './Result.svelte';

	/**
	 * @type {any}
	 */
	let pathway = { value: 9, label: 10 };
	let iterations = { value: 99, label: 100 };
	let beam_size = { value: 49, label: 50 };
	let on = true;
	let off = false;
	let target_molecule = { label: '', value: '' };
	let retrieval = on ? true : false;
	let url =
		'https://retro.pnucolab.com/run?product=' +
		target_molecule.value +
		'&route_topk=' +
		pathway.label +
		'&iterations=' +
		iterations.label +
		'&beam_size=' +
		beam_size.label +
		'&retrieval=' +
		retrieval;
	/**
	 * @type {string | null}
	 */
	let t = null;
</script>

<div class="h-full w-full bg-white flex flex-col justify-center px-24 p-3">
	<div class="w-full flex my-10">
		<p class="w-3/12 text-xl font-bold mr-4">Target molecule</p>
		<input
			class="w-9/12 h-10 rounded-lg border border-point px-5 "
			type="text"
			id="first"
			name="first"
			placeholder="SMILES"
			required
			bind:value={target_molecule.value}
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
			</div>
			<div class="flex p-5">
				<p class="w-4/12">beam size</p>
				<Select
					items={[...Array(50).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
					bind:value={beam_size}
				/>
			</div>

			<div class="flex p-5">
				<p class="w-4/12">retriever usage</p>
				<div class="w-full">
					<button
						class={on
							? 'bg-blue-500 text-blue-700 font-semibold text-white py-2 px-4 border border-blue-500 border-transparent rounded mr-5'
							: 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded mr-5'}
						on:click={() => {
							if (!on) {
								on = !on;
								off = !off;
							}
						}}
					>
						On
					</button>
					<button
						class={off
							? 'bg-blue-500 text-blue-700 font-semibold text-white py-2 px-4 border border-blue-500 border-transparent rounded mr-5'
							: 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded mr-5'}
						on:click={() => {
							if (!off) {
								on = !on;
								off = !off;
							}
						}}
					>
						Off
					</button>
				</div>
			</div>
		</div>
	</div>
	<button
		class={'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-6'}
		on:click={() => {
			load(url).then((result) => {
				t = result.ticket;
				console.log(t);
				let url2 = 'https://retro.pnucolab.com/result?ticket=' + t;
				console.log(url2);
				load(url2).then((result) => {
					console.log(result);
				});
				console.log(t);
			});
			console.log(t);
		}}
	>
		load
	</button>
</div>
