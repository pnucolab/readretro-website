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
	let weight;
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

				/*function sumWeightsWithNullCarryover(matrix) {
					const numRows = matrix.length;
					const numCols = matrix[0].length;
					const colSums = new Array(numCols).fill(0);
					const pastSums = new Array(numCols).fill(0); // 누적용 (carry over)

					// 각 row에 대해
					for (let row = 0; row < numRows; row++) {
						let currentRow = matrix[row];
						let rowValues = [];

						for (let col = 0; col < numCols; col++) {
							const node = currentRow[col];
							let w = 0;

							if (node && node.weight != null) {
								const num = parseFloat(node.weight);
								w = isNaN(num) ? 0 : num;

								// null이었다가 값이 처음 나타난 경우 → carry over
								if (pastSums[col] === 0 && row > 0) {
									let carry = 0;
									for (let prevRow = 0; prevRow < row; prevRow++) {
										for (let otherCol = 0; otherCol < numCols; otherCol++) {
											if (otherCol !== col) {
												const n = matrix[prevRow][otherCol];
												if (n && n.weight != null) {
													const v = parseFloat(n.weight);
													carry += isNaN(v) ? 0 : v;
												}
											}
										}
									}
									colSums[col] += carry;
									pastSums[col] += carry;
								}

								colSums[col] += w;
								pastSums[col] += w;
							}
						}
					}
					console.log('colSums:', colSums);
					return colSums;
				}
				function negativeLogClippedScores(scores) {
					return scores.map((score) => {
						const clipped = Math.min(Math.max(score, 1e-3), 1.0);
						return 0.0 - Math.log(clipped);
					});
				}*/

				function sumWeightsWithNullCarryover(matrix) {
					const numRows = matrix.length;
					const numCols = matrix[0].length;
					const colSums = new Array(numCols).fill(0);
					const pastSums = new Array(numCols).fill(0);
					function negativeLogClippedScore(scores) {
						const clipped = Math.min(Math.max(scores, 1e-3), 1.0);
						return 0.0 - Math.log(clipped);
					}

					for (let row = 0; row < numRows; row++) {
						let currentRow = matrix[row];

						for (let col = 0; col < numCols; col++) {
							const node = currentRow[col];
							if (node && node.weight != null && !node.kegg_reaction) {
								const num = parseFloat(node.weight);
								const rawWeight = isNaN(num) ? 0 : num;
								const negLog = negativeLogClippedScore(rawWeight);

								if (pastSums[col] <= 1e-8 && row > 0) {
									let carry = 0;
									for (let prevRow = 0; prevRow < row; prevRow++) {
										for (let otherCol = 0; otherCol < numCols; otherCol++) {
											if (otherCol !== col) {
												const n = matrix[prevRow][otherCol];
												if (n && n.weight != null) {
													const v = parseFloat(n.weight);
													const w = isNaN(v) ? 0 : v;
													carry += negativeLogClippedScore(w);
												}
											}
										}
									}
									colSums[col] += carry;
									pastSums[col] += carry;
								}

								colSums[col] += negLog;
								pastSums[col] += negLog;
							}
						}
					}

					return colSums;
				}

				const summedWeightsList = pathways.map((pathway) => {
					return sumWeightsWithNullCarryover(pathway);
				});
				weight = summedWeightsList;
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

				filters = mols.map((m) => {
					const mnxInfo = m.kegg ? m.kegg : 'N/A';
					return {
						name: mnxInfo + ': ' + (m.common_name ? m.common_name : m.smiles),
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
		console.log(result);
		let final_result = '';
		final_result += '#title: ' + result.title + '\n';
		final_result += '#task ID: ' + result.task_id + '\n';
		for (let item of result.raw_result) {
			final_result += item + '\n';
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
					<div class="flex justify-left border-b pt-5 overflow-x-scroll p-5">
						<div class=" flex justify-left  {reverse ? 'flex-row' : 'flex-row-reverse'} ">
							{#each p as m, i}
								<div class="flex flex-col">
									{#each m as k, j}
										<div
											class="flex items-center {reverse ? 'flex-row' : 'flex-row-reverse'} flex-1"
										>
											{#if i === 0}
												<p
													style="
											font-weight: bold;
											font-size: 0.9rem;
											color: #4A90E2;
											margin: 4px 20px 4px 12px;  
										  "
												>
													{parseFloat(weight[n][j]).toFixed(4)}
												</p>
											{/if}
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
																	{#if r && r[n] && r[n][i - 1] && r[n][i - 1][j] && r[n][i - 1][j][0]}
																		{#each r[n][i - 1][j][0] as m}
																			<a
																				class="text-center "
																				href="http://www.kegg.jp/entry/{m}"
																				target="_blank">{m}</a
																			>{/each}{/if}
																	<div class="relative inline-block">
																		<img
																			src={arrow_image}
																			alt={`${m} to ${k}`}
																			class="w-32 h-auto"
																		/>
																		<span
																			class="absolute inset-0 flex items-center justify-center text-white font-bold"
																		>
																			{k.weight}
																		</span>
																	</div>

																	{#if r && r[n] && r[n][i - 1] && r[n][i - 1][j] && r[n][i - 1][j][1]}
																		{#each r[n][i - 1][j][1] as m}
																			<a
																				class="text-center "
																				href="http://www.brenda-enzymes.org/enzyme.php?ecno={m}"
																				target="_blank">EC: {m}</a
																			>{/each}{/if}
																{:else}
																	{#if r && r[n] && r[n][i - 1] && r[n][i - 1][j] && r[n][i - 1][j][0]}
																		{#each r[n][i - 1][j][0] as m}
																			<a
																				class="text-center "
																				href="http://www.kegg.jp/entry/{m}"
																				target="_blank">{m}</a
																			>{/each}{/if}
																	<div class="relative inline-block">
																		<img
																			src={arrow_image_red}
																			alt={`${m} to ${k}`}
																			class="w-32 h-auto"
																		/>
																		<span
																			class="absolute inset-0 flex items-center justify-center text-white font-bold"
																		>
																			{k.weight}
																		</span>
																	</div>
																	{#if r && r[n] && r[n][i - 1] && r[n][i - 1][j] && r[n][i - 1][j][1]}
																		{#each r[n][i - 1][j][1] as m}
																			<a
																				class="text-center "
																				href="http://www.brenda-enzymes.org/enzyme.php?ecno={m}"
																				target="_blank">EC: {m}</a
																			>{/each}{/if}
																{/if}
															{:else if parseInt(k.weight) === 1}
																<div class="relative inline-block">
																	<img src={arrow_image} alt={`${m} to ${k}`} class="w-32 h-auto" />
																	<span
																		class="absolute inset-0 flex items-center justify-center text-white font-bold"
																	>
																		{k.weight}
																	</span>
																</div>
															{:else}
																<div class="relative inline-block">
																	<img
																		src={arrow_image_red}
																		alt={`${m} to ${k}`}
																		class="w-32 h-auto"
																	/>
																	<span
																		class="absolute inset-0 flex items-center justify-center text-white font-bold"
																	>
																		{k.weight}
																	</span>
																</div>
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
