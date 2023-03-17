<script>
	import { Spinner } from 'flowbite-svelte';
	import { load } from './fetch';
	import { Card, Button, Toggle, P, Checkbox, Label } from 'flowbite-svelte';
	import { Heading } from 'flowbite-svelte';
	export let result;
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	let last = (a, i) => i == a.length - 1;
	async function mol2image(mol) {
		const result = await load('https://retro.pnucolab.com/mol2image?mol=' + mol);
		return result.image;
	}

	import arrow_image from '$lib/images/right-arrow.svg';
</script>

<Heading class="mb-5" tag="h4">Job Info</Heading>
<Table class="border">
	<TableHead>
		<TableHeadCell>Job ID</TableHeadCell>
		<TableHeadCell>Product</TableHeadCell>
		<TableHeadCell>Submit Date</TableHeadCell>
		<TableHeadCell>End Date</TableHeadCell>
		<TableHeadCell>Status</TableHeadCell>
	</TableHead>
	<TableBody>
		<TableBodyRow>
			<TableBodyCell>{result.task_id}</TableBodyCell>
			<TableBodyCell>{result.product}</TableBodyCell>
			<TableBodyCell>{result.created_at}</TableBodyCell>
			{#if result.status == 0}
				<TableBodyCell>{result.end_at}</TableBodyCell>
			{:else}
				<TableBodyCell>.</TableBodyCell>
			{/if}
			<TableBodyCell>
				{#if result.success}
					{#if result.status == 0} Finished {/if}
					{#if result.status == 1} Running <Spinner size={4} />{/if}
					{#if result.status == 2} Waiting for a slot <Spinner size={4} />{/if}
				{:else}
					Failed (server error)
				{/if}
			</TableBodyCell>
		</TableBodyRow>
	</TableBody>
</Table>

{#if result.status == 0}
	<Heading class="mt-10 mb-5" tag="h4">Pathways</Heading>

	<Table class="border">
		<TableHead>
			<TableHeadCell>Pathway</TableHeadCell>
		</TableHead>
		<TableBody>
			{#each result.pathway as p}
				<TableBodyRow>
					<TableBodyCell>
						<div class="flex flex-row items-center">
							{#each p as m, i}
								<div class="flex-col">
									{#await mol2image(m)}
										<Spinner size={4} />
									{:then img}
										<Card
											color="light"
											class="mb-5 mx-3 w-32"
											size="xs"
											img={'data:image/png;base64,' + img}
										>
											<P class="flex flex-row justify-center text-center text-xs break-all">
												{m}
											</P></Card
										>
									{/await}
								</div>
								{#if !last(p, i)}
									<div class="flex-col w-12 mx-2">
										<img src={arrow_image} alt={m + ' to ' + p[i + 1]} />
									</div>{/if}{/each}
						</div></TableBodyCell
					>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
{/if}
