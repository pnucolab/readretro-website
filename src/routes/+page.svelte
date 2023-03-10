<script>
	import Arguments from './Arguments.svelte';
	import BuildingBlocks from './Building_Blocks.svelte';
	import RetrievalDb from './Retrieval_DB.svelte';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import { Heading, P, A, Mark, Secondary, Button } from 'flowbite-svelte';
	import { Tabs, TabItem } from 'flowbite-svelte';
	import { load } from './fetch';
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

<Navbar let:hidden let:toggle>
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			READRetro
		</span>
	</NavBrand>
	<NavHamburger on:click={toggle} />
	<NavUl {hidden}>
		<NavLi href="/" active={true}>Pathway Explorer</NavLi>
		<NavLi href="/about">About</NavLi>
	</NavUl>
</Navbar>
<div class="px-2 sm:px-4 mb-20">
	<div class="mx-auto flex flex-col container">
		<Heading tag="h1" class="mt-5 mb-2">Pathway Explorer</Heading>
		<Heading tag="h3" class="font-light mb-5"
			>A useful webtool for prediction of retrosynthesis</Heading
		>
		<P class="mb-10"
			>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus nulla nibh, iaculis nec
			vehicula ac, semper ac eros. Aliquam felis erat, tempor sed magna a, laoreet blandit sem.
			Suspendisse ultrices tristique sapien, ut tempus felis molestie in. Nulla consequat est eget
			erat posuere, venenatis ultricies sem pulvinar. Sed justo augue, tristique sed ultricies eu,
			venenatis ut enim. Quisque faucibus malesuada libero. Phasellus non accumsan orci. Quisque non
			sagittis justo, vitae fermentum tellus. Aliquam ullamcorper dui et risus euismod finibus. Sed
			eget fringilla enim, molestie malesuada arcu. Mauris et blandit libero, eu ullamcorper metus.
			Aliquam sit amet nisi id metus tristique ultricies. Suspendisse viverra quam quis urna
			posuere, vitae laoreet orci venenatis. Morbi gravida bibendum consectetur. Praesent
			sollicitudin sagittis neque, ut tempor lectus feugiat quis.
		</P>
		<Tabs style="underline" contentClass="p-8 rounded-lg border mt-4">
			<TabItem open>
				<div slot="title" class="flex items-center gap-2">
					<svg
						aria-hidden="true"
						class="w-5 h-5"
						fill="currentColor"
						viewBox="0 0 20 20"
						xmlns="http://www.w3.org/2000/svg"
						><path
							d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"
						/></svg
					>
					Arguments
				</div>
				<Arguments />
			</TabItem>
			<TabItem>
				<div slot="title" class="flex items-center gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-5 h-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M2.25 7.125C2.25 6.504 2.754 6 3.375 6h6c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-6a1.125 1.125 0 01-1.125-1.125v-3.75zM14.25 8.625c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v8.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 01-1.125-1.125v-8.25zM3.75 16.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 01-1.125-1.125v-2.25z"
						/>
					</svg>
					Building Blocks
				</div>
				<BuildingBlocks />
			</TabItem>
			<TabItem>
				<div slot="title" class="flex items-center gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-5 h-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125"
						/>
					</svg>
					Retrieval DB
				</div>
				<!--<Toggle bind:checked={vCard} class="mt-4 italic dark:text-gray-500">Reverse</Toggle>-->
				<RetrievalDb />
			</TabItem>
		</Tabs>
		<div class="mt-8 text-center">
			<Button
				size="xl"
				on:click={() => {
					load(url).then((result) => {
						t = result.ticket;
						console.log(t);
						let url2 = 'https://retro.pnucolab.com/result?ticket=' + t;
						console.log(url2);
						load(url2).then((result) => {
							console.log(result);
						});
						console.log(t);
					});
					console.log(t);
				}}
				type="submit">Submit</Button
			>
		</div>
	</div>
</div>
