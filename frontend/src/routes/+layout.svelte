<script>
	import { page } from '$app/stores';
	import Bottom from '$lib/Bottom.svelte';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import './styles.css';
</script>

<Navbar let:hidden let:toggle>
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			<div class="flex flex-row gap-3">
				<img src="/favicon.png" class="w-10" alt="Logo" />
				<span class="self-center">READRetro</span>
			</div>
		</span>
	</NavBrand>
	<NavHamburger on:click={toggle} />
	<NavUl {hidden}>
		<NavLi href="/" active={$page.url.pathname === '/'}>Pathway Explorer</NavLi>
		<NavLi href="/about" active={$page.url.pathname === '/about'}>About</NavLi>
	</NavUl>
</Navbar>

<div class="px-2 sm:px-4">
	<div class="mx-auto flex mb-20 flex-col container">
		<slot />
	</div>
</div>

<Bottom />