<script>
	import { Fileupload, Label } from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';

	export let file;
</script>

<div class="h-full w-full bg-white flex flex-col items-center">
	<Button class="mb-10" download="train_canonicalized.txt" href="/train_canonicalized.txt">Click to download retrieval DB</Button>
	<Label class="space-y-2 mb-2">
		<span>Upload retrieval DB:</span>
		<Fileupload bind:value={file} />
	</Label>
</div>
