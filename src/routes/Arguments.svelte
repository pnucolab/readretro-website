<script>
	import Select from 'svelte-select';
	import { onMount } from 'svelte';

	$: items = fetch(`https://retro.pnucolab.com/run`).then((response) => response.json());
</script>

<div class="h-full w-10/12 bg-white flex flex-col justify-items-start px-24 p-3">
	<div class="w-full flex my-10">
		{#await items}
			<p>loading...</p>
		{:then items}
			<p>{items}</p>
		{/await}
		<p class="w-3/12 text-xl font-bold mr-4">Target molecule</p>
		<input
			class="w-9/12 h-10 rounded-lg border border-point px-5 "
			type="text"
			id="first"
			name="first"
			placeholder="SMILES"
			required
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
				/>
			</div>
			<div class="flex p-5">
				<p class="w-4/12"># of iterations</p>
				<Select
					items={[...Array(120).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
				/>
			</div>
			<div class="flex p-5">
				<p class="w-4/12">beam size</p>
				<Select
					items={[...Array(50).keys()].map((e) => {
						return { value: e, label: (e + 1).toString() };
					})}
				/>
			</div>

			<div class="flex p-5">
				<p class="w-4/12">retriever usage</p>
				<div class="w-full">
					<button
						class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded mr-5"
					>
						On
					</button>
					<button
						class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
					>
						Off
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
