<script>
	import { Fileupload, Label } from 'flowbite-svelte';
	import { Button } from 'flowbite-svelte';

	export let files;
</script>

<div class="h-full w-full bg-white flex flex-col items-center">
	<Button class="mb-10" download="retrieval_db.csv" href="/retrieval_db.csv">Click to download retrieval DB</Button>
	<Label class="space-y-2 mb-2">
		<span>Upload retrieval DB:</span>
		<Fileupload bind:files={files} />
	</Label>
</div>
