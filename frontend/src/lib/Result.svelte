<script>
	import { Label, Span, Spinner } from 'flowbite-svelte';
	import { load } from './fetch';
	import Top from '../lib/Top.svelte';
	import { Card, P, A } from 'flowbite-svelte';
	import { Heading } from 'flowbite-svelte';
	import { Popover, Button, Toggle } from 'flowbite-svelte';
	import download from 'downloadjs';
	import { page } from '$app/stores';

	export let ticket;
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';

	let last = (a, i) => i == a.length - 1;
	let result = {};
	let loaded = false;
	let pathways = [];

	async function mol2image(mol) {
		const result = await load('mol2image?mol=' + encodeURIComponent(mol));
		return result.image;
	}

	async function get_result(ticket) {
		const data = await load('result?ticket=' + ticket);
		result = data;
		if (result.success) {
			if (result.status == 0) {
				pathways = [...data.pathway];
				let mols = [];
				for (let i = 0; i < result.pathway.length; i++) {
					for (let j = 0; j < result.pathway[i].length; j++) {
						mols.push(result.pathway[i][j]);
					}
				}
				mols = [...new Set(mols)];
				filters = mols.map((m) => {
					return { name: m, value: m };
				});
			} else if (result.status > 0) {
				setTimeout(() => get_result(ticket), 1000);
			}
		}
	}

	async function rdb(mol1, mol2) {
		const rdb = await load(
			'rdbsearch?mol1=' + encodeURIComponent(mol1) + '&mol2=' + encodeURIComponent(mol2)
		);
		console.log(rdb.existence);
		return rdb.existence;
	}

	async function pop_up(mol) {
		const mnx = await load('mnxsearch?query=' + encodeURIComponent(mol));
		return mnx;
	}

	async function download_result() {
		let final_result = '';
		final_result += '#title: ' + result.title + '\n';
		final_result += '#task ID: ' + result.task_id + '\n';
		for (let i = 0; i < result.pathway.length; i++) {
			final_result += result.pathway[i].join('>>') + '\n';
		}
		download(final_result, 'result.txt', 'text/plain');
	}

	onMount(async () => {
		await get_result(ticket);
		loaded = true;
	});

	import arrow_image from '$lib/images/right-arrow.svg';
	import arrow_image_red from '$lib/images/right-arrow-red.svg';
	import { onMount } from 'svelte';

	let reverse = true;
	let filters = [];

	import { Select } from 'flowbite-svelte';
	let selected;

	$: {
		if (selected) {
			pathways = result.pathway.filter((p) => p.includes(selected));
			pathways = pathways.concat(result.pathway.filter((p) => !p.includes(selected)));
		} else {
			pathways = result.pathway;
		}
	}
</script>

<Top />

{#if loaded}
	<p class="mb-5 text-center font-bold">
		You can access this page again using this link: <A href="/result/{result.task_id}"
			>{$page.url}</A
		>
	</p>
	<Heading class="mb-5" tag="h4">Job Info</Heading>
	<Table class="border">
		<TableHead>
			<TableHeadCell>Job ID</TableHeadCell>
			<TableHeadCell>Title</TableHeadCell>
			<TableHeadCell>Product</TableHeadCell>
			<TableHeadCell>Submit Date</TableHeadCell>
			<TableHeadCell>End Date</TableHeadCell>
			<TableHeadCell>Status</TableHeadCell>
		</TableHead>
		<TableBody>
			<TableBodyRow>
				<TableBodyCell
					>{#if result.success} {result.task_id}{/if}
				</TableBodyCell>
				<TableBodyCell
					>{#if result.success}{result.title}{/if}</TableBodyCell
				>
				<TableBodyCell
					>{#if result.success}{result.product}{/if}</TableBodyCell
				>
				<TableBodyCell
					>{#if result.success}{new Date(result.created_at).toLocaleString()}{/if}</TableBodyCell
				>
				{#if result.status == 0}
					<TableBodyCell>{new Date(result.end_at).toLocaleString()}</TableBodyCell>
				{:else}
					<TableBodyCell>.</TableBodyCell>
				{/if}
				<TableBodyCell>
					{#if result.success}
						{#if result.status == 0} Finished {/if}
						{#if result.status == 1} Running <Spinner size={4} />{/if}
						{#if result.status == 2} Waiting for a slot <Spinner size={4} />{/if}
						{#if result.status == -1} Cancelled {/if}
					{:else}
						No such job ID
					{/if}
				</TableBodyCell>
			</TableBodyRow>
		</TableBody>
	</Table>

	{#if result.status == 0}
		<div class="mt-8 text-center">
			<Button size="xl" on:click={() => download_result()}>Download result</Button>
		</div>
		<Heading class="mt-10 mb-5" tag="h4">Pathways</Heading>

		<div class="flex justify-between mb-5 border p-5 rounded-xl shadow">
			<Label
				>Filter pathways by molecule
				<Select class="mt-2" items={filters} bind:value={selected} />
			</Label>
			<div class="content-center">
				<Label for="direction">Directions</Label>
				<Toggle bind:checked={reverse} id="direction" class="mt-4 italic dark:text-gray-500">
					{#if reverse}
						reverse
					{:else}
						forward
					{/if}</Toggle
				>
			</div>
			<div>
				<Label>Explanation</Label>
				<P class="flex ">
					<img class="w-5" src={arrow_image_red} alt="example" />
					: exists in the retrieval DB</P
				>
				<P class="flex">
					<img class="w-5" src={arrow_image} alt="example" />
					: does not exist in the retrieval DB</P
				>
			</div>
		</div>

		<div class="border-t border-l border-r">
			{#each pathways as p, n}
				<div class="flex flex-row items-center border-b pt-5 overflow-x-scroll">
					{#if reverse}
						{#each p as m, i}
							<div class="flex-col">
								{#await mol2image(m)}
									<Spinner size={4} />
								{:then img}
									<Card
										color={selected && m === selected ? 'yellow' : 'light'}
										class="mb-5 mx-3 w-32"
										size="xs"
										img={'data:image/png;base64,' + img}
										id="b{n}-{i}"
									>
										<P class="flex flex-row justify-center text-center text-xs break-all">
											{m}
										</P></Card
									>
									<Popover class="w-64 text-sm font-light" triggeredBy="#b{n}-{i}">
										{#await pop_up(m)}
											<Spinner size={4} />
										{:then mnx}
											{#if mnx.mnx_id == null}
												<P>MNX ID is not found</P>
											{:else}
												<P>MNX ID:{mnx.mnx_id}</P>
												<P>molecule_name:{mnx.molecule_name}</P>{/if}
										{/await}
									</Popover>
								{/await}
							</div>
							{#if !last(p, i)}
								{#await rdb(m, p[i + 1])}
									<Spinner size={4} />
								{:then exist}
									<div class="flex-col w-12 mx-2 shrink-0">
										{#if exist}
											<img src={arrow_image_red} alt={m + ' to ' + p[i + 1]} />
										{:else}
											<img src={arrow_image} alt={m + ' to ' + p[i + 1]} />
										{/if}
									</div>{/await}{/if}{/each}
					{:else}
						{#each p.reverse() as m, i}
							<div class="flex-col">
								{#await mol2image(m)}
									<Spinner size={4} />
								{:then img}
									<Card
										color={selected && m === selected ? 'yellow' : 'light'}
										class="mb-5 mx-3 w-32"
										size="xs"
										img={'data:image/png;base64,' + img}
										id="b{n}-{i}"
									>
										<P class="flex flex-row justify-center text-center text-xs break-all">
											{m}
										</P></Card
									>
									<Popover class="w-64 text-sm font-light" triggeredBy="#b{n}-{i}">
										{#await pop_up(m)}
											<Spinner size={4} />
										{:then mnx}
											{#if mnx.mnx_id == null}
												<P>MNX ID is not found</P>
											{:else}
												<P>MNX ID:{mnx.mnx_id}</P>
												<P>molecule_name:{mnx.molecule_name}</P>{/if}
										{/await}
									</Popover>
								{/await}
							</div>
							{#if !last(p, i)}
								{#await rdb(m, p[i + 1])}
									<Spinner size={4} />
								{:then exist}
									<div class="flex-col w-12 mx-2 shrink-0">
										{#if exist}
											<img src={arrow_image_red} alt={m + ' to ' + p[i + 1]} />
										{:else}
											<img src={arrow_image} alt={m + ' to ' + p[i + 1]} />
										{/if}
									</div>{/await}{/if}{/each}
					{/if}
				</div>
			{/each}
		</div>
	{/if}
{:else}
	<div class="w-full text-center">
		<Spinner class="mt-20" />
	</div>
{/if}
