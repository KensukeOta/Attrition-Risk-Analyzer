<script lang="ts">
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import { Toaster } from "svelte-sonner";
	import { page } from "$app/state";

	let { children } = $props();

	let navItems = [
		{ href: "/", label: "Home" },
		{ href: "/predict", label: "単体予測" },
		{ href: "/csv", label: "CSV一括予測" },
		{ href: "/feature-importance", label: "特徴量重要度" },
		{ href: "/metrics", label: "モデル評価" }
	];

	function isActive(href: string) {
		if (href === "/") {
			return page.url.pathname === "/";
		}

		return page.url.pathname.startsWith(href);
	}
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="min-h-screen bg-slate-50">
	<header class="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur">
		<div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
			<a href="/" class="font-black text-slate-900"> Attrition Risk Analyzer </a>

			<nav class="hidden items-center gap-2 text-sm font-semibold md:flex">
				{#each navItems as item}
					<a
						href={item.href}
						class={`rounded-full px-3 py-2 transition ${
							isActive(item.href)
								? "bg-blue-600 text-white"
								: "text-slate-600 hover:bg-slate-100 hover:text-blue-600"
						}`}
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</div>
	</header>

	{@render children()}
	<Toaster richColors position="top-center" />
</div>
