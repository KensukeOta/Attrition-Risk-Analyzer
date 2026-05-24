<script lang="ts">
	import { PUBLIC_API_URL } from "$env/static/public";

	type FeatureImportanceItem = {
		feature: string;
		importance_mean: number;
		importance_std: number;
		cv: number;
	};

	let items = $state<FeatureImportanceItem[]>([]);
	let loading = $state(true);
	let errorMessage = $state("");

	const topItems = $derived(items.slice(0, 15));

	const maxImportance = $derived(
		topItems.length > 0 ? Math.max(...topItems.map((item) => item.importance_mean)) : 1
	);

	function stabilityLabel(cv: number) {
		if (cv < 0.2) return "安定";
		if (cv < 0.4) return "やや変動";
		return "不安定";
	}

	function stabilityClass(cv: number) {
		if (cv < 0.2) return "bg-green-100 text-green-700";
		if (cv < 0.4) return "bg-yellow-100 text-yellow-700";
		return "bg-red-100 text-red-700";
	}

	async function fetchFeatureImportance() {
		loading = true;
		errorMessage = "";

		try {
			const res = await fetch(`${PUBLIC_API_URL}/api/v1/model/feature-importance`);

			if (!res.ok) {
				throw new Error("特徴量重要度の取得に失敗しました");
			}

			items = await res.json();
		} catch (e) {
			errorMessage = e instanceof Error ? e.message : "予期しないエラーが発生しました";
		} finally {
			loading = false;
		}
	}

	fetchFeatureImportance();
</script>

<svelte:head>
	<title>特徴量重要度</title>
</svelte:head>

<div class="mx-auto max-w-6xl px-4 py-10">
	<div class="mb-8">
		<p class="text-sm font-semibold tracking-widest text-slate-500 uppercase">
			Model Interpretation
		</p>

		<h1 class="mt-2 text-4xl font-black text-slate-900">特徴量重要度</h1>

		<p class="mt-3 max-w-3xl text-slate-600">
			LightGBMのgain importanceをRepeatedStratifiedKFoldで集計し、
			平均重要度・標準偏差・変動係数を表示しています。
		</p>
	</div>

	{#if loading}
		<div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
			<p class="text-slate-500">読み込み中...</p>
		</div>
	{:else if errorMessage}
		<div class="rounded-3xl border border-red-200 bg-red-50 p-6">
			<p class="font-medium text-red-700">{errorMessage}</p>
		</div>
	{:else}
		<div class="grid gap-6 lg:grid-cols-[2fr_1fr]">
			<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
				<div class="mb-6">
					<h2 class="text-xl font-bold text-slate-900">Top 15 Features</h2>
					<p class="mt-1 text-sm text-slate-500">
						棒が長いほど、モデルの予測改善への寄与が大きい特徴量です。
					</p>
				</div>

				<div class="space-y-4">
					{#each topItems as item, index}
						<div>
							<div class="mb-1 flex items-center justify-between gap-4">
								<div>
									<p class="font-semibold text-slate-800">
										{index + 1}. {item.feature}
									</p>
									<p class="text-xs text-slate-500">
										mean: {item.importance_mean.toFixed(1)}
										/ std: {item.importance_std.toFixed(1)}
										/ cv: {item.cv.toFixed(2)}
									</p>
								</div>

								<span
									class={`shrink-0 rounded-full px-3 py-1 text-xs font-bold ${stabilityClass(item.cv)}`}
								>
									{stabilityLabel(item.cv)}
								</span>
							</div>

							<div class="h-3 overflow-hidden rounded-full bg-slate-100">
								<div
									class="h-full rounded-full bg-blue-600"
									style={`width: ${(item.importance_mean / maxImportance) * 100}%`}
								></div>
							</div>
						</div>
					{/each}
				</div>
			</section>

			<aside class="space-y-6">
				<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
					<h2 class="text-lg font-bold text-slate-900">見方</h2>

					<div class="mt-4 space-y-3 text-sm text-slate-600">
						<p>
							<strong class="text-slate-900">importance_mean</strong>
							は、各foldでの重要度の平均です。
						</p>

						<p>
							<strong class="text-slate-900">importance_std</strong>
							は、fold間でどれくらい重要度がばらついたかを示します。
						</p>

						<p>
							<strong class="text-slate-900">cv</strong>
							は標準偏差 ÷ 平均です。小さいほど安定しています。
						</p>
					</div>
				</section>

				<section class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
					<h2 class="text-lg font-bold text-slate-900">安定性の目安</h2>

					<div class="mt-4 space-y-2 text-sm">
						<div class="flex items-center justify-between">
							<span>cv &lt; 0.2</span>
							<span class="rounded-full bg-green-100 px-3 py-1 font-bold text-green-700">
								安定
							</span>
						</div>

						<div class="flex items-center justify-between">
							<span>0.2 ≤ cv &lt; 0.4</span>
							<span class="rounded-full bg-yellow-100 px-3 py-1 font-bold text-yellow-700">
								やや変動
							</span>
						</div>

						<div class="flex items-center justify-between">
							<span>0.4 ≤ cv</span>
							<span class="rounded-full bg-red-100 px-3 py-1 font-bold text-red-700"> 不安定 </span>
						</div>
					</div>
				</section>
			</aside>
		</div>

		<section class="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
			<h2 class="text-xl font-bold text-slate-900">全特徴量一覧</h2>

			<div class="mt-4 overflow-x-auto">
				<table class="w-full text-left text-sm">
					<thead class="border-b border-slate-200 text-slate-500">
						<tr>
							<th class="py-3 pr-4">Feature</th>
							<th class="py-3 pr-4">Mean</th>
							<th class="py-3 pr-4">Std</th>
							<th class="py-3 pr-4">CV</th>
							<th class="py-3 pr-4">Stability</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-slate-100">
						{#each items as item}
							<tr>
								<td class="py-3 pr-4 font-medium text-slate-800">
									{item.feature}
								</td>
								<td class="py-3 pr-4 text-slate-600">
									{item.importance_mean.toFixed(1)}
								</td>
								<td class="py-3 pr-4 text-slate-600">
									{item.importance_std.toFixed(1)}
								</td>
								<td class="py-3 pr-4 text-slate-600">
									{item.cv.toFixed(2)}
								</td>
								<td class="py-3 pr-4">
									<span
										class={`rounded-full px-3 py-1 text-xs font-bold ${stabilityClass(item.cv)}`}
									>
										{stabilityLabel(item.cv)}
									</span>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>
	{/if}
</div>
