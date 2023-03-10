<script>
	import { Alert } from 'flowbite-svelte';
	import { Spinner } from 'flowbite-svelte';
	import {Heading} from 'flowbite-svelte';
	export let result;
	let status = "Running";
	if (result.success) {
		if (result.status == 0) {
			status = "Finished";
		} else if (result.status == 1) {
			status = "Canceled";
		} else if (result.status == 2) {
			status = "Running";
		}
	} else {
		status = "Failed";
	}
	import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
</script>
<Heading class="mb-5" tag='h4'>Job Info</Heading>
  <Table class="border">
	<TableHead>
	  <TableHeadCell>Job ID</TableHeadCell>
	  <TableHeadCell>Title</TableHeadCell>
	  <TableHeadCell>Submit Date</TableHeadCell>
	  <TableHeadCell>End Date</TableHeadCell>
	  <TableHeadCell>Status</TableHeadCell>
	</TableHead>
	<TableBody>
	  <TableBodyRow>
		<TableBodyCell>1</TableBodyCell>
		<TableBodyCell>2</TableBodyCell>
		<TableBodyCell>3</TableBodyCell>
		<TableBodyCell>today</TableBodyCell>
		<TableBodyCell>{status} {#if result.status == 2} <Spinner size={4} />{/if}</TableBodyCell>
		
	  </TableBodyRow>
	</TableBody>
  </Table>

{#if result.status == 0}

<Heading class="mt-10 mb-5" tag='h4'>Pathways</Heading>

<Table class="border">
	<TableHead>
	  <TableHeadCell>Pathway</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each result.pathway as p}
			<TableBodyRow>
		<TableBodyCell>{p}</TableBodyCell>
	  </TableBodyRow>
		{/each}
	  
	</TableBody>
  </Table>
{/if}
