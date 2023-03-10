<script>
	import Select from 'svelte-select';

	import { load } from './fetch';
	import Result from './Result.svelte';
	import { Input, Label, Helper, Checkbox,Button, A, Heading } from 'flowbite-svelte';

	/**
	 * @type {any}
	 */
	let pathway = { value: 9, label: 10 };
	let iterations = { value: 99, label: 100 };
	let beam_size = { value: 49, label: 50 };
	let on = true;
	let off = false;
	let target_molecule = { label: '', value: '' };
	let retrieval = on ? true : false;
	let url =
		'https://retro.pnucolab.com/run?product=' +
		target_molecule.value +
		'&route_topk=' +
		pathway.label +
		'&iterations=' +
		iterations.label +
		'&beam_size=' +
		beam_size.label +
		'&retrieval=' +
		retrieval;
	/**
	 * @type {string | null}
	 */
	let t = null;
</script>
<form>
	<Heading tag="h4" class="mb-4">Target molecule</Heading>
	<div class="px-5">
	<div class="mb-6">
	  <Label for="target" class="mb-2">Target molecule (in SMILES)</Label>
	  <Input type="text" id="target" placeholder="O=C1C=C2C=CC(O)CC2O1" required />
	</div>
</div>
	<Heading tag="h4" class="mb-4">Options</Heading>
	<div class="px-5">
	<div class="mb-6">
	  <Label for="pathway" class="mb-2">Number of pathway generation</Label>
	  <Input type="number" id="pathway" placeholder="10" />
	</div>

	<div class="mb-6">
	  <Label for="iteration" class="mb-2">Number of iterations</Label>
	  <Input type="number" id="iteration" placeholder="100" required />
	</div>
	
	<div class="mb-6">
		<Label for="beam" class="mb-2">Beam size</Label>
		<Input type="number" id="beam" placeholder="50" required />
	  </div>
	</div>
  </form>

