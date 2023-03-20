<script>
	import { Input, Label, Heading, Toggle } from 'flowbite-svelte';

	export let title;
	export let pathway;
	export let iterations;
	export let beam_size;
	export let expansions;
	export let on;
	export let target_molecule;
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
		<Input
			bind:value={iterations}
			type="number"
			id="iteration"
			placeholder="100"
			required
		/>
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
	<div class="mb-6">
		<Label for="retriever" class="mb-2">Retriever usage</Label>
		<Toggle bind:checked={on} id="retriever" class="mt-4 italic dark:text-gray-500">
			{#if on}
				on
			{:else}
				off
			{/if}</Toggle
		>
	</div>
</div>
