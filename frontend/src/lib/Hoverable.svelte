<script>
	import { fade } from 'svelte/transition'
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    import { load } from './fetch';
	
	export let mol; 
    
	let hovering = false

	async function pop_up(mol) {
		hovering = true
		const mnx = await load('mnxsearch?query=' + mol);
		console.log(mnx)
		return mnx.mnx_id
	}
	const leave = () => (hovering = false)

</script>

<div class="relative" on:mouseenter={pop_up(mol)} on:mouseleave={leave}>
	{#if hovering}
    <div in:scale={{duration: 150, easing: quintOut, opacity: 0}}
				 class="absolute border shadow-xl top-4 left-8 z-50 bg-white shadow-xl rounded-lg p-2 w-48">
			{#await pop_up(mol)}
				<p class="text-sm flex items-center">
					<span class="ml-2">loading...</span>
			  </p>
			{:then details}
			  <div in:fade={{duration: 150}}>
					{details}
			  </div>
			{/await}
		</div>
	{/if}
</div>