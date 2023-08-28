<script>
	import { Label, Span, Spinner } from 'flowbite-svelte';
	import { load } from './fetch';
	import Top from '../lib/Top.svelte';
	import { Card, P, A } from 'flowbite-svelte';
	import { Heading } from 'flowbite-svelte';
	import { Popover, Button, Toggle } from 'flowbite-svelte';
	import download from 'downloadjs';
	import { page } from '$app/stores';

	import arrow_image from '$lib/images/right-arrow.svg';
	import arrow_image_red from '$lib/images/right-arrow-red.svg';
	import arrow_image_green from '$lib/images/right-arrow-green.svg';
	import { onMount } from 'svelte';
	import { Select } from 'flowbite-svelte';

	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';

	export let ticket;

	let last = (a, i) => i == a.length - 1;
	let result = {};
	let loaded = false;
	let pathways = [];
	let reverse = true;
	let filters = [];
	let selected;

	const uniqueFilters = [];
	const seenValues = new Set();

	async function mol2image(mol) {
		const result = await load('mol2image?mol=' + encodeURIComponent(mol));
		return result.image;
	}

	async function get_result(ticket) {
		const data = await load('result?ticket=' + ticket);
		if (data.success) {
			if (data.status == 0) {
				pathways = [...data.pathway];
				console.log(pathways);
				let mols = [];
				for (let i = 0; i < data.pathway.length; i++) {
					for (let j = 0; j < data.pathway[i].molecules.length; j++) {
						let found_duplicate = false;
						for (let k = 0; k < mols.length; k++) {
							if (mols[k].smiles == data.pathway[i].molecules[j].smiles) {
								found_duplicate = true;
								break;
							}
						}
						if (!found_duplicate) mols.push(data.pathway[i].molecules[j]);
					}
				}
				filters = mols
					.map((m) => {
						if (Array.isArray(m)) {
							return m.map((k) => {
								const mnxInfo = k.mnx_info[0] ? k.mnx_info[0] : 'N/A';
								return {
									name: mnxInfo + ': ' + k.smiles,
									value: k.smiles
								};
							});
						} else {
							const mnxInfo = m.mnx_info[0] ? m.mnx_info[0] : 'N/A';
							return {
								name: mnxInfo + ': ' + m.smiles,
								value: m.smiles
							};
						}
					})
					.flat();

				const uniqueFilters = [];
				const seenValues = new Set();

				filters.forEach((filter) => {
					if (!seenValues.has(filter.value)) {
						seenValues.add(filter.value);
						uniqueFilters.push(filter);
					}
				});

				filters = uniqueFilters;
			} else if (data.status > 0) {
				setTimeout(() => get_result(ticket), 1000);
			}
		}
		result = data;
	}

	async function rdb(mol1, mol2) {
		const rdb = await load(
			'rdbsearch?mol1=' + encodeURIComponent(mol1) + '&mol2=' + encodeURIComponent(mol2)
		);
		console.log(rdb.existence);
		return rdb.existence;
	}

	async function get_mnx_info(mol) {
		const mnx = await load('mnxsearch?query=' + encodeURIComponent(mol));
		return mnx;
	}

	async function download_result() {
		let final_result = '';
		final_result += '#title: ' + result.title + '\n';
		final_result += '#task ID: ' + result.task_id + '\n';
		for (let i = 0; i < result.pathway.length; i++) {
			final_result += result.pathway[i].molecules.map((e) => e.smiles).join('>>') + '\n';
		}
		download(final_result, 'result.txt', 'text/plain');
	}

	onMount(async () => {
		await get_result(ticket);
		loaded = true;
	});

	$: {
		if (selected) {
			pathways = result.pathway.filter((p) => p.molecules.includes(selected));
			pathways = pathways.concat(result.pathway.filter((p) => !p.molecules.includes(selected)));
		} else {
			pathways = result.pathway;
		}
	}
</script>

<Top />

{#if loaded}
	<p class="mb-5 text-center font-bold break-all">
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
					>{#if result.success}{new Date(
							result.created_at + 'Z'
						).toLocaleString()}{/if}</TableBodyCell
				>
				{#if result.status == 0}
					<TableBodyCell>{new Date(result.end_at + 'Z').toLocaleString()}</TableBodyCell>
				{:else}
					<TableBodyCell>.</TableBodyCell>
				{/if}
				<TableBodyCell>
					{#if result.success}
						{#if result.status == 0} Finished {/if}
						{#if result.status == 1} Running <Spinner size={4} />{/if}
						{#if result.status == 2} Waiting for a slot <Spinner size={4} />{/if}
						{#if result.status == -1} Cancelled {/if}
						{#if result.status == -2} Error {/if}
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
			<Label class="w-1/4">
				Highlight pathways by molecule
				<Select class="mt-2" items={filters} bind:value={selected} />
			</Label>
			<div class="content-center w-1/4">
				<Label for="direction">Directions</Label>
				<Toggle bind:checked={reverse} id="direction" class="mt-4 italic dark:text-gray-500">
					{#if reverse}
						reverse
					{:else}
						forward
					{/if}
				</Toggle>
			</div>
			<div class="w-1/4">
				<Label>Explanation</Label>
				<P class="flex ">
					<img class="w-5" src={arrow_image} alt="example" />
					: exists in the retrieval DB</P
				>
				<P class="flex">
					<img class="w-5" src={arrow_image_red} alt="example" />
					: does not exist in the retrieval DB</P
				>
				<P class="flex">
					<img class="w-5" src={arrow_image_green} alt="example" />
					: pathway retriever</P
				>
			</div>
		</div>

		<div class="border-t border-l border-r">
			{#if pathways.length === 0}
				<div class="flex items-center justify-center border-b py-5">No pathways found.</div>
			{:else}
				{#each pathways as p, n}
					<div class="flex justify-left items-center border-b pt-5 overflow-x-scroll ">
						<div
							class=" flex justify-left items-center  {reverse ? 'flex-row' : 'flex-row-reverse'}"
						>
							{#each p.molecules as m, i}
								{#if m.length > 1}
									<div class="flex-col">
										{#each m as k}
											<div class="flex-col">
												<Card
													color={selected && k.smiles === selected
														? 'yellow'
														: k.mnx_info[0]
														? 'blue'
														: 'red'}
													class="mb-5 mx-3 w-44"
													size="xs"
													img={'data:image/png;base64,' + k.image}
													id="b{n}-{i}"
												>
													<P class="break-all text-center mb-2">
														{#if k.mnx_info[0]}
															<span class="font-bold text-xs">
																{k.mnx_info[1]}<br />(<a
																	href="https://metanetx.org/chem_info/{k.mnx_info[0]}"
																	target="_blank">{k.mnx_info[0]})</a
																>
															</span>
														{:else}
															<span class="font-bold text-xs"> N/A </span>
														{/if}
													</P>
													<P class="flex flex-row justify-center text-center break-all">
														<span class="text-xs">{k.smiles}</span>
													</P>
												</Card>
											</div>
										{/each}
									</div>
								{:else}
									<div class="flex-col">
										<Card
											color={selected && m.smiles === selected
												? 'yellow'
												: m.mnx_info[0]
												? 'blue'
												: 'red'}
											class="mb-5 mx-3 w-44"
											size="xs"
											img={'data:image/png;base64,' + m.image}
											id="b{n}-{i}"
										>
											<P class="break-all text-center mb-2">
												{#if m.mnx_info[0]}
													<span class="font-bold text-xs">
														{m.mnx_info[1]}<br />(<a
															href="https://metanetx.org/chem_info/{m.mnx_info[0]}"
															target="_blank">{m.mnx_info[0]})</a
														>
													</span>
												{:else}
													<span class="font-bold text-xs"> N/A </span>
												{/if}
											</P>
											<P class="flex flex-row justify-center text-center break-all">
												<span class="text-xs">{m.smiles}</span>
											</P>
										</Card>
									</div>
									{#if !last(p.molecules, i)}
										<div class="flex-col w-20 mx-2 shrink-0">
											{#if p.kegg_reactions}
												{#if parseInt(p.scores[i]) === 1}
													<a href="www.kegg.jp/entry/{p.kegg_reactions[i].rname}"
														>{p.kegg_reactions[i].rname}</a
													>
													<img class="relative" src={arrow_image} alt={m + ' to ' + p[i + 1]} />
													{#if p.kegg_reactions[i].ec.length > 0}<div class="w-20 absolute ">
															<P class="flex w-full justify-center text-center" weight="medium"
																>EC: {p.kegg_reactions[i].ec}</P
															>
														</div>{/if}
												{:else}
													<P href="www.kegg.jp/entry/{p.kegg_reactions[i].rname}"
														>{p.kegg_reactions[i].rname}</P
													>
													<img class="relative" src={arrow_image_red} alt={m + ' to ' + p[i + 1]} />
													{#if p.kegg_reactions[i].ec.length > 0}<div class="absolute">
															<P
																class="flex w-full justify-center text-center break-all"
																weight="medium">EC: {p.kegg_reactions[i].ec}</P
															>
														</div>{/if}
												{/if}
											{:else if parseInt(p.scores[i]) === 1}
												<img src={arrow_image} alt={m + ' to ' + p[i + 1]} />
											{:else}
												<img src={arrow_image_red} alt={m + ' to ' + p[i + 1]} />
											{/if}
										</div>
									{/if}
								{/if}
							{/each}
						</div>
						{#if p.kegg_path}
							<div class="flex-col w-12 mx-2 shrink-0">
								<img src={arrow_image_green} alt="green" />
							</div>
							<Card
								color="green"
								href="https://www.{p.kegg_path}"
								target="_blank"
								padding="sm"
								size="lg"><Heading tag="h3">{p.kegg}</Heading></Card
							>{/if}
					</div>
				{/each}
			{/if}
		</div>
	{/if}
{:else}
	<div class="w-full text-center">
		<Spinner class="mt-20" />
	</div>
{/if}
