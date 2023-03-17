<script>
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import { Heading, P } from 'flowbite-svelte';

	import './styles.css';
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

<div class="mx-auto flex flex-col container">
	<Heading tag="h2" class="mt-5 mb-2">Pathway Explorer</Heading>
	<Heading tag="h5" class="font-light mb-5"
		>A useful webtool for prediction of retrosynthesis</Heading
	>
	<P class="mb-10"
		>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus nulla nibh, iaculis nec
		vehicula ac, semper ac eros. Aliquam felis erat, tempor sed magna a, laoreet blandit sem.
		Suspendisse ultrices tristique sapien, ut tempus felis molestie in. Nulla consequat est eget
		erat posuere, venenatis ultricies sem pulvinar.
	</P>
	
	<div class="mb-20">
		<slot />
	</div>
</div>