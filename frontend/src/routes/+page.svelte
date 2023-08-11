<script>
	import Arguments from '../lib/Arguments.svelte';
	import BuildingBlocks from '../lib/Building_Blocks.svelte';
	import RetrievalDb from '../lib/Retrieval_DB.svelte';
	import Top from '../lib/Top.svelte';
	import { Button } from 'flowbite-svelte';
	import { load } from '../lib/fetch';

	let title;
	let pathway;
	let iterations;
	let beam_size;
	let expansions;
	let on = true;
	let target_molecule;
	let ticket;
	let files;
	let building_blocks = [];
	let active_tab = 0;
	let path_retrieval = true;
	let model;
	let tabs = ['Arguments', 'Building Blocks', 'Retrieval DB'];

	async function run() {
		let url =
			'run?title=' +
			encodeURIComponent(title ? title : 'Untitled') +
			'&product=' +
			encodeURIComponent(
				target_molecule ? target_molecule : 'CCC1=CC2CC3(C1N(C2)CCC4=C3NC5=CC=CC=C45)C(=O)OC'
			) +
			'&building_blocks=' +
			encodeURIComponent(building_blocks.join(',')) +
			'&iterations=' +
			(iterations ? iterations : 100) +
			'&exp_topk=' +
			(expansions ? expansions : 10) +
			'&route_topk=' +
			(pathway ? pathway : 10) +
			'&beam_size=' +
			(beam_size ? beam_size : 10) +
			'&retrieval=' +
			on +
			'&path_retrieval=' +
			path_retrieval +
			'&model=' +
			encodeURIComponent(model ? model : 'ensemble');
		let response;
		if (files && files.length == 1) {
			response = await load(url, 'POST', files[0]);
		} else {
			response = await load(url, 'POST');
		}
		ticket = response.ticket;
		location.href = `/result/${ticket}`;
	}
</script>

<Top />

<div
	class="text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700"
>
	<ul class="flex flex-wrap -mb-px">
		{#each tabs as tab, i}
			<li class="mr-2">
				<button
					class="flex items-center gap-2 inline-block p-4 border-b-2 rounded-t-lg {active_tab === i
						? 'active text-blue-600 border-blue-600 dark:text-blue-500 dark:border-blue-500'
						: 'border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300'}"
					on:click={() => {
						active_tab = i;
					}}
				>
					{#if i === 0}
						<svg
							aria-hidden="true"
							class="w-5 h-5"
							fill="currentColor"
							viewBox="0 0 20 20"
							xmlns="http://www.w3.org/2000/svg"
							><path
								d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"
							/>
						</svg>
					{:else if i === 1}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-5 h-5"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M2.25 7.125C2.25 6.504 2.754 6 3.375 6h6c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-6a1.125 1.125 0 01-1.125-1.125v-3.75zM14.25 8.625c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v8.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 01-1.125-1.125v-8.25zM3.75 16.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 01-1.125-1.125v-2.25z"
							/>
						</svg>
					{:else if i === 2}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-5 h-5"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125"
							/>
						</svg>
					{/if}
					{tab}</button
				>
			</li>
		{/each}
	</ul>
</div>

<div class="p-8 rounded-lg border mt-4 {active_tab != 0 ? 'hidden' : ''}">
	<Arguments
		bind:title
		bind:pathway
		bind:iterations
		bind:beam_size
		bind:on
		bind:target_molecule
		bind:expansions
	/>
</div>

<div class="p-8 rounded-lg border mt-4 {active_tab != 1 ? 'hidden' : ''}">
	<BuildingBlocks bind:smiles={building_blocks} />
</div>

<div class="p-8 rounded-lg border mt-4 {active_tab != 2 ? 'hidden' : ''}">
	<RetrievalDb bind:files />
</div>

<div class="mt-8 text-center">
	<Button size="xl" on:click={() => run()} type="submit">Submit</Button>
</div>
