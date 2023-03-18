<script>
	import Arguments from '../lib/Arguments.svelte';
	import BuildingBlocks from '../lib/Building_Blocks.svelte';
	import RetrievalDb from '../lib/Retrieval_DB.svelte';
	import Top from '../lib/Top.svelte';
	import { Button } from 'flowbite-svelte';
	import { Tabs, TabItem } from 'flowbite-svelte';
	import { load } from '../lib/fetch';

	let pathway = { value: 9, label: 10 };
	let iterations = { value: 99, label: 100 };
	let beam_size = { value: 49, label: 50 };
	let on = true;
	let target_molecule = { label: 'O=C1C=C2C=CC(O)CC2O1', value: 'O=C1C=C2C=CC(O)CC2O1' };
	let ticket;
	let building_blocks = [];

	async function run(url) {
		const response = await load(url);
		ticket = response.ticket;
		location.href = `/result/${ticket}`;
	}
</script>

<Top />

<Tabs style="underline" contentClass="p-8 rounded-lg border mt-4">
	<TabItem open>
		<div slot="title" class="flex items-center gap-2">
			<svg
				aria-hidden="true"
				class="w-5 h-5"
				fill="currentColor"
				viewBox="0 0 20 20"
				xmlns="http://www.w3.org/2000/svg"
				><path
					d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"
				/></svg
			>
			Arguments
		</div>
		<Arguments bind:pathway bind:iterations bind:beam_size bind:on bind:target_molecule />
	</TabItem>
	<TabItem>
		<div slot="title" class="flex items-center gap-2">
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
			Building Blocks
		</div>
		<BuildingBlocks bind:smiles={building_blocks} />
	</TabItem>
	<TabItem>
		<div slot="title" class="flex items-center gap-2">
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
			Retrieval DB
		</div>
		<RetrievalDb />
	</TabItem>
</Tabs>
<div class="mt-8 text-center">
	<Button
		size="xl"
		on:click={() =>
			run(
				'run?product=' +
					target_molecule.value +
					'&building_blocks=' +
					building_blocks.join(',') +
					'&route_topk=' +
					pathway.label +
					'&iterations=' +
					iterations.label +
					'&beam_size=' +
					beam_size.label +
					'&retrieval=' +
					on
			)}
		type="submit">Submit</Button
	>
</div>