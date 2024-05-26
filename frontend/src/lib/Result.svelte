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
	import white from '$lib/images/white.png';
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
	let reaction = [];
	let selected;
	let r;
	let r2;
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

				for (let i = 0; i < pathways.length; i++) {
					reaction[i] = [];
					for (let j = 0; j < pathways[i].length; j++) {
						for (let k = 0; k < pathways[i][j].length; k++) {
							if (pathways[i][j][k] && !pathways[i][j][k].smiles.includes('kegg')) {
								pathways[i][j][k].smiles = pathways[i][j][k].smiles.replace('*', 'CoA');
								mols.push(pathways[i][j][k]);
								reaction[i].push(pathways[i][j][k].reaction);
							}
						}
					}
				}
				r = pathways.map((p) => {
					return p.map((k) => {
						return k.map((j) => {
							if (j && !j.smiles.includes('kegg')) {
								return j.reaction;
							}
							return [null, null];
						});
					});
				});

				console.log(r, 'r');

				function getLastNonNullValue(array) {
					let filteredArray = array.filter((item) => item !== null);
					return filteredArray.length > 0 ? filteredArray[filteredArray.length - 1] : [null, null];
				}

				function fillMissingValues(arr) {
					for (let i = 1; i < arr.length; i++) {
						for (let j = 0; j < arr[i].length; j++) {
							if (arr[i][j] === [null, null]) {
								arr[i][j] =
									arr[i + 1][j] !== [null, null] ? getLastNonNullValue(arr[i]) : [null, null];
							}
						}
					}
					return arr;
				}

				r2 = fillMissingValues(r);
				function getDifferentIndicesExtended(array1, array2) {
					let differentIndices = [];

					let maxLength = Math.max(array1.length, array2.length);

					for (let i = 0; i < maxLength; i++) {
						if (array1[i] !== array2[i]) {
							differentIndices.push(i);
						}
					}

					return differentIndices;
				}
				console.log('r2', r2);
				let differentIndicesExtended = getDifferentIndicesExtended(r, r2);

				console.log(differentIndicesExtended);
				filters = mols.map((m) => {
					const mnxInfo = m.kegg ? m.kegg : 'N/A';
					return {
						name: mnxInfo + ': ' + m.smiles,
						value: m.smiles
					};
				});

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

	async function download_result() {
		let final_result = '';
		final_result += '#title: ' + result.title + '\n';
		final_result += '#task ID: ' + result.task_id + '\n';
		if (result.pathway) {
			for (let i = 0; i < result.pathway.length; i++) {
				for (let j = 0; j < result.pathway[i].length; j++) {
					console.log(result.pathway[i][j], 'gg');
					if (result.pathway[i][j].length) {
						continue;
					}
					result.pathway[i][j].map((e) => {
						if (e !== null && e.smiles !== null) {
							final_result += e.smiles + '.';
						}
					});
					final_result += '>>';
				}
				final_result += '\n';
			}
		}
		download(final_result, 'result.txt', 'text/plain');
	}

	async function download_result2() {
		let final_result = '';
		final_result += '#title: ' + result.title + '\n';
		final_result += '#task ID: ' + result.task_id + '\n';

		if (result.pathway) {
			for (let i = 0; i < result.pathway.length; i++) {
				final_result += i + ': ';
				for (let j = 0; j < result.pathway[i].length; j++) {
					let currentArray = result.pathway[i][j];
					if (currentArray === null || currentArray.length === 0) {
						continue;
					}

					for (let k = 0; k < currentArray.length; k++) {
						let e = currentArray[k];
						if (e !== null && e.smiles !== null) {
							if (k < currentArray.length - 1 && currentArray[k - 1] === null) {
								final_result += '--.';
							}
							final_result += e.smiles;
							if (k < currentArray.length - 1 && currentArray[k + 1] !== null) {
								final_result += '.';
							}
						}
					}

					if (j < result.pathway[i].length - 1) {
						final_result += ' >> ';
					}
				}
				final_result += '\n';
			}
		}

		download(final_result, 'result.txt', 'text/plain');
	}

	onMount(async () => {
		await get_result(ticket);
		loaded = true;
	});

	$: {
		if (selected) {
			pathways = result.pathway.filter((p) => {
				return p.some((k) => k.some((j) => j && j.smiles && j.smiles === selected));
			});

			pathways = pathways.concat(
				result.pathway.filter((p) => {
					return !p.some((k) => k.some((j) => j && j.smiles && j.smiles === selected));
				})
			);
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
			<Button size="xl" on:click={() => download_result2()}>Download result</Button>
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
					<P>n:{n}</P>
					<div class="flex justify-left border-b pt-5 overflow-x-scroll p-5">
						<div class=" flex justify-left  {reverse ? 'flex-row' : 'flex-row-reverse'} ">
							{#each p as m, i}
								<P>p: {m}, {i}</P>
								<div class="flex flex-col">
									{#each m as k, j}
										<P>m: {k}, {j}</P>
										<div
											class="flex items-center {reverse ? 'flex-row' : 'flex-row-reverse'} flex-1"
										>
											{#if k}
												{#if i != 0}
													<div class="flex flex-row w-24 mx-2 shrink-0 h-fit self-center">
														<div class="flex flex-col h-fit">
															{#if k.smiles.includes('kegg')}<img
																	src={arrow_image_green}
																	class="px-2"
																	alt={m + ' to ' + k}
																/>
															{:else if k.reaction}
																{#if parseInt(k.weight) === 1}
																	{#if r[n][i - 1][j][0]}
																		{#each r[n][i - 1][j][0] as m}<a
																				class="text-center "
																				href="http://www.kegg.jp/entry/{m}"
																				target="_blank">{m}</a
																			>{/each}{/if}
																	<img src={arrow_image} class="px-2" alt={m + ' to ' + k} />
																	{#if r[n][i - 1][j][1]}
																		{#each r[n][i - 1][j][1] as m}<a
																				class="text-center "
																				href="http://www.brenda-enzymes.org/enzyme.php?ecno={m}"
																				target="_blank">EC: {m}</a
																			>{/each}{/if}
																{:else}
																	{#if r[n][i - 1][j][0]}
																		{#each r[n][i - 1][j][0] as m}<a
																				class="text-center "
																				href="http://www.kegg.jp/entry/{m}"
																				target="_blank">{m}</a
																			>{/each}{/if}
																	<img src={arrow_image_red} class="px-2" alt={m + ' to ' + k} />
																	{#if r[n][i - 1][j][1]}
																		{#each r[n][i - 1][j][1] as m}<a
																				class="text-center "
																				href="http://www.brenda-enzymes.org/enzyme.php?ecno={m}"
																				target="_blank">EC: {m}</a
																			>{/each}{/if}
																{/if}
															{:else if parseInt(k.weight) === 1}
																<img src={arrow_image} class="px-2" alt={m + ' to ' + k} />
															{:else}
																<img src={arrow_image_red} class="px-2" alt={m + ' to ' + k} />
															{/if}
														</div>
													</div>
												{/if}
												{#if k.kegg_reaction}
													<Card
														color="green"
														href="https://www.{k.smiles}"
														class="mb-5 mx-3 w-44 h-fit"
														target="_blank"
														padding="sm"
														size="lg"
														><Heading
															class="flex items-center  justify-items-center text-2xl font-bold tracking-tight text-gray-900 dark:text-white break-all"
															tag="h5">{k.kegg_reaction}</Heading
														>
													</Card>
												{:else}
													<Card
														color={selected && k.smiles === selected
															? 'yellow'
															: k.kegg
															? 'blue'
															: 'red'}
														class="mb-5 mx-3 w-44 h-fit"
														size="xs"
														img={'data:image/png;base64,' + k.image}
														id="b{n}-{i}"
													>
														<P class="break-all text-center mb-2">
															{#if k.kegg}
																<span class="font-bold text-xs">
																	<a href="https://www.kegg.jp/entry/{k.kegg}" target="_blank"
																		>{k.kegg}</a
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
												{/if}
											{:else}
												<Card
													color={'gray'}
													class="mb-5 mx-3 w-44 h-80 invisible "
													padding="none"
													size="xs"
													img={white}
													id="b{n}-{i}"
												>
													<P class="break-all text-center mb-2">
														<span class="font-bold text-xs"> N/A </span>
													</P>
													<P class="flex flex-row justify-center text-center break-all">
														<span class="text-xs">N/A</span>
													</P>
												</Card>
											{/if}
										</div>
									{/each}
								</div>
							{/each}
						</div>
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
