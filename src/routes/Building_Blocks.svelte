<script>
	import { Card, Button, Toggle, P, Checkbox, Label } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { load } from './fetch';
	let blocks = {};
	let mounted = false;
	let checked = [];
	function toggleChecked(i) {
		checked[i] = !checked[i];
		console.log(i);
	}
	onMount(async () => {
		const rtn = await load('https://retro.pnucolab.com/building-blocks');
		if (rtn.success) {
			blocks = rtn.building_blocks;
			checked = new Array(Object.keys(blocks).length).fill(true);
		}
		console.log(blocks);
		mounted = true;
	});
</script>

<div class="grid grid-cols-6">
	{#if mounted}
		{#each Object.keys(blocks) as block, i}
			<Card
				color="light"
				class="mb-5 mx-3"
				size="xs"
				img={'data:image/png;base64,' + blocks[block]}
			>
				<div class="flex flex-row text-center">
					<Checkbox class="mr-1" id={'m' + i} bind:checked={checked[i]} />
					<Label
						for={'m' + i}
						class="break-all font-bold tracking-tight text-gray-900 dark:text-white">{block}</Label
					>
				</div></Card
			>
		{/each}
	{/if}
</div>
