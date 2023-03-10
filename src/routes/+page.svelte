<script>
	import Arguments from './Arguments.svelte';
	import BuildingBlocks from './Building_Blocks.svelte';
	import RetrievalDb from './Retrieval_DB.svelte';

	let argu = true;
	let bb = false;
	let rdb = false;
</script>

<div class="h-full w-full bg-white flex flex-col items-center p-3">
	<h1 class="text-5xl font-bold p-12">Pathway explorer</h1>
	<div class="h-full w-full bg-white flex flex-col items-center p-8">
		<p>
			A short tutorial is available <a
				class="font-bold underline decoration-sky-500 text-sky-500"
				href="https://kit.svelte.dev">here</a
			>
		</p>
	</div>
	<div class="flex self-start w-11/12 ml-20 mt-5">
		<button
			class="text-xl bg-blue-500 hover:bg-blue-700 text-white font-bold w-1/6 mx-3 p-2"
			on:click={() => ((argu = true), (bb = false), (rdb = false))}
		>
			Arguments
		</button>
		<button
			class="text-xl bg-blue-500 hover:bg-blue-700 text-white font-bold w-1/6 mx-3 p-2"
			on:click={() => ((bb = true), (argu = false), (rdb = false))}
		>
			Building Blocks
		</button>
		<button
			class="text-xl bg-blue-500 hover:bg-blue-700 text-white font-bold w-1/6 mx-3 p-2"
			on:click={() => ((rdb = true), (bb = false), (argu = false))}
		>
			Retrieval DB
		</button>
	</div>
	<div class="w-11/12 h-full justify-center m-4 mt-0  border-2">
		{#if argu}
			<Arguments />
		{/if}
		{#if bb}
			<BuildingBlocks />
		{/if}
		{#if rdb}
			<RetrievalDb />
		{/if}
	</div>
</div>
