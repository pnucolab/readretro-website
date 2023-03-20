<script>
	import { Card, Checkbox, Label } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { load } from './fetch';
	import { Button, Modal, Heading, Input, P } from 'flowbite-svelte';

	let defaultModal = false;
	let blocks = {};
	let mounted = false;
	let checked = [];
	let custom_checked = [];
	let custom_smiles = [];
	let s = '';
	export let smiles = [];
	$: {
		smiles = custom_smiles
			.map((x, i) => (custom_checked[i] ? x.smiles : ''))
			.filter((x) => x != '');
		for (let i = 0; i < checked.length; i++) {
			for (let j = 0; j < checked[i].length; j++) {
				if (checked[i][j]) {
					smiles.push(blocks[i].molecules[j].smiles);
				}
			}
		}
	}
	onMount(async () => {
		const rtn = await load('building-blocks');
		if (rtn.success) {
			blocks = rtn.building_blocks;
			for (let i = 0; i < blocks.length; i++) {
				checked.push(new Array(blocks[i].molecules.length).fill(true));
			}
		}
		mounted = true;
	});

	async function add_smiles() {
		if (s != '') {
			custom_smiles.push({ smiles: s, image: (await load('mol2image?mol=' + s)).image });
			custom_checked.push(true);
			s = '';
			custom_smiles = custom_smiles;
		}
	}
</script>

{#if mounted}
	<Heading tag="h5" class="mb-3">Custom blocks</Heading>
	<div
		class="grid gap-5 grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 mb-5"
	>
		{#each custom_smiles as smiles, i}
			<Card color="light" class="w-full" img={'data:image/png;base64,' + smiles.image}>
				<div class="flex flex-row text-center">
					<Checkbox bind:checked={custom_checked[i]} />
					<div class="flex flex-col flex-grow">
						<P class="text-sm ml-1">{smiles.smiles}</P>
					</div>
				</div>
			</Card>
		{/each}

		<Button on:click={() => (defaultModal = true)}>
			<div class="h-64 flex items-center">
				<span class="text-4xl ">+</span>
			</div></Button
		>
	</div>
	<Modal title="Add custom smiles" bind:open={defaultModal} autoclose>
		<Label for="smiles">Enter SMILES</Label>
		<Input bind:value={s} type="text" id="smiles" required />
		<svelte:fragment slot="footer">
			<Button on:click={() => add_smiles()}>Add</Button>
			<Button on:click={() => (s = '')} color="alternative">Cancel</Button>
		</svelte:fragment>
	</Modal>
	{#each blocks as cl, n}
		<div class="mb-10">
			<Heading tag="h5" class="mb-3">{cl.class}</Heading>
			<div
				class="grid gap-5 grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6"
			>
				{#each cl.molecules as mol, i}
					<Card color="light" class="w-full" img={'data:image/png;base64,' + mol.image}>
						<div class="flex flex-row text-center">
							<Checkbox class="mr-1" id="m-{n}-{i}" bind:checked={checked[n][i]} />
							<Label
								for="m-{n}-{i}"
								class="break-all font-bold tracking-tight text-gray-900 dark:text-white"
								>{mol.name}</Label
							>
						</div></Card
					>
				{/each}
			</div>
		</div>{/each}
{/if}
