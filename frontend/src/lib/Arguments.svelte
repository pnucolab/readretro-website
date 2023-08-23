<script>
	import { Input, Label, Heading, Toggle } from 'flowbite-svelte';
	import { Button, Dropdown, DropdownItem, Chevron, Radio, P } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	export let model = 'Ensemble';
	export let title;
	export let pathway;
	export let iterations;
	export let beam_size;
	export let expansions;
	export let retrieval;
	export let target_molecule;
	export let path_retrieval;

	$: {
		if (model === 'Retriever only') {
			retrieval = true;
		}
		if (model === 'Retriever only' && !retrieval) {
			retrieval = true;
		}
	}
</script>

<Heading tag="h4" class="mb-4">Experiment Information</Heading>
<div class="px-5">
	<div class="mb-6">
		<Label for="title" class="mb-2">Title</Label>
		<Input bind:value={title} type="text" id="title" placeholder="Untitled" />
	</div>
	<div class="mb-6">
		<Label for="target" class="mb-2">Target molecule (in SMILES)</Label>
		<Input
			bind:value={target_molecule}
			type="text"
			id="target"
			placeholder="CCC1=CC2CC3(C1N(C2)CCC4=C3NC5=CC=CC=C45)C(=O)OC"
			required
		/>
	</div>
</div>
<Heading tag="h4" class="mb-4">Options</Heading>
<div class="px-5">
	<div class="mb-6">
		<Label for="iteration" class="mb-2">Number of iterations</Label>
		<Input bind:value={iterations} type="number" id="iteration" placeholder="100" required />
	</div>
	<div class="mb-6">
		<Label for="pathway" class="mb-2">Number of pathway generation</Label>
		<Input bind:value={pathway} type="number" id="pathway" placeholder="10" />
	</div>
	<div class="mb-6">
		<Label for="expansions" class="mb-2">Number of expansions</Label>
		<Input bind:value={expansions} type="number" id="expansions" placeholder="10" />
	</div>
	<div class="mb-6">
		<Label for="beam" class="mb-2">Beam size</Label>
		<Input bind:value={beam_size} type="number" id="beam" placeholder="10" required />
	</div>
	<div class="mb-6 flex">
		<div class="mr-10">
			<Label for="retriever" class="mb-2">Reaction Retriever</Label>
			<Toggle bind:checked={retrieval} id="retriever" class="mt-4 italic dark:text-gray-500">
				{#if retrieval}
					on
				{:else}
					off
				{/if}</Toggle
			>
		</div>
		<div class="mr-10">
			<Label for="Pathway_retriever" class="mb-2">Pathway Retriever</Label>
			<Toggle
				bind:checked={path_retrieval}
				id="Pathway_retriever"
				class="mt-4 italic dark:text-gray-500"
			>
				{#if path_retrieval}
					on
				{:else}
					off
				{/if}</Toggle
			>
		</div>
		<div>
			<Label for="retriever" class="mb-2">model type</Label>
			<Button><Chevron>{model}</Chevron></Button>
			<Dropdown class="w-44 p-3 space-y-3 text-sm">
				<li>
					<Radio name="group1" bind:group={model} value="Ensemble">Ensemble</Radio>
				</li>
				<li>
					<Radio name="group1" bind:group={model} value="Retroformer">Retroformer</Radio>
				</li>
				<li>
					<Radio name="group1" bind:group={model} value="Graph2SMILES">Graph2SMILES</Radio>
				</li>
				<li>
					<Radio name="group1" bind:group={model} value="Retriever only">Retriever only</Radio>
				</li>
			</Dropdown>
		</div>
	</div>
</div>
