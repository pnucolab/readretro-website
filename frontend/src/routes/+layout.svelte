<script>
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';

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

<div class="px-2 sm:px-4">
	<div class="mx-auto flex mb-20 flex-col container">
		<slot />
	</div>
</div>